import os
import time

import numpy
import torch

from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_task_stage import TaskStage
from fourier_core.rl.rl_robot_tool import torch_quat_rotate_inverse

from fourier_grx.robot.gr1_simple.fi_robot_gr1_simple_algorithm import RobotGR1SimpleAlgorithmBasicControlModel
from fourier_grx.algorithm.gait_generator import FourierGaitGenerator as GaitGenerator


# fmt: off

class RobotGR1SimpleAlgorithmRLCPGStackControlModel(RobotGR1SimpleAlgorithmBasicControlModel):
    def __init__(
            self,
            dt: float = 0.01,
            decimation: int = 1,
            warmup_period=1.0,
            actor_model_file_path=None,
    ):
        """
        Simple (Only lower limb without ankle roll) GR1T1 robot control model with RL CPG stack algorithm.

        Input:
        - dt: time step, s
        - decimation: decimation factor
        - warmup_period: warm up period, s
        - actor_model_file_path: actor model file path
        """
        super().__init__()

        # --------------------------------------------------------------------
        # dt and decimation
        self.dt: float = dt
        self.decimation: int = int(decimation)
        self.decimation_count = 0

        # --------------------------------------------------------------------
        # warm up
        self.warmup_period: float = warmup_period
        self.warmup_start_time: float | None = None

        # --------------------------------------------------------------------
        # model file path
        self.actor_model_file_path: str | None = actor_model_file_path

        # --------------------------------------------------------------------
        # real robot
        self.num_of_joints = 5 + 5

        self.flag_joint_pd_torque_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)

        self.index_of_joints_real_robot = torch.tensor(
            [
                0, 1, 2, 3, 4,  # 5 # left leg (5), no ankle roll
                6, 7, 8, 9, 10,  # 11 # right leg (5), no ankle roll
            ]
        )
        self.pd_control_kp_real_robot = numpy.array(
            [
                # left leg(5)
                60 / (15 / 180 * numpy.pi),
                45 / (15 / 180 * numpy.pi),
                130 / (30 / 180 * numpy.pi),
                130 / (30 / 180 * numpy.pi),
                18 / (30 / 180 * numpy.pi),
                # 9 / (30 / 180 * numpy.pi),
                # right leg(5)
                60 / (15 / 180 * numpy.pi),
                45 / (15 / 180 * numpy.pi),
                130 / (30 / 180 * numpy.pi),
                130 / (30 / 180 * numpy.pi),
                18 / (30 / 180 * numpy.pi),
                # 9 / (30 / 180 * numpy.pi),
            ]
        )
        self.pd_control_kd_real_robot = self.pd_control_kp_real_robot / 10 * 0.5

        # --------------------------------------------------------------------

        self.num_of_joints_controlled = 5 + 5
        self.index_of_joints_controlled = numpy.array(
            [
                0, 1, 2, 3, 4,  # left leg (5), no ankle roll
                5, 6, 7, 8, 9,  # right leg (5), no ankle roll
            ]
        )
        self.joint_default_position = numpy.array(
            [
                0.0, 0.0, -0.2618, 0.5236, -0.2618,  # left leg (5), no ankle roll
                0.0, 0.0, -0.2618, 0.5236, -0.2618,  # right leg (5), no ankle roll
            ]
        )
        self.joint_default_position_tensor = torch.tensor(
            [
                [
                    0.0, 0.0, -0.2618, 0.5236, -0.2618,  # left leg (5), no ankle roll
                    0.0, 0.0, -0.2618, 0.5236, -0.2618,  # right leg (5), no ankle roll
                ]
            ],
            dtype=torch.float32,
        )

        self.nn_obs_scale_lin_vel = 1.00
        self.nn_obs_scale_ang_vel = 1.00
        self.nn_obs_scale_command = 1.00
        self.nn_obs_scale_gravity = 1.00
        self.nn_obs_scale_dof_pos = 1.00
        self.nn_obs_scale_dof_vel = 1.00
        self.nn_act_scale_action = 1.00

        # --------------------------------------------------------------------
        # env
        self.num_envs = 1
        self.device = torch.device("cpu")

        # actor
        self.ac_profile = "GR1T1-airtime"
        self.num_actor_obs = 45
        self.num_actor_obs_stack = 10
        self.num_actor_act = self.num_of_joints_controlled

        # flags
        self.flag_buffer_inited = FlagState.CLEAR

        self.commands = torch.zeros(self.num_envs, 3)
        self.command_linear_velocity_x_range = torch.tensor([[-0.50, 0.50]])  # unit: m/s
        self.command_linear_velocity_y_range = torch.tensor([[-0.50, 0.50]])  # unit: m/s
        self.command_angular_velocity_range = torch.tensor([[-0.50, 0.50]])  # unit: rad/s

        self.measured_joint_position = torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.measured_joint_velocity = torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.measured_joint_kinetic = torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.measured_joint_position_offset = torch.zeros(self.num_envs, self.num_of_joints_controlled)

        self.base_height_target = 0.90
        self.gravity_vector = torch.tensor([[0.0, 0.0, -1.0]])
        self.base_quat_to_world = torch.tensor([[0.0, 0.0, 0.0, 1.0]])

        self.nn_actor = None
        self._init_actor()

        # --------------------------------------------------------------------
        # gait
        self.swing_feet_height_target = 0.10  # unit: m

        self.gait_generator = \
            GaitGenerator(num_envs=self.num_envs,
                          num_feet=2,
                          phase_offset=torch.tensor([0.0, torch.pi],
                                                    dtype=torch.float,
                                                    device=self.device),
                          dt=self.dt,
                          foot_height_target=self.swing_feet_height_target,
                          device=self.device)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # input
        self.base_xyz_vel_to_self = torch.zeros(self.num_envs, 3)
        self.base_rpy_vel_to_self = torch.zeros(self.num_envs, 3)
        self.base_xyz_to_world = torch.zeros(self.num_envs, 3)
        self.base_quat_to_world = torch.zeros(self.num_envs, 4)
        self.base_project_gravity = torch.zeros(self.num_envs, 3)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # output
        self.target_joint_position_offset = torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.target_joint_position = torch.zeros(self.num_envs, self.num_of_joints_controlled)
        # --------------------------------------------------------------------

    def _init_actor(self):
        self.nn_actor_input_base_angular_velocity = \
            torch.zeros(self.num_envs, 3)
        self.nn_actor_input_base_projected_gravity = \
            torch.zeros(self.num_envs, 3)
        self.nn_actor_input_commands = \
            torch.zeros(self.num_envs, 3)
        self.nn_actor_input_measured_joint_position_offset = \
            torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.nn_actor_input_measured_joint_velocity = \
            torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.nn_actor_input_action = \
            torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.nn_actor_input_gait_x = \
            torch.zeros(self.num_envs, 2)
        self.nn_actor_input_gait_y = \
            torch.zeros(self.num_envs, 2)
        self.nn_actor_input_gait_phase = \
            torch.zeros(self.num_envs, 2)
        self.nn_actor_input_length = \
            self.num_actor_obs * self.num_actor_obs_stack
        self.nn_actor_input = \
            torch.zeros(self.num_envs, self.nn_actor_input_length)

        self.nn_actor_output_tensor = \
            torch.zeros(self.num_envs, self.num_actor_act)
        self.nn_actor_output_raw = \
            torch.zeros(self.num_envs, self.num_actor_act)
        self.nn_actor_output = \
            torch.zeros(self.num_envs, self.num_actor_act)
        self.nn_actor_output_scale = \
            torch.ones(self.num_envs, self.num_actor_act) * self.nn_act_scale_action
        self.nn_actor_output_clip_max = \
            torch.tensor([
                0.79, 0.7, 0.7, 1.92, 0.52,  # left leg (5), no ankle roll
                0.09, 0.7, 0.7, 1.92, 0.52,  # left leg (5), no ankle roll
            ])
        self.nn_actor_output_clip_min = \
            torch.tensor([
                -0.09, -0.7, -1.75, -0.09, -1.05,  # left leg (5), no ankle roll
                -0.79, -0.7, -1.75, -0.09, -1.05,  # left leg (5), no ankle roll
            ])
        self.nn_actor_output_clip_max = \
            self.nn_actor_output_clip_max \
            + numpy.array([
                15, 15, 30, 30, 30,
                15, 15, 30, 30, 30,
            ]) / 180 * numpy.pi
        self.nn_actor_output_clip_min = \
            self.nn_actor_output_clip_min \
            - numpy.array([
                15, 15, 30, 30, 30,
                15, 15, 30, 30, 30,
            ]) / 180 * numpy.pi
        self.nn_actor_output_scaled = torch.tensor([])

    def _load_actor(self):
        if self.nn_actor is None:
            if self.actor_model_file_path is None:
                model_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               "cpg_stack_actor.pt")
            else:
                model_file_path = self.actor_model_file_path

            try:
                self.nn_actor = torch.jit.load(model_file_path, map_location=self.device)
            except Exception as exp:
                print(f"Load actor model error: {exp}")
                self.nn_actor = None

    def _init_buffer(self, init_output):
        # Jason 2024-07-07:
        # If the init_output is the default position, the nn_actor_output will be zero
        self.nn_actor_output = \
            (init_output[0, self.index_of_joints_controlled]
             - self.joint_default_position_tensor[0, self.index_of_joints_controlled]) \
            / self.nn_actor_output_scale

    def _update_buffer(
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

    def _actor_run(self):
        # prepare
        self._actor_prepare()

        # obs
        self._actor_obs()

        # nn
        self._actor_nn()

        # output
        self._actor_output()

        return self.target_joint_position

    def _actor_prepare(self):
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

        # gait x, y, phase
        self.nn_actor_input_gait_x = self.gait_generator.get_x()
        self.nn_actor_input_gait_y = self.gait_generator.get_y()
        self.nn_actor_input_gait_phase = self.gait_generator.get_phase_norm()

    def _actor_obs(self):
        obs_buf = torch.cat(
            (
                # base related
                self.nn_actor_input_base_angular_velocity * self.nn_obs_scale_ang_vel,
                self.nn_actor_input_base_projected_gravity * self.nn_obs_scale_gravity,
                self.nn_actor_input_commands * self.nn_obs_scale_command,
                # dof related
                self.nn_actor_input_measured_joint_position_offset * self.nn_obs_scale_dof_pos,
                self.nn_actor_input_measured_joint_velocity * self.nn_obs_scale_dof_vel,
                self.nn_actor_input_action,
                # gait related
                self.nn_actor_input_gait_x,
                self.nn_actor_input_gait_y,
                self.nn_actor_input_gait_phase,
            ),
            dim=-1,
        )

        self.nn_actor_input = torch.cat(
            (
                self.nn_actor_input[:, self.num_actor_obs:],
                obs_buf),
            dim=-1).float()

    def _actor_nn(self):
        self.nn_actor_output_tensor = self.nn_actor(self.nn_actor_input)

        self.nn_actor_output_raw = self.nn_actor_output_tensor.detach()

        self.nn_actor_output = torch.clip(
            self.nn_actor_output_raw,
            min=self.nn_actor_output_clip_min,
            max=self.nn_actor_output_clip_max
        )

    def _actor_output(self):
        self.target_joint_position_offset = \
            self.nn_actor_output * self.nn_actor_output_scale

        self.target_joint_position = \
            self.target_joint_position_offset + self.joint_default_position_tensor

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
        - base_measured_quat_to_world: measured base quaternion to world, [x, y, z, w]
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
            # run neural network to warm up, all inputs are zero
            self._load_actor()

            self.nn_actor(self.nn_actor_input)

            if self.warmup_start_time is None:
                self.warmup_start_time = time.time()

            if time.time() - self.warmup_start_time >= self.warmup_period:
                self._init_actor()
                self.stage = TaskStage.STAGE_RUN
                print("Warmup done. Running algorithm...")

            self.target_joint_position = self.joint_default_position_tensor
            target_joint_position = self.target_joint_position
            target_joint_position = target_joint_position.numpy()[0]

            return target_joint_position

        # gait
        self.gait_generator.step()

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
        torch_init_output = \
            torch.from_numpy(init_output.astype(numpy.float32)).unsqueeze(0)

        torch_commands = \
            torch.from_numpy(commands.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_quat_to_world = \
            torch.from_numpy(base_measured_quat_to_world.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_rpy_vel_to_self = \
            torch.from_numpy(base_measured_rpy_vel_to_self.astype(numpy.float32)).unsqueeze(0)
        torch_joint_measured_position_urdf = \
            torch.from_numpy(joint_measured_position_urdf.astype(numpy.float32)).unsqueeze(0)
        torch_joint_measured_velocity_urdf = \
            torch.from_numpy(joint_measured_velocity_urdf.astype(numpy.float32)).unsqueeze(0)

        # gait
        if torch.norm(torch_commands[0, 0:2]) < 0.1:
            self.gait_generator.set_stand_pattern()
        else:
            self.gait_generator.set_walk_pattern()

        # --------------------------------------------------------------------
        # state
        if self.flag_buffer_inited == FlagState.CLEAR:
            self._init_buffer(
                init_output=torch_init_output,
            )
            self.flag_buffer_inited = FlagState.SET

        self._update_buffer(
            commands=torch_commands,
            base_measured_quat_to_world=torch_base_measured_quat_to_world,
            base_measured_rpy_vel_to_self=torch_base_measured_rpy_vel_to_self,
            joint_measured_position_urdf=torch_joint_measured_position_urdf,
            joint_measured_velocity_urdf=torch_joint_measured_velocity_urdf,
        )
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # actor
        target_joint_position = self._actor_run()
        target_joint_position = target_joint_position.numpy()[0]
        # --------------------------------------------------------------------

        return target_joint_position

# fmt: on
