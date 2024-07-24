import os

import numpy
import torch
from fourier_core.logger.fi_logger import Logger
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.rl.rl_actor_critic_mlp import ActorCriticMLP
from fourier_core.rl.rl_encoder import Encoder
from fourier_grx.robot.gr1.fi_robot_gr1_algorithm_rl import RobotGR1AlgorithmRLACEncoder


class RobotGR1NowhlaAlgorithmRLACEncoder(RobotGR1AlgorithmRLACEncoder):
    def __init__(self, dt=0.01):
        super().__init__(dt=dt)

        # robot model
        self.num_of_joints = 6 + 6 + 4 + 4
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
                    0.2,
                    0.0,
                    -0.3,  # left arm (4)
                    0.0,
                    -0.2,
                    0.0,
                    -0.3,  # right arm (4)
                ]
            ]
        )

        self.num_of_joints_controlled = 6 + 6 + 4 + 4
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
                14,
                15,  # left arm
                16,
                17,
                18,
                19,  # right arm
            ]
        )

        self.index_of_joints_real = torch.tensor(
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
                18,
                19,
                20,
                21,  # left arm
                25,
                26,
                27,
                28,  # right arm
            ]
        )

        self.flag_joint_pd_position_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_pd_torque_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_velocity_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_kinetic_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)

        # numpy -> torch
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
                    0.2,
                    0.0,
                    -0.3,  # left arm (4)
                    0.0,
                    -0.2,
                    0.0,
                    -0.3,  # right arm (4)
                ]
            ],
            dtype=torch.float32,
        )


class RobotGR1NowhlaAlgorithmRLWalkEncoderControlModel(RobotGR1NowhlaAlgorithmRLACEncoder):
    def __init__(self, dt=0.01):
        super().__init__(dt=dt)

        # actor-critic
        # self.ac_profile = "GR1T1-walk"
        self.ac_profile = "GR1T1-walk-pri"
        self.base_height_target = 0.90

        # input variables
        self.input_filter_factor_base_xyz_to_world = 1.0  # 4Hz
        self.input_filter_factor_base_quat_to_world = 1.0  # 4Hz
        self.input_filter_factor_base_xyz_vel_to_self = 1.0  # 10Hz
        self.input_filter_factor_base_rpy_vel_to_self = 1.0  # 10Hz
        self.input_filter_factor_joint_measured_position_value = 1.0  # 10Hz
        self.input_filter_factor_joint_measured_velocity_value = 1.0  # 10Hz

        # encoder
        # self.encoder_profile = "GR1T1-blv-bho"
        self.encoder_profile = "GR1T1-history-blv-bho"
        self.nn_encoder_input_history_length = 5
        self.encoder_output_last = torch.zeros(1, 4)

        self.encoder_filter_factor_base_lin_vel_x = 1.0  # 15Hz
        self.encoder_filter_factor_base_lin_vel_y = 1.0  # 15Hz
        self.encoder_filter_factor_base_lin_vel_z = 1.0  # 15Hz
        self.encoder_filter_factor_base_height_offset = 1.0  # 15Hz

    def load_model(self):
        # nerual network
        try:
            self.model_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_3500.pt")
            # print("model_file_path: ", self.model_file_path)

            model = torch.load(self.model_file_path, map_location=torch.device("cpu"))
            model_actor_dict = model["model_state_dict"]

            self.nn_actor = ActorCriticMLP(
                num_actor_obs=80,
                num_critic_obs=521,
                num_actions=self.num_of_joints_controlled,
                actor_hidden_dims=[512, 256, 128],
                critic_hidden_dims=[512, 256, 128],
            )
            # ActorCriticMLP(num_actor_obs=67,
            #                num_critic_obs=67,
            #                num_actions=self.num_of_joints_controlled,
            #                actor_hidden_dims=[512, 256, 128],
            #                critic_hidden_dims=[512, 256, 128])

            self.nn_actor.load_state_dict(model_actor_dict)

            model_encoder_dict = model["encoder_state_dict"]

            self.nn_encoder = Encoder(num_encoder_obs=30 * 5, num_encoder_out=4, encoder_hidden_dims=[512, 256, 128])
            # Encoder(num_encoder_obs=30,
            #         num_encoder_out=4,
            #         encoder_hidden_dims=[512, 256, 128])

            self.nn_encoder.load_state_dict(model_encoder_dict)

        except Exception as e:
            Logger().print_trace_warning(e)

    def actor_obs(self):
        if self.ac_profile == "GR1T1-walk":
            self.nn_actor_input = torch.cat(
                (
                    # unobservable proprioception
                    self.nn_actor_input_base_linear_velocity,
                    self.nn_actor_input_base_height_offset,
                    # base related
                    self.nn_actor_input_base_angular_velocity,
                    self.nn_actor_input_base_projected_gravity,
                    self.nn_actor_input_commands,
                    # dof related
                    self.nn_actor_input_measured_joint_position,
                    self.nn_actor_input_measured_joint_velocity,
                    self.nn_actor_input_action,
                    # phase related
                    self.nn_actor_input_gait_phase_sin,
                    self.nn_actor_input_gait_phase_cos,
                    self.nn_actor_input_gait_phase_ratio,
                    self.nn_actor_input_gait_cycle,
                    # avg related
                    self.nn_actor_input_base_linear_velocity_avg,
                    self.nn_actor_input_base_angular_velocity_avg,
                ),
                dim=-1,
            )

        elif self.ac_profile == "GR1T1-walk-pri":
            self.nn_actor_input = torch.cat(
                (
                    # unobservable proprioception
                    self.nn_actor_input_base_linear_velocity,
                    self.nn_actor_input_base_height_offset,
                    # base related
                    self.nn_actor_input_base_angular_velocity,
                    self.nn_actor_input_base_projected_gravity,
                    self.nn_actor_input_commands,
                    # dof related
                    self.nn_actor_input_measured_joint_position,
                    self.nn_actor_input_measured_joint_velocity,
                    self.nn_actor_input_action,
                    # phase related
                    self.nn_actor_input_gait_phase_sin,
                    self.nn_actor_input_gait_phase_cos,
                    self.nn_actor_input_gait_phase_ratio,
                    self.nn_actor_input_gait_cycle,
                ),
                dim=-1,
            )

        else:
            raise Exception("Unknown ac_profile: ", self.ac_profile)

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

        elif self.encoder_profile == "GR1T1-history-blv-bho":
            self.nn_encoder_input = torch.cat(
                (
                    self.nn_encoder_input_history_base_angular_velocity.view(
                        self.nn_encoder_input_history_base_angular_velocity.shape[0], -1
                    ),
                    self.nn_encoder_input_history_base_projected_gravity.view(
                        self.nn_encoder_input_history_base_projected_gravity.shape[0], -1
                    ),
                    self.nn_encoder_input_history_measured_leg_joint_position.view(
                        self.nn_encoder_input_history_measured_leg_joint_position.shape[0], -1
                    ),
                    self.nn_encoder_input_history_measured_leg_joint_velocity.view(
                        self.nn_encoder_input_history_measured_leg_joint_velocity.shape[0], -1
                    ),
                ),
                dim=-1,
            )

        else:
            raise Exception("Unknown encoder_profile: ", self.encoder_profile)

    def encoder_output_filter(self, encoder_output):
        encoder_output_filtered = torch.zeros_like(encoder_output)

        encoder_output_filtered[0, 0] = (
            self.encoder_filter_factor_base_lin_vel_x * encoder_output[0, 0]
            + (1.0 - self.encoder_filter_factor_base_lin_vel_x) * self.encoder_output_last[0, 0]
        )
        encoder_output_filtered[0, 1] = (
            self.encoder_filter_factor_base_lin_vel_y * encoder_output[0, 1]
            + (1.0 - self.encoder_filter_factor_base_lin_vel_y) * self.encoder_output_last[0, 1]
        )
        encoder_output_filtered[0, 2] = (
            self.encoder_filter_factor_base_lin_vel_z * encoder_output[0, 2]
            + (1.0 - self.encoder_filter_factor_base_lin_vel_z) * self.encoder_output_last[0, 2]
        )

        encoder_output_filtered[0, 3] = (
            self.encoder_filter_factor_base_height_offset * encoder_output[0, 3]
            + (1.0 - self.encoder_filter_factor_base_height_offset) * self.encoder_output_last[0, 3]
        )

        return encoder_output_filtered


