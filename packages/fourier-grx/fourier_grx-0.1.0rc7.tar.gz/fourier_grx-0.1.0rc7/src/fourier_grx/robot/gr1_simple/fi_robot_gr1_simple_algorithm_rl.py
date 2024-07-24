import os
import time

import numpy
import torch
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_task_stage import TaskStage
from fourier_core.rl.rl_actor_critic_mlp import ActorCriticMLP
from fourier_core.rl.rl_robot_tool import torch_quat_rotate_inverse
from fourier_grx.robot.gr1_simple.fi_robot_gr1_simple_algorithm import RobotGR1SimpleAlgorithmBasicControlModel


class RobotGR1SimpleAlgorithmRLAirtimeControlModel(RobotGR1SimpleAlgorithmBasicControlModel):
    def __init__(self, dt: float = 0.01, decimation: int = 1):
        super().__init__()

        self.dt = dt
        self.decimation = int(decimation)
        self.decimation_count = 0

        # --------------------------------------------------------------------
        # warm up
        self.warmup_period = 0.0
        self.warmup_start_time: float | None = None

        # --------------------------------------------------------------------
        # real robot
        self.num_of_joints = 5 + 5

        self.flag_joint_pd_torque_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)

        self.index_of_joints_real_robot = torch.tensor(
            [
                0,
                1,
                2,
                3,
                4,  # 5 # left leg (5), no ankle roll
                6,
                7,
                8,
                9,
                10,  # 11 # right leg (5), no ankle roll
            ]
        )
        self.pd_control_kp_real_robot = numpy.array(
            [
                60,
                45,
                130,
                130,
                16,  # left leg(5)
                60,
                45,
                130,
                130,
                16,  # right leg(5)
            ]
        ) / (45 / 180 * numpy.pi)
        self.pd_control_kd_real_robot = self.pd_control_kp_real_robot / 10 * 2.5

        # --------------------------------------------------------------------

        self.num_of_joints_controlled = 5 + 5
        self.index_of_joints_controlled = numpy.array(
            [
                0,
                1,
                2,
                3,
                4,  # left leg (5), no ankle roll
                5,
                6,
                7,
                8,
                9,  # right leg (5), no ankle roll
            ]
        )
        self.joint_default_position = numpy.array(
            [
                0.0,
                0.0,
                -0.2618,
                0.5236,
                -0.2618,  # left leg (5), no ankle roll
                0.0,
                0.0,
                -0.2618,
                0.5236,
                -0.2618,  # right leg (5), no ankle roll
            ]
        )
        self.joint_default_position_tensor = torch.tensor(
            [
                [
                    0.0,
                    0.0,
                    -0.2618,
                    0.5236,
                    -0.2618,  # left leg (5), no ankle roll
                    0.0,
                    0.0,
                    -0.2618,
                    0.5236,
                    -0.2618,  # right leg (5), no ankle roll
                ]
            ],
            dtype=torch.float32,
        )

        self.nn_act_scale_action = 1.00

        # --------------------------------------------------------------------
        # actor
        self.ac_profile = "GR1T1-airtime"
        self.num_actor_obs = 39
        self.num_critc_obs = 168
        self.num_action = self.num_of_joints_controlled

        # flags
        self.flag_buffer_inited = FlagState.CLEAR

        self.commands = torch.zeros(1, 3)
        self.command_linear_velocity_x_range = torch.tensor([[-0.50, 0.50]])  # unit: m/s
        self.command_linear_velocity_y_range = torch.tensor([[-0.50, 0.50]])  # unit: m/s
        self.command_angular_velocity_range = torch.tensor([[-0.50, 0.50]])  # unit: rad/s

        self.measured_joint_position = torch.zeros(1, self.num_of_joints_controlled)
        self.measured_joint_velocity = torch.zeros(1, self.num_of_joints_controlled)
        self.measured_joint_kinetic = torch.zeros(1, self.num_of_joints_controlled)
        self.measured_joint_position_offset = torch.zeros(1, self.num_of_joints_controlled)

        self.base_height_target = 0.90
        self.gravity_vector = torch.tensor([[0.0, 0.0, -1.0]])
        self.base_quat_to_world = torch.tensor([[0.0, 0.0, 0.0, 1.0]])

        self.nn_actor = None
        self.init_actor()

        # --------------------------------------------------------------------
        # input
        self.base_xyz_vel_to_self = torch.zeros(1, 3)
        self.base_rpy_vel_to_self = torch.zeros(1, 3)
        self.base_quat_to_world = torch.zeros(1, 4)
        self.base_project_gravity = torch.zeros(1, 3)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # output
        self.target_joint_position_offset = torch.zeros(1, self.num_of_joints_controlled)
        self.target_joint_position = torch.zeros(1, self.num_of_joints_controlled)
        # --------------------------------------------------------------------

    def init_actor(self):
        self.nn_actor_input_base_angular_velocity = torch.zeros(1, 3)
        self.nn_actor_input_base_projected_gravity = torch.zeros(1, 3)
        self.nn_actor_input_commands = torch.zeros(1, 3)
        self.nn_actor_input_measured_joint_position_offset = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_measured_joint_velocity = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_action = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_length = self.num_actor_obs
        self.nn_actor_input = torch.zeros(1, self.nn_actor_input_length)

        self.nn_actor_output_tensor = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output_raw = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output_scale = torch.ones(1, self.num_of_joints_controlled) * self.nn_act_scale_action
        self.nn_actor_output_clip_max = torch.tensor(
            [
                0.79,
                0.7,
                0.7,
                1.92,
                0.52,  # left leg (5), no ankle roll
                0.09,
                0.7,
                0.7,
                1.92,
                0.52,  # left leg (5), no ankle roll
            ]
        )
        self.nn_actor_output_clip_min = torch.tensor(
            [
                -0.09,
                -0.7,
                -1.75,
                -0.09,
                -1.05,  # left leg (5), no ankle roll
                -0.79,
                -0.7,
                -1.75,
                -0.09,
                -1.05,  # left leg (5), no ankle roll
            ]
        )
        self.nn_actor_output_clip_max = self.nn_actor_output_clip_max + 45 / 180 * torch.pi / 3
        self.nn_actor_output_clip_min = self.nn_actor_output_clip_min - 45 / 180 * torch.pi / 3
        self.nn_actor_output_scaled = torch.tensor([])

    def load_actor(self):
        if self.nn_actor is None:
            self.model_file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                # "stand_model.pt"
                "walk_model.pt",
            )

            model = torch.load(self.model_file_path, map_location=torch.device("cpu"))
            model_actor_dict = model["model_state_dict"]

            self.nn_actor = ActorCriticMLP(
                num_actor_obs=self.num_actor_obs,
                num_critic_obs=self.num_critc_obs,
                num_actions=self.num_action,
                actor_hidden_dims=[512, 256, 128],
                critic_hidden_dims=[512, 256, 128],
            )

            self.nn_actor.load_state_dict(model_actor_dict)

    def init_buffer(self, init_output):
        # Jason 2024-07-07:
        # If the init_output is the default position, the nn_actor_output will be zero
        self.nn_actor_output = (
            init_output[0, self.index_of_joints_controlled]
            - self.joint_default_position_tensor[0, self.index_of_joints_controlled]
        ) / self.nn_actor_output_scale

    def update_buffer(
        self,
        commands,
        base_measured_quat_to_world,
        base_measured_rpy_vel_to_self,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
    ):
        self.commands = commands
        self.commands[0, 0] = torch.clip(
            self.commands[0, 0],
            min=self.command_linear_velocity_x_range[0, 0],
            max=self.command_linear_velocity_x_range[0, 1],
        )
        self.commands[0, 1] = torch.clip(
            self.commands[0, 1],
            min=self.command_linear_velocity_y_range[0, 0],
            max=self.command_linear_velocity_y_range[0, 1],
        )
        self.commands[0, 2] = torch.clip(
            self.commands[0, 2],
            min=self.command_angular_velocity_range[0, 0],
            max=self.command_angular_velocity_range[0, 1],
        )

        # Jason 2024-07-08:
        # torch_quat_rotate_inverse will be called here at first and finish the torch.jit.script
        self.base_quat_to_world = base_measured_quat_to_world
        self.base_project_gravity = torch_quat_rotate_inverse(self.base_quat_to_world, self.gravity_vector)

        self.base_rpy_vel_to_self = base_measured_rpy_vel_to_self
        self.measured_joint_position = joint_measured_position_urdf

        self.measured_joint_position_offset = self.measured_joint_position - self.joint_default_position_tensor

        self.measured_joint_velocity = joint_measured_velocity_urdf

    def actor_prepare(self):
        # base angular velocity
        self.nn_actor_input_base_angular_velocity = self.base_rpy_vel_to_self

        # projected gravity
        self.nn_actor_input_base_projected_gravity = self.base_project_gravity

        # commands
        self.nn_actor_input_commands = self.commands

        # measured joint position offset, velocity
        self.nn_actor_input_measured_joint_position_offset = self.measured_joint_position_offset

        self.nn_actor_input_measured_joint_velocity = self.measured_joint_velocity

        # actions
        self.nn_actor_input_action = self.nn_actor_output.clone()

    def actor_run(self):
        # prepare
        self.actor_prepare()

        # obs
        self.actor_obs()

        # nn
        self.actor_nn()

        # output
        self.actor_output()

        return self.target_joint_position

    def actor_obs(self):
        if self.ac_profile == "GR1T1-airtime":
            obs_buf = torch.cat(
                (
                    # base related
                    self.nn_actor_input_base_angular_velocity,
                    self.nn_actor_input_base_projected_gravity,
                    self.nn_actor_input_commands,
                    # dof related
                    self.nn_actor_input_measured_joint_position_offset,
                    self.nn_actor_input_measured_joint_velocity,
                    self.nn_actor_input_action,
                ),
                dim=-1,
            )

            self.nn_actor_input = obs_buf

        else:
            raise Exception("Unknown ac_profile: ", self.ac_profile)

    def actor_nn(self):
        self.nn_actor_output_tensor = self.nn_actor(self.nn_actor_input)

        self.nn_actor_output_raw = self.nn_actor_output_tensor.detach()
        self.nn_actor_output = torch.clip(
            self.nn_actor_output_raw, min=self.nn_actor_output_clip_min, max=self.nn_actor_output_clip_max
        )

        # store nn output
        # self.nn_actor_input_action = \
        #     self.nn_actor_output.clone()

    def actor_output(self):
        self.nn_actor_output_scaled = self.nn_actor_output * self.nn_actor_output_scale

        # prepare output
        self.target_joint_position_offset = self.nn_actor_output_scaled

        self.target_joint_position = self.target_joint_position_offset + self.joint_default_position_tensor

    def run(
        self,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
        init_output=None,
        commands=numpy.array([0, 0, 0]),
        base_measured_quat_to_world=numpy.array([0, 0, 0, 1]),
        base_measured_rpy_vel_to_self=numpy.array([0, 0, 0]),
    ):
        """
        Run the RL walk control algorithm.

        Input:
        - init_output: initial output of the robot, rad
        - commands: commands for the robot, [linear_velocity_x, linear_velocity_y, angular_velocity], m/s, m/s, rad/s
        - base_measured_xyz_to_world: measured base position in world, [x, y, z], m
        - base_measured_quat_to_world: measured base quaternion to world, [x, y, z, w]
        - base_measured_xyz_vel_to_self: measured base linear velocity in world, [x, y, z], m/s
        - base_measured_rpy_vel_to_self: measured base angular velocity in world, [roll, pitch, yaw], rad/s
        - joint_measured_position_urdf: measured joint position in URDF, rad
        - joint_measured_velocity_urdf: measured joint velocity in URDF, rad/s

        Output:
        - target_joint_position: output joint control target, rad
        """

        if self.stage == TaskStage.STAGE_INIT:
            self.flag_buffer_inited = FlagState.CLEAR
            self.decimation_count = 0
            self.stage = TaskStage.STAGE_WARM_UP

        if self.stage == TaskStage.STAGE_START:
            self.decimation_count = 0
            self.stage = TaskStage.STAGE_WARM_UP

        if self.stage == TaskStage.STAGE_WARM_UP:
            self.load_actor()

            # run neural network to warm up, all inputs are zero
            self.nn_actor(self.nn_actor_input)

            if self.warmup_start_time is None:
                self.warmup_start_time = time.time()

            if time.time() - self.warmup_start_time >= self.warmup_period:
                self.init_actor()
                self.stage = TaskStage.STAGE_RUN

            self.target_joint_position = self.joint_default_position_tensor
            target_joint_position = self.target_joint_position
            target_joint_position = target_joint_position.numpy()[0]

            return target_joint_position

        # check decimation count
        if self.decimation_count % self.decimation == 0:
            # update decimation count
            self.decimation_count += 1
        else:
            # update decimation count
            self.decimation_count += 1

            target_joint_position = self.target_joint_position

            target_joint_position = target_joint_position.numpy()[0]

            return target_joint_position

        # --------------------------------------------------------------------
        # numpy.array -> torch.tensor
        # Jason 2024-07-07: torch.from_numpy() share the same memory with numpy array, will not copy the data
        if init_output is None:
            init_output = numpy.zeros(self.num_of_joints_controlled)
        torch_init_output = torch.from_numpy(init_output.astype(numpy.float32)).unsqueeze(0)

        torch_commands = torch.from_numpy(commands.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_quat_to_world = torch.from_numpy(
            base_measured_quat_to_world.astype(numpy.float32)
        ).unsqueeze(0)
        torch_base_measured_rpy_vel_to_self = torch.from_numpy(
            base_measured_rpy_vel_to_self.astype(numpy.float32)
        ).unsqueeze(0)
        torch_joint_measured_position_urdf = torch.from_numpy(
            joint_measured_position_urdf.astype(numpy.float32)
        ).unsqueeze(0)
        torch_joint_measured_velocity_urdf = torch.from_numpy(
            joint_measured_velocity_urdf.astype(numpy.float32)
        ).unsqueeze(0)

        # --------------------------------------------------------------------
        # state
        if self.flag_buffer_inited == FlagState.CLEAR:
            self.init_buffer(
                init_output=torch_init_output,
            )
            self.flag_buffer_inited = FlagState.SET

        self.update_buffer(
            commands=torch_commands,
            base_measured_quat_to_world=torch_base_measured_quat_to_world,
            base_measured_rpy_vel_to_self=torch_base_measured_rpy_vel_to_self,
            joint_measured_position_urdf=torch_joint_measured_position_urdf,
            joint_measured_velocity_urdf=torch_joint_measured_velocity_urdf,
        )
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # actor
        self.load_actor()

        # actor
        target_joint_position = self.actor_run()
        target_joint_position = target_joint_position.numpy()[0]

        # --------------------------------------------------------------------

        return target_joint_position


# ======================================================================================================================


class RobotGR1SimpleAlgorithmRLAirtimeStackControlModel(RobotGR1SimpleAlgorithmBasicControlModel):
    def __init__(self, dt: float = 0.01, decimation: int = 1):
        super().__init__()

        self.dt = dt
        self.decimation = int(decimation)
        self.decimation_count = 0

        # robot model
        self.num_of_joints = 5 + 5
        self.joint_default_position = torch.tensor(
            [
                [
                    0.0,
                    0.0,
                    -0.2618,
                    0.5236,
                    -0.2618,  # left leg (5), no ankle roll
                    0.0,
                    0.0,
                    -0.2618,
                    0.5236,
                    -0.2618,  # right leg (5), no ankle roll
                ]
            ],
            dtype=torch.float32,
        )

        self.num_of_joints_controlled = 5 + 5
        self.index_of_joints_controlled = torch.tensor(
            [
                0,
                1,
                2,
                3,
                4,  # left leg (5), no ankle roll
                5,
                6,
                7,
                8,
                9,  # right leg (5), no ankle roll
            ]
        )

        self.index_of_joints_urdf = torch.tensor(
            [
                0,
                1,
                2,
                3,
                4,  # 5 # left leg (5), no ankle roll
                6,
                7,
                8,
                9,
                10,  # 11 # right leg (5), no ankle roll
            ]
        )

        self.flag_joint_pd_torque_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)

        # actor-critic
        self.ac_profile = "GR1T1-airtime-stack"
        self.num_actor_obs = 39
        self.num_critc_obs = 168
        self.num_action = self.num_of_joints_controlled
        self.num_stack = 10

    # def load_actor(self):
    #     # nerual network
    #     try:
    #         self.model_file_path = os.path.join(
    #             os.path.dirname(os.path.abspath(__file__)),
    #             # "stand_model.pt"
    #             # "walk_model.pt"
    #             "model_1000.pt"
    #         )
    #
    #         model = torch.load(self.model_file_path, map_location=torch.device("cpu"))
    #         model_actor_dict = model["model_state_dict"]
    #
    #         self.nn_actor = \
    #             ActorCriticMLP(num_actor_obs=self.num_actor_obs * self.num_stack,
    #                            num_critic_obs=self.num_critc_obs * self.num_stack,
    #                            num_actions=self.num_action,
    #                            actor_hidden_dims=[512, 256, 128],
    #                            critic_hidden_dims=[512, 256, 128])
    #
    #         self.nn_actor.load_state_dict(model_actor_dict)
    #
    #     except Exception as e:
    #         Logger().print_trace_warning(e)
    #
    # def init_buffer(self,
    #                 base_measured_xyz_to_world,
    #                 base_measured_quat_to_world,
    #                 base_measured_xyz_vel_to_world,
    #                 base_measured_rpy_vel_to_world,
    #                 joint_measured_position_urdf,
    #                 joint_measured_velocity_urdf,
    #                 measured_surround_heights=None):
    #     super().init_buffer(
    #         base_measured_xyz_to_world,
    #         base_measured_quat_to_world,
    #         base_measured_xyz_vel_to_world,
    #         base_measured_rpy_vel_to_world,
    #         joint_measured_position_urdf,
    #         joint_measured_velocity_urdf,
    #         measured_surround_heights=measured_surround_heights)
    #
    #     # input buffer
    #     self.nn_actor_input = torch.zeros(1, self.num_actor_obs * self.num_stack, dtype=torch.float32)
    #
    #     # output buffer
    #     self.nn_actor_output_scale = torch.ones(1, self.num_of_joints_controlled) \
    #                                  * self.nn_actor_output_scale_factor
    #     self.nn_actor_output_clip_max = torch.tensor([
    #         0.79, 0.7, 0.7, 1.92, 0.52,  # left leg (5), no ankle roll
    #         0.09, 0.7, 0.7, 1.92, 0.52,  # left leg (5), no ankle roll
    #     ])
    #     self.nn_actor_output_clip_min = torch.tensor([
    #         -0.09, -0.7, -1.75, -0.09, -1.05,  # left leg (5), no ankle roll
    #         -0.79, -0.7, -1.75, -0.09, -1.05,  # left leg (5), no ankle roll
    #     ])
    #
    #     self.nn_actor_output_clip_max = self.nn_actor_output_clip_max + 1 / 3
    #     self.nn_actor_output_clip_min = self.nn_actor_output_clip_min - 1 / 3
    #
    # def actor_obs(self):
    #     if self.ac_profile == "GR1T1-airtime-stack":
    #         obs_buf = torch.cat((
    #             # base related
    #             self.nn_actor_input_base_angular_velocity,
    #             self.nn_actor_input_base_projected_gravity,
    #             self.nn_actor_input_commands,
    #
    #             # dof related
    #             self.nn_actor_input_measured_joint_position,
    #             self.nn_actor_input_measured_joint_velocity,
    #             self.nn_actor_input_action,
    #         ), dim=-1)
    #
    #         self.nn_actor_input = torch.cat((
    #             self.nn_actor_input[:, self.num_actor_obs:], obs_buf
    #         ), dim=-1)
    #
    #     else:
    #         raise Exception("Unknown ac_profile: ", self.ac_profile)
