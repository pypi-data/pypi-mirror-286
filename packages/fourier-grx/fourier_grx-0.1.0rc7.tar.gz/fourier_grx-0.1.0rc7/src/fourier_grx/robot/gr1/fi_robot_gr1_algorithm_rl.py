import math

import numpy
import torch
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.rl.rl_robot_tool import torch_quat_rotate_inverse
from fourier_grx.robot.gr1.fi_robot_gr1_algorithm import RobotGR1AlgorithmBasicControlModel


class RobotGR1AlgorithmRLAC(RobotGR1AlgorithmBasicControlModel):
    def __init__(self, dt=0.01):
        super().__init__()

        # robot model
        self.num_of_joints = 6 + 6 + 3 + 3 + 7 + 7
        self.joint_default_position = torch.tensor(
            [
                [
                    0.0,
                    0.0,
                    -0.2618,
                    0.5236,
                    -0.2618,
                    0.0,  # left leg (6)
                    0.0,
                    0.0,
                    -0.2618,
                    0.5236,
                    -0.2618,
                    0.0,  # right leg (6)
                    0.0,
                    0.0,
                    0.0,  # waist (3)
                    0.0,
                    0.0,
                    0.0,  # head (3)
                    0.0,
                    0.2,
                    0.0,
                    -0.3,
                    0.0,
                    0.0,
                    0.0,  # left arm (7)
                    0.0,
                    -0.2,
                    0.0,
                    -0.3,
                    0.0,
                    0.0,
                    0.0,  # right arm (7)
                ]
            ],
            dtype=torch.float32,
        )

        self.num_of_joints_controlled = 6 + 6 + 3 + 3 + 4 + 4
        self.index_of_joints_controlled = torch.tensor(
            [
                0,
                1,
                2,
                3,
                4,
                5,  # left leg
                6,
                7,
                8,
                9,
                10,
                11,  # right leg
                12,
                13,
                14,  # waist
                15,
                16,
                17,  # head
                18,
                19,
                20,
                21,
                22,
                23,
                24,  # left arm
                25,
                26,
                27,
                28,
                29,
                30,
                31,  # right arm
            ]
        )

        self.flag_joint_pd_torque_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)

        # actor-critic
        self.ac_profile = "GR1T1"
        self.num_actor_obs = 39
        self.num_critc_obs = 168
        self.num_action = self.num_of_joints_controlled

        # flags
        self.flag_model_inited = FlagState.CLEAR
        self.flag_buffer_inited = FlagState.CLEAR
        self.flag_actor_inited = FlagState.CLEAR

        self.dt = dt

        self.transform_move_count_max = 1000

        self.target_linear_velocity_x_range = torch.tensor([[-0.50, 0.50]])  # unit: m/s
        self.target_linear_velocity_y_range = torch.tensor([[-0.50, 0.50]])  # unit: m/s
        self.target_angular_velocity_range = torch.tensor([[-0.50, 0.50]])  # unit: rad/s

        self.measured_joint_position = []
        self.measured_joint_velocity = []
        self.measured_joint_kinetic = []

        self.gait_clock_time = 0.0
        self.gait_clock_dt = self.dt
        self.gait_clock_period = 1.0
        self.gait_phase = torch.tensor([[0.0, 0.0]])
        self.gait_phase_ratio = torch.tensor([[0.0, 0.0]])
        self.gait_phase_theta = torch.tensor([[0.0, 0.0]])

        self.base_height_target = 0.90
        self.gravity_vector = torch.tensor([[0.0, 0.0, -1.0]])
        self.base_quat_to_world = torch.tensor([[0.0, 0.0, 0.0, 1.0]])

        self.base_linear_velocity_avg_factor = torch.tensor([[0.0, 0.0, 0.0]])
        self.base_angular_velocity_avg_factor = torch.tensor([[0.0, 0.0, 0.0]])
        self.base_linear_velocity_avg = torch.tensor([[0.0, 0.0, 0.0]])
        self.base_angular_velocity_avg = torch.tensor([[0.0, 0.0, 0.0]])

        self.nn_actor_input_base_linear_velocity = torch.zeros(1, 3)
        self.nn_actor_input_base_angular_velocity = torch.zeros(1, 3)
        self.nn_actor_input_base_projected_gravity = torch.zeros(1, 3)
        self.nn_actor_input_commands = torch.zeros(1, 3)
        self.nn_actor_input_measured_joint_position = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_measured_joint_velocity = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_action = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_gait_phase_sin = torch.zeros(1, 2)
        self.nn_actor_input_gait_phase_cos = torch.zeros(1, 2)
        self.nn_actor_input_gait_phase_ratio = torch.zeros(1, 2)
        self.nn_actor_input_gait_cycle = torch.zeros(1, 1)
        self.nn_actor_input_base_height_offset = torch.zeros(1, 1)
        self.nn_actor_input_base_linear_velocity_avg = torch.zeros(1, 3)
        self.nn_actor_input_base_angular_velocity_avg = torch.zeros(1, 3)
        self.nn_actor_input_surround_heights_offset = torch.tensor([])
        self.nn_actor_input = torch.tensor([])

        self.nn_actor = None

        self.nn_actor_output_tensor = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output_raw = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output_scale_factor = 1.0
        self.nn_actor_output_scale = torch.tensor([])
        self.nn_actor_output_clip_min = torch.tensor([])
        self.nn_actor_output_clip_max = torch.tensor([])
        self.nn_actor_output_scaled = torch.tensor([])

        self.target_joint_position = torch.tensor([])

        self.output_joint_control_mode = torch.tensor([])
        self.output_joint_position = torch.tensor([])
        self.output_joint_velocity = torch.tensor([])
        self.output_joint_acceleration = torch.tensor([])
        self.output_joint_kinetic = torch.tensor([])

        # prepare variables
        self.gait_clock_period = 1.0
        self.gait_phase = torch.tensor([[0.0, 0.0]])
        self.gait_phase_ratio_stand = torch.tensor([[0.0, 0.0]])
        self.gait_phase_ratio_walk = torch.tensor([[0.35, 0.35]])
        self.gait_phase_ratio = self.gait_phase_ratio_stand
        self.gait_phase_theta = torch.tensor([[0.00, 0.50]])

        self.base_height_target = 0.90

        # --------------------------------------------------------------------
        # Jason 2024-03-05:
        # Make sure the filter has same cut-off frequency as in the simulator
        self.base_linear_velocity_avg_factor = 0.02
        self.base_angular_velocity_avg_factor = 0.01
        # --------------------------------------------------------------------

        # input variables
        self.base_xyz_vel_to_self = torch.zeros(1, 3)
        self.base_rpy_vel_to_self = torch.zeros(1, 3)
        self.base_xyz_to_world = torch.zeros(1, 3)
        self.base_quat_to_world = torch.zeros(1, 4)
        self.surround_heights = None

    def load_model(self):
        pass

    def init_buffer(
        self,
        base_measured_xyz_to_world,
        base_measured_quat_to_world,
        base_measured_xyz_vel_to_world,
        base_measured_rpy_vel_to_world,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
        measured_surround_heights=None,
    ):
        self.base_xyz_to_world[0, 2] = self.base_height_target
        self.base_quat_to_world = base_measured_quat_to_world

        self.joint_measured_position = joint_measured_position_urdf
        self.joint_measured_velocity = joint_measured_velocity_urdf

        self.nn_actor_input_measured_joint_position = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_measured_joint_velocity = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_input_action = torch.zeros(1, self.num_of_joints_controlled)

        self.nn_actor_output_tensor = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output_raw = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_actor_output = torch.zeros(1, self.num_of_joints_controlled)

        self.nn_actor_output_scale = torch.ones(1, self.num_of_joints_controlled) * self.nn_actor_output_scale_factor
        self.nn_actor_output_clip_min = (
            -3.14 * torch.ones(1, self.num_of_joints_controlled) / self.nn_actor_output_scale_factor
        )
        self.nn_actor_output_clip_max = (
            3.14 * torch.ones(1, self.num_of_joints_controlled) / self.nn_actor_output_scale_factor
        )

    def actor_input(
        self,
        base_measured_xyz_to_world,
        base_measured_quat_to_world,
        base_measured_xyz_vel_to_world,
        base_measured_rpy_vel_to_world,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
        measured_surround_heights=None,
    ):
        # do filter or not
        self.base_xyz_to_world = base_measured_xyz_to_world
        self.base_quat_to_world = base_measured_quat_to_world
        self.base_xyz_vel_to_self = base_measured_xyz_vel_to_world
        self.base_rpy_vel_to_self = base_measured_rpy_vel_to_world
        self.joint_measured_position = joint_measured_position_urdf
        self.joint_measured_velocity = joint_measured_velocity_urdf
        self.surround_heights = measured_surround_heights

    def actor_init(self, init_output, commands):
        # prepare variables
        self.gait_clock_time = 0.0

        self.gait_phase = (
            self.gait_clock_time / self.gait_clock_period
            - math.floor(self.gait_clock_time / self.gait_clock_period)
            + self.gait_phase_theta
        )

        self.gait_phase = self.gait_phase - torch.floor(self.gait_phase)

        # 强化学习参数初始化
        # base linear velocity
        self.nn_actor_input_base_linear_velocity = self.base_xyz_vel_to_self

        # base angular velocity
        self.nn_actor_input_base_angular_velocity = self.base_rpy_vel_to_self

        # projected gravity
        self.base_quat_to_world = self.base_quat_to_world
        self.nn_actor_input_base_projected_gravity = torch_quat_rotate_inverse(
            self.base_quat_to_world, self.gravity_vector
        )

        # commands
        self.nn_actor_input_commands = torch.tensor([[0, 0, 0]])
        self.nn_actor_input_commands[0, 0] = torch.clip(
            self.nn_actor_input_commands[0, 0],
            min=self.target_linear_velocity_x_range[0, 0],
            max=self.target_linear_velocity_x_range[0, 1],
        )
        self.nn_actor_input_commands[0, 1] = torch.clip(
            self.nn_actor_input_commands[0, 1],
            min=self.target_linear_velocity_y_range[0, 0],
            max=self.target_linear_velocity_y_range[0, 1],
        )
        self.nn_actor_input_commands[0, 2] = torch.clip(
            self.nn_actor_input_commands[0, 2],
            min=self.target_angular_velocity_range[0, 0],
            max=self.target_angular_velocity_range[0, 1],
        )

        # joint position, joint velocity, action
        self.nn_actor_input_measured_joint_position[0] = (
            self.joint_measured_position[0, self.index_of_joints_controlled]
            - self.joint_default_position[0, self.index_of_joints_controlled]
        )

        self.nn_actor_input_measured_joint_velocity[0] = self.joint_measured_velocity[
            0, self.index_of_joints_controlled
        ]

        self.nn_actor_input_action[0] = (
            init_output[0, self.index_of_joints_controlled]
            - self.joint_default_position[0, self.index_of_joints_controlled]
        ) / self.nn_actor_output_scale

        # gait phase sin, cos, ratio, cycle
        self.nn_actor_input_gait_phase_sin = torch.sin(2 * math.pi * self.gait_phase)
        self.nn_actor_input_gait_phase_cos = torch.cos(2 * math.pi * self.gait_phase)
        self.nn_actor_input_gait_phase_ratio = self.gait_phase_ratio
        self.nn_actor_input_gait_cycle = torch.tensor([[self.gait_clock_period]], dtype=torch.float32)

        # base height offset
        self.nn_actor_input_base_height_offset[0] = self.base_xyz_to_world[0, 2] - self.base_height_target

        # base linear velocity average, base angular velocity average
        self.nn_actor_input_base_linear_velocity_avg = torch.zeros(3)
        self.nn_actor_input_base_angular_velocity_avg = torch.zeros(3)

        # surround heights
        if self.surround_heights is not None:
            self.nn_actor_input_surround_heights_offset = (
                self.base_xyz_to_world[0, 2] - self.base_height_target - self.surround_heights
            )

        # obs
        self.actor_obs()

        # nn

        # prepare nn output
        self.nn_actor_output_scaled = self.nn_actor_output * self.nn_actor_output_scale

        # prepare output
        # copy action input as action output
        self.target_joint_position = self.nn_actor_output_scaled

        joint_pd_control_target = init_output

        return joint_pd_control_target

    def actor_run(self, init_output, commands):
        # calculate gait phase
        self.gait_clock_time += self.gait_clock_dt

        # self.gait_clock_time = 0

        self.gait_phase = (
            self.gait_clock_time / self.gait_clock_period
            - math.floor(self.gait_clock_time / self.gait_clock_period)
            + self.gait_phase_theta
        )

        self.gait_phase = self.gait_phase - torch.floor(self.gait_phase)

        # prepare nn input
        # base linear velocity
        self.nn_actor_input_base_linear_velocity = self.base_xyz_vel_to_self

        # base angular velocity
        self.nn_actor_input_base_angular_velocity = self.base_rpy_vel_to_self

        # projected gravity
        self.base_quat_to_world = self.base_quat_to_world
        self.nn_actor_input_base_projected_gravity = torch_quat_rotate_inverse(
            self.base_quat_to_world, self.gravity_vector
        )

        # commands
        self.nn_actor_input_commands = commands
        self.nn_actor_input_commands[0, 0] = torch.clip(
            self.nn_actor_input_commands[0, 0],
            min=self.target_linear_velocity_x_range[0, 0],
            max=self.target_linear_velocity_x_range[0, 1],
        )
        self.nn_actor_input_commands[0, 1] = torch.clip(
            self.nn_actor_input_commands[0, 1],
            min=self.target_linear_velocity_y_range[0, 0],
            max=self.target_linear_velocity_y_range[0, 1],
        )
        self.nn_actor_input_commands[0, 2] = torch.clip(
            self.nn_actor_input_commands[0, 2],
            min=self.target_angular_velocity_range[0, 0],
            max=self.target_angular_velocity_range[0, 1],
        )

        # joint position, joint velocity, action
        self.nn_actor_input_measured_joint_position[0] = (
            self.joint_measured_position[0, self.index_of_joints_controlled]
            - self.joint_default_position[0, self.index_of_joints_controlled]
        )

        self.nn_actor_input_measured_joint_velocity[0] = self.joint_measured_velocity[
            0, self.index_of_joints_controlled
        ]

        self.nn_actor_input_action = self.nn_actor_input_action

        # gait phase sin, cos, ratio
        self.nn_actor_input_gait_phase_sin = torch.sin(2 * math.pi * self.gait_phase)
        self.nn_actor_input_gait_phase_cos = torch.cos(2 * math.pi * self.gait_phase)
        self.nn_actor_input_gait_phase_ratio = self.gait_phase_ratio

        # base height offset
        self.nn_actor_input_base_height_offset[0] = self.base_xyz_to_world[0, 2] - self.base_height_target

        # base linear velocity average, base angular velocity average
        self.base_linear_velocity_avg = (
            self.base_linear_velocity_avg_factor * self.base_xyz_vel_to_self
            + (1.0 - self.base_linear_velocity_avg_factor) * self.base_linear_velocity_avg
        )

        self.base_angular_velocity_avg = (
            self.base_angular_velocity_avg_factor * self.base_rpy_vel_to_self
            + (1.0 - self.base_angular_velocity_avg_factor) * self.base_angular_velocity_avg
        )

        self.nn_actor_input_base_linear_velocity_avg = self.base_linear_velocity_avg
        self.nn_actor_input_base_angular_velocity_avg = self.base_angular_velocity_avg

        # surround heights
        if self.surround_heights is not None:
            self.nn_actor_input_surround_heights_offset = (
                self.base_xyz_to_world[0, 2] - self.base_height_target - self.surround_heights
            )

        # obs
        self.actor_obs()

        # nn
        self.actor_nn()

        # prepare nn output
        self.nn_actor_output_scaled = self.nn_actor_output * self.nn_actor_output_scale

        # prepare output
        self.target_joint_position = self.nn_actor_output_scaled

        joint_pd_control_target = torch.zeros(1, self.num_of_joints)
        joint_pd_control_target[0] = self.target_joint_position[0, self.index_of_joints_controlled]
        joint_pd_control_target += self.joint_default_position

        return joint_pd_control_target

    def actor_obs(self):
        if self.ac_profile == "GR1T1":
            self.nn_actor_input = torch.cat(
                (
                    self.nn_actor_input_base_linear_velocity,
                    self.nn_actor_input_base_angular_velocity,
                    self.nn_actor_input_base_projected_gravity,
                    self.nn_actor_input_commands,
                    self.nn_actor_input_measured_joint_position,
                    self.nn_actor_input_measured_joint_velocity,
                    self.nn_actor_input_action,
                    self.nn_actor_input_gait_phase_sin,
                    self.nn_actor_input_gait_phase_cos,
                    self.nn_actor_input_gait_phase_ratio,
                    self.nn_actor_input_base_height_offset,
                    self.nn_actor_input_base_linear_velocity_avg,
                    self.nn_actor_input_base_angular_velocity_avg,
                ),
                dim=0,
            )

        else:
            raise Exception("Unknown ac_profile: ", self.ac_profile)

    def actor_nn(self):
        self.nn_actor_output_tensor = self.nn_actor(self.nn_actor_input)

        self.nn_actor_output_raw = self.nn_actor_output_tensor.detach()
        self.nn_actor_output = torch.clip(
            self.nn_actor_output_raw, min=self.nn_actor_output_clip_min, max=self.nn_actor_output_clip_max
        )

        # store nn output
        self.nn_actor_input_action = self.nn_actor_output.clone()

    def run(
        self,
        init_output,
        commands,
        base_measured_xyz_to_world,
        base_measured_quat_to_world,
        base_measured_xyz_vel_to_world,
        base_measured_rpy_vel_to_world,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
        measured_surround_heights=None,
    ):
        # Jason 2024-03-14:
        # use torch.tensor([variables]) to create a tensor with num_envs=1
        torch_init_output = torch.from_numpy(init_output.astype(numpy.float32)).unsqueeze(0)
        torch_commands = torch.from_numpy(commands.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_xyz_to_world = torch.from_numpy(base_measured_xyz_to_world.astype(numpy.float32)).unsqueeze(
            0
        )
        torch_base_measured_quat_to_world = torch.from_numpy(
            base_measured_quat_to_world.astype(numpy.float32)
        ).unsqueeze(0)
        torch_base_measured_xyz_vel_to_world = torch.from_numpy(
            base_measured_xyz_vel_to_world.astype(numpy.float32)
        ).unsqueeze(0)
        torch_base_measured_rpy_vel_to_world = torch.from_numpy(
            base_measured_rpy_vel_to_world.astype(numpy.float32)
        ).unsqueeze(0)
        torch_joint_measured_position_urdf = torch.from_numpy(
            joint_measured_position_urdf.astype(numpy.float32)
        ).unsqueeze(0)
        torch_joint_measured_velocity_urdf = torch.from_numpy(
            joint_measured_velocity_urdf.astype(numpy.float32)
        ).unsqueeze(0)

        if measured_surround_heights is not None:
            torch_measured_surround_heights = torch.from_numpy(
                measured_surround_heights.astype(numpy.float32)
            ).unsqueeze(0)
        else:
            torch_measured_surround_heights = None

        if self.flag_model_inited == FlagState.CLEAR:
            self.load_model()
            self.flag_model_inited = FlagState.SET

        if self.flag_buffer_inited == FlagState.CLEAR:
            self.init_buffer(
                base_measured_xyz_to_world=torch_base_measured_xyz_to_world,
                base_measured_quat_to_world=torch_base_measured_quat_to_world,
                base_measured_xyz_vel_to_world=torch_base_measured_xyz_vel_to_world,
                base_measured_rpy_vel_to_world=torch_base_measured_rpy_vel_to_world,
                joint_measured_position_urdf=torch_joint_measured_position_urdf,
                joint_measured_velocity_urdf=torch_joint_measured_velocity_urdf,
                measured_surround_heights=torch_measured_surround_heights,
            )
            self.flag_buffer_inited = FlagState.SET

        # input filter
        self.actor_input(
            base_measured_xyz_to_world=torch_base_measured_xyz_to_world,
            base_measured_quat_to_world=torch_base_measured_quat_to_world,
            base_measured_xyz_vel_to_world=torch_base_measured_xyz_vel_to_world,
            base_measured_rpy_vel_to_world=torch_base_measured_rpy_vel_to_world,
            joint_measured_position_urdf=torch_joint_measured_position_urdf,
            joint_measured_velocity_urdf=torch_joint_measured_velocity_urdf,
            measured_surround_heights=torch_measured_surround_heights,
        )

        # actor
        if self.flag_actor_inited == FlagState.CLEAR:
            # 初始化神经网络后，需要先执行一次，让神经网络的输出稳定下来
            joint_pd_control_target = self.actor_init(init_output=torch_init_output, commands=torch_commands)
            self.flag_actor_inited = FlagState.SET
        else:
            joint_pd_control_target = self.actor_run(init_output=torch_init_output, commands=torch_commands)

        joint_pd_control_target = joint_pd_control_target.numpy()[0]

        return joint_pd_control_target


class RobotGR1AlgorithmRLACEncoder(RobotGR1AlgorithmRLAC):
    def __init__(self, dt=0.01):
        super().__init__(dt=dt)

        # flags
        self.encoder_profile = "GR1T1"
        self.encoder_output_last = torch.zeros(0)

        self.num_of_joints_leg = 6 + 6
        self.index_of_joints_leg = [
            0,
            1,
            2,
            3,
            4,
            5,  # left leg
            6,
            7,
            8,
            9,
            10,
            11,  # right leg
        ]

        self.nn_encoder_input_base_linear_velocity = torch.tensor([])
        self.nn_encoder_input_base_angular_velocity = torch.tensor([])
        self.nn_encoder_input_base_projected_gravity = torch.tensor([])
        self.nn_encoder_input_measured_joint_position = torch.tensor([])
        self.nn_encoder_input_measured_joint_velocity = torch.tensor([])
        self.nn_encoder_input_measured_leg_joint_position = torch.tensor([])
        self.nn_encoder_input_measured_leg_joint_velocity = torch.tensor([])

        self.nn_encoder_input_history_length = 10
        self.nn_encoder_input_history_base_angular_velocity = torch.tensor([])
        self.nn_encoder_input_history_base_projected_gravity = torch.tensor([])
        self.nn_encoder_input_history_measured_joint_position = torch.tensor([])
        self.nn_encoder_input_history_measured_joint_velocity = torch.tensor([])
        self.nn_encoder_input_history_measured_leg_joint_position = torch.tensor([])
        self.nn_encoder_input_history_measured_leg_joint_velocity = torch.tensor([])

        self.nn_encoder_input = torch.tensor([])

        self.nn_encoder = None

        self.nn_encoder_output_tensor = torch.zeros(0)
        self.nn_encoder_output = torch.tensor([])

    def init_buffer(
        self,
        base_measured_xyz_to_world,
        base_measured_quat_to_world,
        base_measured_xyz_vel_to_world,
        base_measured_rpy_vel_to_world,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
        measured_surround_heights=None,
    ):
        super().init_buffer(
            base_measured_xyz_to_world,
            base_measured_quat_to_world,
            base_measured_xyz_vel_to_world,
            base_measured_rpy_vel_to_world,
            joint_measured_position_urdf,
            joint_measured_velocity_urdf,
            measured_surround_heights=None,
        )

        self.nn_encoder_input_measured_joint_position = torch.zeros(1, self.num_of_joints_controlled)
        self.nn_encoder_input_measured_joint_velocity = torch.zeros(1, self.num_of_joints_controlled)

        self.nn_encoder_input_measured_leg_joint_position = torch.zeros(1, self.num_of_joints_leg)
        self.nn_encoder_input_measured_leg_joint_velocity = torch.zeros(1, self.num_of_joints_leg)

        self.nn_encoder_input_history_base_angular_velocity = torch.zeros(
            1, self.nn_encoder_input_history_length, 3, dtype=torch.float32, requires_grad=False
        )
        self.nn_encoder_input_history_base_projected_gravity = torch.zeros(
            1, self.nn_encoder_input_history_length, 3, dtype=torch.float32, requires_grad=False
        )
        self.nn_encoder_input_history_measured_joint_position = torch.zeros(
            1,
            self.nn_encoder_input_history_length,
            self.num_of_joints_controlled,
            dtype=torch.float32,
            requires_grad=False,
        )
        self.nn_encoder_input_history_measured_joint_velocity = torch.zeros(
            1,
            self.nn_encoder_input_history_length,
            self.num_of_joints_controlled,
            dtype=torch.float32,
            requires_grad=False,
        )
        self.nn_encoder_input_history_measured_leg_joint_position = torch.zeros(
            1, self.nn_encoder_input_history_length, self.num_of_joints_leg, dtype=torch.float32, requires_grad=False
        )
        self.nn_encoder_input_history_measured_leg_joint_velocity = torch.zeros(
            1, self.nn_encoder_input_history_length, self.num_of_joints_leg, dtype=torch.float32, requires_grad=False
        )

    def encoder_run(
        self,
        base_measured_xyz_to_world,
        base_measured_quat_to_world,
        base_measured_xyz_vel_to_world,
        base_measured_rpy_vel_to_world,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
    ):
        # prepare nn input
        # base linear velocity
        self.nn_encoder_input_base_linear_velocity = base_measured_xyz_vel_to_world

        # base angular velocity
        self.nn_encoder_input_base_angular_velocity = base_measured_rpy_vel_to_world

        # projected gravity
        self.base_quat_to_world = self.base_quat_to_world
        self.nn_encoder_input_base_projected_gravity = torch_quat_rotate_inverse(
            self.base_quat_to_world, self.gravity_vector
        )

        # joint position, joint velocity (controlled)
        self.nn_encoder_input_measured_joint_position[0] = (
            self.joint_measured_position[0, self.index_of_joints_controlled]
            - self.joint_default_position[0, self.index_of_joints_controlled]
        )

        self.nn_encoder_input_measured_joint_velocity[0] = self.joint_measured_velocity[
            0, self.index_of_joints_controlled
        ]

        # joint position, joint velocity (leg)
        self.nn_encoder_input_measured_leg_joint_position[0] = (
            self.joint_measured_position[0, self.index_of_joints_leg]
            - self.joint_default_position[0, self.index_of_joints_leg]
        )

        self.nn_encoder_input_measured_leg_joint_velocity[0] = self.joint_measured_velocity[0, self.index_of_joints_leg]

        # history
        self.encoder_history()

        # obs
        self.encoder_obs()

        # nn
        self.encoder_nn()

        return self.nn_encoder_output

    def encoder_history(self):
        self.nn_encoder_input_history_base_angular_velocity = torch.cat(
            (
                self.nn_encoder_input_history_base_angular_velocity[:, 1:],
                self.nn_encoder_input_base_angular_velocity.unsqueeze(1),
            ),
            dim=1,
        )

        self.nn_encoder_input_history_base_projected_gravity = torch.cat(
            (
                self.nn_encoder_input_history_base_projected_gravity[:, 1:],
                self.nn_encoder_input_base_projected_gravity.unsqueeze(1),
            ),
            dim=1,
        )

        self.nn_encoder_input_history_measured_joint_position = torch.cat(
            (
                self.nn_encoder_input_history_measured_joint_position[:, 1:],
                self.nn_encoder_input_measured_joint_position.unsqueeze(1),
            ),
            dim=1,
        )

        self.nn_encoder_input_history_measured_joint_velocity = torch.cat(
            (
                self.nn_encoder_input_history_measured_joint_velocity[:, 1:],
                self.nn_encoder_input_measured_joint_velocity.unsqueeze(1),
            ),
            dim=1,
        )

        self.nn_encoder_input_history_measured_leg_joint_position = torch.cat(
            (
                self.nn_encoder_input_history_measured_leg_joint_position[:, 1:],
                self.nn_encoder_input_measured_leg_joint_position.unsqueeze(1),
            ),
            dim=1,
        )

        self.nn_encoder_input_history_measured_leg_joint_velocity = torch.cat(
            (
                self.nn_encoder_input_history_measured_leg_joint_velocity[:, 1:],
                self.nn_encoder_input_measured_leg_joint_velocity.unsqueeze(1),
            ),
            dim=1,
        )

    def encoder_obs(self):
        if self.encoder_profile == "GR1T1-blv-bho":
            self.nn_encoder_input = torch.cat(
                (
                    self.nn_encoder_input_base_angular_velocity,
                    self.nn_encoder_input_base_projected_gravity,
                    self.nn_encoder_input_measured_leg_joint_position,
                    self.nn_encoder_input_measured_leg_joint_velocity,
                ),
                dim=-1,
            )

        else:
            raise Exception("Unknown encoder_profile: ", self.encoder_profile)

    def encoder_nn(self):
        # encoder
        self.nn_encoder_output_tensor = self.nn_encoder(self.nn_encoder_input)

        # self.nn_encoder_output_tensor = \
        #     torch.from_torch(torch.random.rand(4))

        self.nn_encoder_output = self.nn_encoder_output_tensor.detach()

    def run(
        self,
        init_output,
        commands,
        base_measured_xyz_to_world,
        base_measured_quat_to_world,
        base_measured_xyz_vel_to_world,
        base_measured_rpy_vel_to_world,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
        measured_surround_heights=None,
    ):
        # Jason 2024-03-14:
        # use torch.tensor([variables]) to create a tensor with num_envs=1
        torch_init_output = torch.from_numpy(init_output.astype(numpy.float32)).unsqueeze(0)
        torch_commands = torch.from_numpy(commands.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_xyz_to_world = torch.from_numpy(base_measured_xyz_to_world.astype(numpy.float32)).unsqueeze(
            0
        )
        torch_base_measured_quat_to_world = torch.from_numpy(
            base_measured_quat_to_world.astype(numpy.float32)
        ).unsqueeze(0)
        torch_base_measured_xyz_vel_to_world = torch.from_numpy(
            base_measured_xyz_vel_to_world.astype(numpy.float32)
        ).unsqueeze(0)
        torch_base_measured_rpy_vel_to_world = torch.from_numpy(
            base_measured_rpy_vel_to_world.astype(numpy.float32)
        ).unsqueeze(0)
        torch_joint_measured_position_urdf = torch.from_numpy(
            joint_measured_position_urdf.astype(numpy.float32)
        ).unsqueeze(0)
        torch_joint_measured_velocity_urdf = torch.from_numpy(
            joint_measured_velocity_urdf.astype(numpy.float32)
        ).unsqueeze(0)

        if measured_surround_heights is not None:
            torch_measured_surround_heights = torch.from_numpy(
                measured_surround_heights.astype(numpy.float32)
            ).unsqueeze(0)
        else:
            torch_measured_surround_heights = None

        if self.flag_model_inited == FlagState.CLEAR:
            self.load_model()
            self.flag_model_inited = FlagState.SET

        if self.flag_buffer_inited == FlagState.CLEAR:
            self.init_buffer(
                base_measured_xyz_to_world=torch_base_measured_xyz_to_world,
                base_measured_quat_to_world=torch_base_measured_quat_to_world,
                base_measured_xyz_vel_to_world=torch_base_measured_xyz_vel_to_world,
                base_measured_rpy_vel_to_world=torch_base_measured_rpy_vel_to_world,
                joint_measured_position_urdf=torch_joint_measured_position_urdf,
                joint_measured_velocity_urdf=torch_joint_measured_velocity_urdf,
                measured_surround_heights=torch_measured_surround_heights,
            )
            self.flag_buffer_inited = FlagState.SET

        # encoder
        encoder_output_raw = self.encoder_run(
            base_measured_xyz_to_world=torch_base_measured_xyz_to_world,
            base_measured_quat_to_world=torch_base_measured_quat_to_world,
            base_measured_xyz_vel_to_world=torch_base_measured_xyz_vel_to_world,
            base_measured_rpy_vel_to_world=torch_base_measured_rpy_vel_to_world,
            joint_measured_position_urdf=torch_joint_measured_position_urdf,
            joint_measured_velocity_urdf=torch_joint_measured_velocity_urdf,
        )

        # encoder filter
        encoder_output = encoder_output_raw.clone()
        self.encoder_output_last = encoder_output

        # Jason 2024-02-04:
        # 一旦使用了 encoder，可能就反而不能使用仿真器的“真实”数据了，
        # 因为仿真器与仿真器之间可能存在不同，而 actor 训练时是基于训练用的仿真器的数据的。
        # 所以，如果使用了 encoder，可能就不能使用另外的仿真器的数据了。

        # encoder -> measured
        # if self.encoder_profile == "GR1T1-blv-bho" or \
        #         self.encoder_profile == "GR1T1-history-blv-bho":
        #     torch_base_measured_xyz_vel_to_world[:, 0:3] = encoder_output[:, 0:3]
        #     torch_base_measured_xyz_to_world[:, 2] = encoder_output[:, 3] + self.base_height_target

        # input filter
        self.actor_input(
            base_measured_xyz_to_world=torch_base_measured_xyz_to_world,
            base_measured_quat_to_world=torch_base_measured_quat_to_world,
            base_measured_xyz_vel_to_world=torch_base_measured_xyz_vel_to_world,
            base_measured_rpy_vel_to_world=torch_base_measured_rpy_vel_to_world,
            joint_measured_position_urdf=torch_joint_measured_position_urdf,
            joint_measured_velocity_urdf=torch_joint_measured_velocity_urdf,
            measured_surround_heights=torch_measured_surround_heights,
        )

        # actor
        if self.flag_actor_inited == FlagState.CLEAR:
            # 初始化神经网络后，需要先执行一次，让神经网络的输出稳定下来
            joint_pd_control_target = self.actor_init(init_output=torch_init_output, commands=torch_commands)
            self.flag_actor_inited = FlagState.SET
        else:
            joint_pd_control_target = self.actor_run(init_output=torch_init_output, commands=torch_commands)

        joint_pd_control_target = joint_pd_control_target.numpy()[0]
        encoder_output = encoder_output.numpy()[0]
        encoder_output_raw = encoder_output_raw.numpy()[0]

        return joint_pd_control_target, encoder_output, encoder_output_raw