class RobotGR1NowhlaAlgorithmRLStairEncoderControlModel(RobotGR1NowhlaAlgorithmRLWalkEncoderControlModel):
    def __init__(self, dt=0.01):
        super().__init__(dt=dt)

        # actor-critic
        self.ac_profile = "GR1T1-mh-pri"
        self.nn_actor_output_scale_factor = 1.0

        # encoder
        self.encoder_profile = "GR1T1-history-blv-bho"
        self.nn_encoder_input_history_length = 5
        self.encoder_output_last = torch.zeros(1, 4)

    def load_model(self):
        # nerual network
        try:
            self.model_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_1600.pt")
            # print("model_file_path: ", self.model_file_path)

            model = torch.load(self.model_file_path, map_location=torch.device("cpu"))
            model_actor_dict = model["model_state_dict"]

            self.nn_actor = ActorCriticMLP(
                num_actor_obs=201,
                num_critic_obs=205,
                num_actions=self.num_of_joints_controlled,
                actor_hidden_dims=[512, 256, 128],
                critic_hidden_dims=[512, 256, 128],
            )
            # ActorCriticMLP(num_actor_obs=67,
            #                num_critic_obs=67,
            #                num_actions=self.num_of_joints_controlled,
            #                actor_hidden_dims=[512, 256, 128],
            #                critic_hidden_dims=[512, 256, 128])

            self.nn_actor.load_state_dict(model_actor_dict)

            model_encoder_dict = model["encoder_state_dict"]

            self.nn_encoder = Encoder(num_encoder_obs=30 * 5, num_encoder_out=4, encoder_hidden_dims=[512, 256, 128])
            # Encoder(num_encoder_obs=30,
            #         num_encoder_out=4,
            #         encoder_hidden_dims=[512, 256, 128])

            self.nn_encoder.load_state_dict(model_encoder_dict)

        except Exception as e:
            Logger().print_trace_warning(e)

    def actor_obs(self):
        if self.ac_profile == "GR1T1-mh-pri":
            self.nn_actor_input = torch.cat(
                (
                    # unobservable proprioception
                    self.nn_actor_input_base_linear_velocity,
                    self.nn_actor_input_base_height_offset,
                    # base related
                    self.nn_actor_input_base_angular_velocity,
                    self.nn_actor_input_base_projected_gravity,
                    self.nn_actor_input_commands,
                    # dof related
                    self.nn_actor_input_measured_joint_position,
                    self.nn_actor_input_measured_joint_velocity,
                    self.nn_actor_input_action,
                    # phase related
                    self.nn_actor_input_gait_phase_sin,
                    self.nn_actor_input_gait_phase_cos,
                    self.nn_actor_input_gait_phase_ratio,
                    self.nn_actor_input_gait_cycle,
                    # height related
                    self.nn_actor_input_surround_heights_offset,
                ),
                dim=-1,
            )

        else:
            raise Exception("Unknown ac_profile: ", self.ac_profile)
