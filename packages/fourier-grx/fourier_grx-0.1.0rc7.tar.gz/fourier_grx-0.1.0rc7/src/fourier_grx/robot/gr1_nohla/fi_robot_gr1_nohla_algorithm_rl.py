import math
import os
import time

import numpy
import torch

from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_task_stage import TaskStage
from fourier_core.rl.rl_robot_tool import torch_quat_rotate_inverse

from fourier_grx.robot.gr1_nohla.fi_robot_gr1_nohla_algorithm import RobotGR1NohlaAlgorithmBasicControlModel
from fourier_grx.tools.low_pass_filter import LowPassFilterTorch


# fmt: off

class RobotGR1NohlaAlgorithmRLWalkControlModel(RobotGR1NohlaAlgorithmBasicControlModel):
    def __init__(
            self,
            dt: float = 0.01,
            decimation: int = 1,
            warmup_period=1.0,
            actor_model_file_path=None,
            encoder_model_file_path=None,
    ):
        """
        Nohla (No head, lower arm control) RL walk control algorithm.

        Input:
        - dt: time step, s
        - decimation: decimation factor
        - warmup_period: warm up period, s
        - actor_model_file_path: actor model file path
        - encoder_model_file_path: encoder model file path
        """
        super().__init__()

        # --------------------------------------------------------------------
        # dt and decimation
        self.dt: float = dt
        self.decimation: int = int(decimation)
        self.decimation_count: int = 0

        # --------------------------------------------------------------------
        # warm up
        self.warmup_period: float = warmup_period
        self.warmup_start_time: float | None = None

        # --------------------------------------------------------------------
        # model file path
        self.actor_model_file_path: str | None = actor_model_file_path
        self.encoder_model_file_path: str | None = encoder_model_file_path

        # --------------------------------------------------------------------
        # real robot
        self.num_of_joints = 6 + 6 + 3 + 4 + 4

        self.flag_joint_pd_torque_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)

        self.index_of_joints_real_robot = numpy.array(
            [
                0, 1, 2, 3, 4, 5,  # left leg
                6, 7, 8, 9, 10, 11,  # right leg
                12, 13, 14,  # waist
                18, 19, 20, 21,  # left arm
                25, 26, 27, 28,  # right arm
            ]
        )
        self.pd_control_kp_real_robot = numpy.array(
            [
                251.625, 362.5214, 200, 200, 10.9805, 10.9805,  # left leg
                251.625, 362.5214, 200, 200, 10.9805, 10.9805,  # right leg
                362.5214, 362.5214, 362.5214,  # waist
                92.85, 92.85, 112.06, 112.06,  # left arm
                92.85, 92.85, 112.06, 112.06,  # right arm
            ]
        )
        self.pd_control_kd_real_robot = numpy.array(
            [
                14.72, 10.0833, 11, 11, 0.5991, 0.5991,  # left leg
                14.72, 10.0833, 11, 11, 0.5991, 0.5991,  # right leg
                10.0833, 10.0833, 10.0833,  # waist
                2.575, 2.575, 3.1, 3.1,  # left arm
                2.575, 2.575, 3.1, 3.1,  # right arm
            ]
        )

        # --------------------------------------------------------------------

        self.num_of_joints_controlled = 6 + 6 + 3 + 4 + 4
        self.index_of_joints_controlled = numpy.array(
            [
                0, 1, 2, 3, 4, 5,  # left leg
                6, 7, 8, 9, 10, 11,  # right leg
                12, 13, 14,  # waist
                15, 16, 17, 18,  # left arm
                19, 20, 21, 22,  # right arm
            ]
        )
        self.joint_default_position = numpy.array(
            [
                0.0, 0.0, -0.5236, 1.0472, -0.5236, 0.0,  # left leg (6)
                0.0, 0.0, -0.5236, 1.0472, -0.5236, 0.0,  # right leg (6)
                0.0, 0.0, 0.0,  # waist (3)
                0.0, 0.3, 0.0, -0.3,  # left arm (4)
                0.0, -0.3, 0.0, -0.3,  # right arm (4)
            ]
        )
        self.joint_default_position_tensor = torch.tensor(
            [
                [
                    0.0, 0.0, -0.5236, 1.0472, -0.5236, 0.0,  # left leg (6)
                    0.0, 0.0, -0.5236, 1.0472, -0.5236, 0.0,  # right leg (6)
                    0.0, 0.0, 0.0,  # waist (3)
                    0.0, 0.3, 0.0, -0.3,  # left arm (4)
                    0.0, -0.3, 0.0, -0.3,  # right arm (4)
                ]
            ],
            dtype=torch.float32,
        )

        self.nn_obs_scale_lin_vel = 2.00
        self.nn_obs_scale_ang_vel = 0.25
        self.nn_obs_scale_command = torch.tensor(
            [[self.nn_obs_scale_lin_vel, self.nn_obs_scale_lin_vel, self.nn_obs_scale_ang_vel]]
        )
        self.nn_obs_scale_gravity = 1.00
        self.nn_obs_scale_dof_pos = 1.00
        self.nn_obs_scale_dof_vel = 0.05
        self.nn_obs_scale_height = 5.00
        self.nn_act_scale_action = 0.50

        # --------------------------------------------------------------------
        # env
        self.num_envs = 1
        self.device = torch.device("cpu")

        # actor
        self.num_actor_obs = 321
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

        self.gait_clock_time = 0.0
        self.gait_clock_dt = self.dt * self.decimation
        self.gait_clock_period = 0.7
        self.gait_phase = torch.tensor([[0.0, 0.0]])
        self.gait_phase_ratio_stand = torch.tensor([[0.0, 0.0]])
        self.gait_phase_ratio_walk = torch.tensor([[0.35, 0.35]])
        self.gait_phase_ratio = self.gait_phase_ratio_walk
        self.gait_phase_theta = torch.tensor([[0.35, 0.85]])

        self.base_height_target = 0.85
        self.gravity_vector = torch.tensor([[0.0, 0.0, -1.0]])
        self.base_quat_to_world = torch.tensor([[0.0, 0.0, 0.0, 1.0]])

        self.base_linear_velocity_avg = torch.tensor([[0.0, 0.0, 0.0]])
        self.base_angular_velocity_avg = torch.tensor([[0.0, 0.0, 0.0]])
        self.base_linear_velocity_avg_factor = torch.tensor([[0.0, 0.0, 0.0]])
        self.base_angular_velocity_avg_factor = torch.tensor([[0.0, 0.0, 0.0]])

        self.base_linear_velocity_avg_factor[0, 0] = 2 * self.gait_clock_dt / self.gait_clock_period
        self.base_linear_velocity_avg_factor[0, 1] = 1 * self.gait_clock_dt / self.gait_clock_period
        self.base_angular_velocity_avg_factor[0, 2] = 1 * self.gait_clock_dt / self.gait_clock_period

        self.nn_actor = None
        self._init_actor()

        # --------------------------------------------------------------------
        # encoder
        self.flag_use_encoder = FlagState.SET
        self.num_encoder_obs = 3600
        self.num_encoder_out = 4

        self.nn_encoder = None
        self._init_encoder()

        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # input
        self.base_xyz_vel_to_self = torch.zeros(self.num_envs, 3)
        self.base_rpy_vel_to_self = torch.zeros(self.num_envs, 3)
        self.base_xyz_to_world = torch.zeros(self.num_envs, 3)
        self.base_quat_to_world = torch.zeros(self.num_envs, 4)
        self.base_project_gravity = torch.zeros(self.num_envs, 3)

        # Jason 2024-07-07:
        # cut-off frequency lower than 30hz may not work well
        self.filter_for_base_lin_vel = LowPassFilterTorch(
            cutoff_freq=30, damping_ratio=0.707, dt=self.dt * self.decimation, shape=(self.num_envs, 3)
        )
        self.filter_for_base_ang_vel = LowPassFilterTorch(
            cutoff_freq=30, damping_ratio=0.707, dt=self.dt * self.decimation, shape=(self.num_envs, 3)
        )
        self.filter_for_dof_pos = LowPassFilterTorch(
            cutoff_freq=30, damping_ratio=0.707, dt=self.dt * self.decimation, shape=(self.num_envs, 23)
        )
        self.filter_for_dof_vel = LowPassFilterTorch(
            cutoff_freq=50, damping_ratio=0.707, dt=self.dt * self.decimation, shape=(self.num_envs, 23)
        )
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # output
        self.target_joint_position_offset = torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.target_joint_position = torch.zeros(self.num_envs, self.num_of_joints_controlled)
        # --------------------------------------------------------------------

    def _init_actor(self):
        self.nn_actor_input_base_linear_velocity = \
            torch.zeros(self.num_envs, 3)
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
        self.nn_actor_input_gait_phase_sin = \
            torch.zeros(self.num_envs, 2)
        self.nn_actor_input_gait_phase_cos = \
            torch.zeros(self.num_envs, 2)
        self.nn_actor_input_gait_phase_ratio = \
            torch.zeros(self.num_envs, 2)
        self.nn_actor_input_gait_cycle = \
            torch.tensor([[self.gait_clock_period]], dtype=torch.float32)
        self.nn_actor_input_base_height_offset = \
            torch.zeros(self.num_envs, 1)
        self.nn_actor_input_base_linear_velocity_avg = \
            torch.zeros(self.num_envs, 3)
        self.nn_actor_input_base_angular_velocity_avg = \
            torch.zeros(self.num_envs, 3)
        self.nn_actor_input_history_length = 5
        self.nn_actor_input_history_measured_joint_position_offset = \
            torch.zeros(self.num_envs, self.nn_actor_input_history_length * self.num_of_joints_controlled)
        self.nn_actor_input_history_measured_joint_velocity = \
            torch.zeros(self.num_envs, self.nn_actor_input_history_length * self.num_of_joints_controlled)
        self.nn_actor_input_length = \
            self.num_actor_obs
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
        self.nn_actor_output_clip_min = \
            -100 * torch.ones(self.num_envs, self.num_actor_act)
        self.nn_actor_output_clip_max = \
            100 * torch.ones(self.num_envs, self.num_actor_act)

    def _init_encoder(self):
        self.nn_encoder_input_measured_joint_position_offset = \
            torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.nn_encoder_input_measured_joint_velocity = \
            torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.nn_encoder_input_action = \
            torch.zeros(self.num_envs, self.num_of_joints_controlled)
        self.nn_encoder_input_base_projected_gravity = \
            torch.zeros(self.num_envs, 3)
        self.nn_encoder_input = \
            torch.zeros(self.num_envs, self.num_encoder_obs)

        self.nn_encoder_output_tensor = \
            torch.zeros(self.num_envs, self.num_encoder_out)
        self.nn_encoder_output = \
            torch.zeros(self.num_envs, self.num_encoder_out)

    def _load_actor(self):
        if self.nn_actor is None:
            if self.actor_model_file_path is None:
                model_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               "actor.pt")
            else:
                model_file_path = self.actor_model_file_path

            try:
                self.nn_actor = torch.jit.load(model_file_path, map_location=self.device)
            except Exception as exp:
                print(f"Load actor model error: {exp}")
                self.nn_actor = None

        # script_model = torch.jit.load(model_file_path, map_location=torch.device('cpu'))
        # self.nn_actor = torch.jit.optimize_for_inference(script_model)

    def _load_encoder(self):
        if self.nn_encoder is None:
            if self.encoder_model_file_path is None:
                model_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               "encoder.pt")
            else:
                model_file_path = self.encoder_model_file_path

            try:
                self.nn_encoder = torch.jit.load(model_file_path, map_location=self.device)
            except Exception as exp:
                print(f"Load encoder model error: {exp}")
                self.nn_encoder = None

        # script_model = torch.jit.load(model_file_path, map_location=torch.device('cpu'))
        # self.nn_encoder = torch.jit.optimize_for_inference(script_model)

    def _init_buffer(self, init_output):
        self.base_xyz_to_world[0, 2] = self.base_height_target

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

        # self.measured_joint_velocity = joint_measured_velocity_urdf
        self.measured_joint_velocity = self.filter_for_dof_vel.filter(joint_measured_velocity_urdf)

    def _actor_input(self, base_measured_xyz_to_world, base_measured_xyz_vel_to_self):
        # do filter or not
        self.base_xyz_to_world = base_measured_xyz_to_world
        self.base_xyz_vel_to_self = base_measured_xyz_vel_to_self

    def _actor_run(self):
        # prepare
        self._actor_prepare()

        # obs
        self._actor_obs()

        # nn
        self._actor_nn()

        # history
        self._actor_history()

        # output
        self._actor_output()

        return self.target_joint_position

    def _actor_prepare(self):
        # calculate gait phase
        self.gait_phase = \
            (self.gait_clock_time / self.gait_clock_period + self.gait_phase_theta) \
            - torch.floor(self.gait_clock_time / self.gait_clock_period + self.gait_phase_theta)

        self.gait_clock_time += self.gait_clock_dt

        # base linear velocity
        self.nn_actor_input_base_linear_velocity = self.base_xyz_vel_to_self

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

        # gait phase sin, cos, ratio, cycle
        self.nn_actor_input_gait_phase_sin = torch.sin(2 * math.pi * self.gait_phase)

        self.nn_actor_input_gait_phase_cos = torch.cos(2 * math.pi * self.gait_phase)

        self.nn_actor_input_gait_phase_ratio = self.gait_phase_ratio

        # base height offset
        self.nn_actor_input_base_height_offset[0] = torch.clip(
            self.base_xyz_to_world[0, 2] - self.base_height_target, min=-1, max=1
        )

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

    def _actor_obs(self):
        self.nn_actor_input = torch.cat(
            (
                # base related
                self.nn_actor_input_base_linear_velocity * self.nn_obs_scale_lin_vel,
                self.nn_actor_input_base_angular_velocity * self.nn_obs_scale_ang_vel,
                self.nn_actor_input_base_projected_gravity * self.nn_obs_scale_gravity,
                self.nn_actor_input_commands * self.nn_obs_scale_command,
                # dof related
                self.nn_actor_input_measured_joint_position_offset * self.nn_obs_scale_dof_pos,
                self.nn_actor_input_measured_joint_velocity * self.nn_obs_scale_dof_vel,
                self.nn_actor_input_action,
                # gait related
                self.nn_actor_input_gait_phase_sin,
                self.nn_actor_input_gait_phase_cos,
                self.nn_actor_input_gait_phase_ratio,
                # others
                self.nn_actor_input_base_height_offset * self.nn_obs_scale_height,
                self.nn_actor_input_base_linear_velocity_avg[:, 0:2] * self.nn_obs_scale_lin_vel,
                self.nn_actor_input_base_angular_velocity_avg[:, 2:] * self.nn_obs_scale_ang_vel,
                self.nn_actor_input_history_measured_joint_position_offset * self.nn_obs_scale_dof_pos,
                self.nn_actor_input_history_measured_joint_velocity * self.nn_obs_scale_dof_vel,
            ),
            dim=1,
        )

    def _actor_nn(self):
        self.nn_actor_output_tensor = self.nn_actor(self.nn_actor_input)

        self.nn_actor_output_raw = self.nn_actor_output_tensor.detach()

        self.nn_actor_output = torch.clip(
            self.nn_actor_output_raw,
            min=self.nn_actor_output_clip_min,
            max=self.nn_actor_output_clip_max
        )

    def _actor_history(self):
        self.nn_actor_input_history_measured_joint_position_offset = torch.cat(
            (
                self.nn_actor_input_history_measured_joint_position_offset[:, self.num_of_joints_controlled:],
                self.nn_actor_input_measured_joint_position_offset,
            ),
            dim=1,
        )
        self.nn_actor_input_history_measured_joint_velocity = torch.cat(
            (
                self.nn_actor_input_history_measured_joint_velocity[:, self.num_of_joints_controlled:],
                self.nn_actor_input_measured_joint_velocity,
            ),
            dim=1,
        )

    def _actor_output(self):
        self.target_joint_position_offset = \
            self.nn_actor_output * self.nn_actor_output_scale

        self.target_joint_position = \
            self.target_joint_position_offset + self.joint_default_position_tensor

    def _encoder_run(self):
        # prepare
        self._encoder_prepare()

        # obs
        self._encoder_obs()

        # nn
        self._encoder_nn()

        # output
        self._encoder_output()

        return self.nn_encoder_output

    def _encoder_prepare(self):
        # measured joint position offset, velocity
        self.nn_encoder_input_measured_joint_position_offset[0] = self.measured_joint_position_offset[
            0, self.index_of_joints_controlled
        ]

        self.nn_encoder_input_measured_joint_velocity[0] = self.measured_joint_velocity[
            0, self.index_of_joints_controlled
        ]

        # actions
        self.nn_encoder_input_action[0] = self.nn_actor_output

        # projected gravity
        self.nn_encoder_input_base_projected_gravity = self.base_project_gravity

    def _encoder_obs(self):
        self.nn_encoder_input = torch.cat(
            (
                self.nn_encoder_input[:, self.num_of_joints_controlled * 3 + 3:],
                self.nn_encoder_input_measured_joint_position_offset * self.nn_obs_scale_dof_pos,
                self.nn_encoder_input_measured_joint_velocity * self.nn_obs_scale_dof_vel,
                self.nn_encoder_input_action,
                self.nn_encoder_input_base_projected_gravity * self.nn_obs_scale_gravity,
            ),
            dim=1,
        )

    def _encoder_nn(self):
        # encoder
        self.nn_encoder_output_tensor = self.nn_encoder(self.nn_encoder_input)

    def _encoder_output(self):
        self.nn_encoder_output = self.nn_encoder_output_tensor.detach()

    def run(
            self,
            joint_measured_position_urdf,
            joint_measured_velocity_urdf,
            init_output=None,
            commands=numpy.array([0, 0, 0]),
            base_measured_xyz_to_world=numpy.array([0, 0, 0]),
            base_measured_quat_to_world=numpy.array([0, 0, 0, 1]),
            base_measured_xyz_vel_to_self=numpy.array([0, 0, 0]),
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
            # run neural network to warm up, all inputs are zero
            self._load_actor()
            self._load_encoder()

            self.nn_actor(self.nn_actor_input)
            self.nn_encoder(self.nn_encoder_input)

            if self.warmup_start_time is None:
                self.warmup_start_time = time.time()

            if time.time() - self.warmup_start_time >= self.warmup_period:
                self._init_actor()
                self._init_encoder()
                self.stage = TaskStage.STAGE_RUN
                print("Warmup done. Running algorithm...")

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
            init_output = numpy.zeros(self.num_actor_act)
        torch_init_output = \
            torch.from_numpy(init_output.astype(numpy.float32)).unsqueeze(0)

        torch_commands = \
            torch.from_numpy(commands.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_xyz_to_world = \
            torch.from_numpy(base_measured_xyz_to_world.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_quat_to_world = \
            torch.from_numpy(base_measured_quat_to_world.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_xyz_vel_to_self = \
            torch.from_numpy(base_measured_xyz_vel_to_self.astype(numpy.float32)).unsqueeze(0)
        torch_base_measured_rpy_vel_to_self = \
            torch.from_numpy(base_measured_rpy_vel_to_self.astype(numpy.float32)).unsqueeze(0)
        torch_joint_measured_position_urdf = \
            torch.from_numpy(joint_measured_position_urdf.astype(numpy.float32)).unsqueeze(0)
        torch_joint_measured_velocity_urdf = \
            torch.from_numpy(joint_measured_velocity_urdf.astype(numpy.float32)).unsqueeze(0)

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
        # encoder
        if self.flag_use_encoder == FlagState.SET:
            encoder_output = self._encoder_run()

            # encoder -> measured
            torch_base_measured_xyz_vel_to_self[:, 0] = encoder_output[:, 0] / self.nn_obs_scale_lin_vel
            torch_base_measured_xyz_vel_to_self[:, 1] = encoder_output[:, 1] / self.nn_obs_scale_lin_vel
            torch_base_measured_xyz_vel_to_self[:, 2] = encoder_output[:, 2] / self.nn_obs_scale_lin_vel
            torch_base_measured_xyz_to_world[:, 2] = (
                    encoder_output[:, 3] / self.nn_obs_scale_height + self.base_height_target
            )
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # actor
        self._actor_input(
            base_measured_xyz_to_world=torch_base_measured_xyz_to_world,
            base_measured_xyz_vel_to_self=torch_base_measured_xyz_vel_to_self,
        )

        target_joint_position = self._actor_run()
        target_joint_position = target_joint_position.numpy()[0]
        # --------------------------------------------------------------------

        return target_joint_position

# fmt: on
