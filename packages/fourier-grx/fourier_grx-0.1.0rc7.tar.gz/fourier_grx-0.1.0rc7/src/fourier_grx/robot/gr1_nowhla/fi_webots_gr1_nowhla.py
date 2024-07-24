import os
from enum import Enum

import numpy
import torch
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.webots.webots_robot import WebotsRobot, WebotsRobotTask
from fourier_grx.robot.gr1_nowhla.fi_robot_gr1_nowhla_algorithm import (
    RobotGR1NowhlaAlgorithmStandControlModel,
)
from fourier_grx.robot.gr1_nowhla.fi_robot_gr1_nowhla_algorithm_rl import (
    RobotGR1NowhlaAlgorithmRLStairEncoderControlModel,
    RobotGR1NowhlaAlgorithmRLWalkEncoderControlModel,
)


class WebotsGR1NowhlaTask(Enum):
    IDLE = WebotsRobotTask.IDLE.value
    STAND = 1
    RL_WALK_ENCODER = 2
    RL_STAIR_ENCODER = 3


class WebotsGR1Nowhla(WebotsRobot):
    def __init__(self, sim_dt):
        super().__init__(sim_dt=sim_dt)

        self.robot_name = "GR1Nowhla"

        self.base_target_height = 0.90

        self.num_of_legs = 2

        self.num_of_links = 6 + 6 + 4 + 4
        self.links_name = [
            # left leg
            "l_thigh_roll",
            "l_thigh_yaw",
            "l_thigh_pitch",
            "l_shank_pitch",
            "l_foot_pitch",
            "l_foot_roll",
            # right leg
            "r_thigh_roll",
            "r_thigh_yaw",
            "r_thigh_pitch",
            "r_shank_pitch",
            "r_foot_pitch",
            "r_foot_roll",
            # left arm
            "l_upper_arm_pitch",
            "l_upper_arm_roll",
            "l_upper_arm_yaw",
            "l_lower_arm_pitch",
            # right arm
            "r_upper_arm_pitch",
            "r_upper_arm_roll",
            "r_upper_arm_yaw",
            "r_lower_arm_pitch",
        ]

        self.num_of_joints = 6 + 6 + 4 + 4
        self.joints_name = [
            # left leg
            "l_hip_roll",
            "l_hip_yaw",
            "l_hip_pitch",
            "l_knee_pitch",
            "l_ankle_pitch",
            "l_ankle_roll",
            # right leg
            "r_hip_roll",
            "r_hip_yaw",
            "r_hip_pitch",
            "r_knee_pitch",
            "r_ankle_pitch",
            "r_ankle_roll",
            # left arm
            "l_shoulder_pitch",
            "l_shoulder_roll",
            "l_shoulder_yaw",
            "l_elbow_pitch",
            # right arm
            "r_shoulder_pitch",
            "r_shoulder_roll",
            "r_shoulder_yaw",
            "r_elbow_pitch",
        ]
        self.joints_kp = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.joints_ki = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.joints_kd = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]

        self.num_of_joint_position_sensors = 6 + 6 + 4 + 4
        self.joint_position_sensors_name = [
            # left leg
            "l_hip_roll_sensor",
            "l_hip_yaw_sensor",
            "l_hip_pitch_sensor",
            "l_knee_pitch_sensor",
            "l_ankle_pitch_sensor",
            "l_ankle_roll_sensor",
            # right leg
            "r_hip_roll_sensor",
            "r_hip_yaw_sensor",
            "r_hip_pitch_sensor",
            "r_knee_pitch_sensor",
            "r_ankle_pitch_sensor",
            "r_ankle_roll_sensor",
            # left arm
            "l_shoulder_pitch_sensor",
            "l_shoulder_roll_sensor",
            "l_shoulder_yaw_sensor",
            "l_elbow_pitch_sensor",
            # right arm
            "r_shoulder_pitch_sensor",
            "r_shoulder_roll_sensor",
            "r_shoulder_yaw_sensor",
            "r_elbow_pitch_sensor",
        ]

        self.num_of_imus = 1
        self.imus_name = ["inertial unit"]

        self.num_of_gyros = 1
        self.gyros_name = ["gyro"]

        self.num_of_accelerometers = 1
        self.accelerometers_name = ["accelerometer"]

        # self.tasks
        self.tasks = [
            WebotsGR1NowhlaTask.IDLE,
            WebotsGR1NowhlaTask.STAND,
            WebotsGR1NowhlaTask.RL_WALK_ENCODER,
            WebotsGR1NowhlaTask.RL_STAIR_ENCODER,
        ]

        self.task_selected = WebotsGR1NowhlaTask.STAND.value
        self.task_selected_last = self.task_selected
        self.task_assigned = WebotsGR1NowhlaTask.STAND.value
        self.task_assigned_last = self.task_assigned

        # avg
        self.base_measured_quat_to_world_buffer_length = 10
        self.base_measured_quat_to_world_buffer = []
        self.base_measured_quat_to_world_avg = numpy.zeros(4)

        self.base_measured_rpy_vel_to_self_buffer_length = 10
        self.base_measured_rpy_vel_to_self_buffer = []
        self.base_measured_rpy_vel_to_self_avg = numpy.zeros(3)

        self.joint_measured_velocity_value_buffer_length = 10
        self.joint_measured_velocity_value_buffer = []
        self.joint_measured_velocity_value_avg = numpy.zeros(self.num_of_joints)

        # algorithm models
        self.stand_algorithm_model = RobotGR1NowhlaAlgorithmStandControlModel()

        # run under real robot control frequency
        self.rl_walk_encoder_algorithm_model_run_decimation = 20
        self.rl_walk_encoder_algorithm_model_run_count = 0
        self.rl_walk_encoder_algorithm_model = RobotGR1NowhlaAlgorithmRLWalkEncoderControlModel(
            dt=0.001 * self.sim_dt * self.rl_walk_encoder_algorithm_model_run_decimation
        )

        self.rl_stair_encoder_algorithm_model_run_decimation = 20
        self.rl_stair_encoder_algorithm_model_run_count = 0
        self.rl_stair_encoder_algorithm_model = RobotGR1NowhlaAlgorithmRLStairEncoderControlModel(
            dt=0.001 * self.sim_dt * self.rl_stair_encoder_algorithm_model_run_decimation
        )

        # pd control
        self.joint_pd_control_target = numpy.zeros(self.num_of_joints)
        self.joint_pd_control_output = numpy.zeros(self.num_of_joints)

        self.joint_pd_control_target_buffer = []
        self.joint_pd_control_target_delay = 0

        for i in range(self.joint_pd_control_target_delay + 1):
            self.joint_pd_control_target_buffer.append(numpy.zeros(self.num_of_joints))

        self.joint_pd_control_kp = numpy.array(
            [
                251.625,
                362.5214,
                200.0,
                200.0,
                10.9885,
                0.25,  # left leg(6)
                251.625,
                362.5214,
                200.0,
                200.0,
                10.9885,
                0.25,  # right leg(6)
                92.85,
                92.85,
                112.06,
                112.06,  # left arm(4)
                92.85,
                92.85,
                112.06,
                112.06,  # right arm(4)
            ]
        )
        self.joint_pd_control_kd = numpy.array(
            [
                14.72,
                10.0833,
                11.0,
                11.0,
                0.5991,
                0.01,  # left leg(6)
                14.72,
                10.0833,
                11.0,
                11.0,
                0.5991,
                0.01,  # right leg(6)
                2.575,
                2.575,
                3.1,
                3.1,  # left arm(4)
                2.575,
                2.575,
                3.1,
                3.1,  # right arm(4)
            ]
        )
        self.joint_pd_control_max = numpy.array(
            [
                100.0,
                82.5,
                150.0,
                150.0,
                16.0,
                8.0,  # left leg(6)
                100.0,
                82.5,
                150.0,
                150.0,
                16.0,
                8.0,  # right leg(6)
                38.0,
                38.0,
                30.0,
                30.0,  # left arm(4)
                38.0,
                38.0,
                30.0,
                30.0,  # right arm(4)
            ]
        )
        self.joint_pd_control_min = numpy.array(
            [
                -100.0,
                -82.5,
                -150.0,
                -150.0,
                -16.0,
                -8.0,  # left leg(6)
                -100.0,
                -82.5,
                -150.0,
                -150.0,
                -16.0,
                -8.0,  # right leg(6)
                -38.0,
                -38.0,
                -30.0,
                -30.0,  # left arm(4)
                -38.0,
                -38.0,
                -30.0,
                -30.0,  # right arm(4)
            ]
        )

        # actuator network
        self.actuator_run_decimation = 2  # actuator network run decimation (also the actuator model fit decimation)

        self.use_actuator_network = False
        self.actuator_network_type = "mlp"
        self.actuator_network_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../../../fourier-core-models/actuators/mlp_jit_1307e_8_50000.pt",
        )
        self.actuator_direction = -1.0
        self.actuator_run_count = 0

        if self.use_actuator_network:
            if self.actuator_network_type == "lstm":
                self.actuator_network = torch.jit.load(self.actuator_network_file)
                self.actuator_network_input = torch.zeros(self.num_of_joints, 1, 2)  # dof_target - dof_pos, dof_vel
                self.actuator_network_hidden_state = torch.zeros(2, self.num_of_joints, 8)
                self.actuator_network_cell_state = torch.zeros(2, self.num_of_joints, 8)

            elif self.actuator_network_type == "mlp":
                self.actuator_network = torch.jit.load(self.actuator_network_file)
                self.actuator_network_input_size = 16
                self.actuator_network_input = torch.zeros(
                    self.num_of_joints, self.actuator_network_input_size
                )  # dof_target - dof_pos, dof_vel

            else:
                Exception("actuator network type is not supported")

        # actuator networks
        self.use_actuator_networks = True
        self.actuator_networks_types = [
            "mlp",
            "mlp",
            "mlp",
            "mlp",
            "pd",
        ]
        self.actuator_network_file = [
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../../../fourier-core-models/actuators/mlp_802028_3_20000_32_0417.pt",
            ),
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../../../fourier-core-models/actuators/mlp_601750_3_20000_32_0413.pt",
            ),
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../../../fourier-core-models/actuators/mlp_1307e_3_20000_32_0413.pt",
            ),
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../../../fourier-core-models/actuators/mlp_1307e_3_10000_0413.pt",
            ),
            None,
        ]
        self.actuator_match_indexes = [
            # [0, 6],  # 802050
            # [1, 7],  # 601750
            # [2, 3, 8, 9],  # 1307e
            # [],  # 361480
            # [4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],  # pd
            [0, 6],  # 802050
            [],  # 601750
            [],  # 1307e
            [],  # 361480
            [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],  # pd
        ]
        self.actuator_directions = [
            # left leg
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            # right leg
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            # left arm
            1.0,
            1.0,
            1.0,
            1.0,
            # right arm
            1.0,
            1.0,
            1.0,
            1.0,
        ]

        if self.use_actuator_networks:
            self.actuator_networks = []
            if self.actuator_network_type == "mlp":
                for i in range(len(self.actuator_network_file)):
                    if self.actuator_network_file[i] is None:
                        self.actuator_networks.append(None)
                        continue

                    self.actuator_networks.append(torch.jit.load(self.actuator_network_file[i]))

                self.actuator_network_input_size = 3 * 2
                self.actuator_network_input = torch.zeros(
                    self.num_of_joints, self.actuator_network_input_size
                )  # dof_target - dof_pos, dof_vel

            else:
                Exception("actuator network type is not supported")

        # start task
        # self.task_assigned_last = WebotsGR1NowhlaTask.STAND.value
        # self.task_assigned = WebotsGR1NowhlaTask.RL_STAIR_ENCODER.value

        # record
        self.flag_record = FlagState.CLEAR
        self.record_tick = 0
        self.record_start = 0
        self.record_length = 5000

    def control_loop_update_joystick_state_print_selected_task(self):
        super().control_loop_update_joystick_state_print_selected_task()

        for item in WebotsGR1NowhlaTask:
            if self.tasks[self.task_selected] == item:
                print("task_selected = ", item)
                break

    def control_loop_update_joystick_state_print_assigned_task(self):
        super().control_loop_update_joystick_state_print_assigned_task()

        for item in WebotsGR1NowhlaTask:
            if self.tasks[self.task_assigned] == item:
                print("task_assigned = ", item)
                break

    def before_control_loop(self):
        super().before_control_loop()

        # assign control model
        self.task_algorithm_model = self.stand_algorithm_model

    def control_loop_update_task_state(self):
        if (
            self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.IDLE
            and self.tasks[self.task_assigned_last] != WebotsGR1NowhlaTask.IDLE
        ):
            print("Info: robot task IDLE")
            for joint in self.joints:
                joint.setPosition(0)

        elif (
            self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.STAND
            and self.tasks[self.task_assigned_last] != WebotsGR1NowhlaTask.STAND
        ):
            print("Info: robot task STAND")
            for joint in self.joints:
                joint.setPosition(0)

            self.task_algorithm_model = self.stand_algorithm_model

        elif (
            self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.RL_WALK_ENCODER
            and self.tasks[self.task_assigned_last] != WebotsGR1NowhlaTask.RL_WALK_ENCODER
        ):
            print("Info: robot task RL_WALK_ENCODER")

            self.rl_walk_encoder_algorithm_model.flag_inited = False
            self.task_algorithm_model = self.rl_walk_encoder_algorithm_model

            self.flag_record = FlagState.SET  # start recording...

        elif (
            self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.RL_STAIR_ENCODER
            and self.tasks[self.task_assigned_last] != WebotsGR1NowhlaTask.RL_STAIR_ENCODER
        ):
            print("Info: robot task RL_STAIR_ENCODER")

            self.rl_stair_encoder_algorithm_model.flag_inited = False
            self.task_algorithm_model = self.rl_stair_encoder_algorithm_model

            self.flag_record = FlagState.SET  # start recording...

        else:
            pass

        self.set_task_assigned(self.task_assigned)

    def control_loop_algorithm(self):
        if self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.IDLE:
            pass

        elif self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.STAND:
            self.stand_algorithm_model.run(
                joint_measured_position_urdf=self.joint_measured_position_value,
                joint_measured_velocity_urdf=self.joint_measured_velocity_value_avg,
            )

            self.joint_pd_control_target = self.stand_algorithm_model.output_joint_position

        elif self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.RL_WALK_ENCODER:
            if (
                self.rl_walk_encoder_algorithm_model_run_count % self.rl_walk_encoder_algorithm_model_run_decimation
                == 0
            ):
                body_speed_lin_max = 0.70
                body_speed_ang_max = 0.35
                commands = numpy.array(
                    [
                        body_speed_lin_max * -self.joystick_axis_left_value[1],
                        body_speed_lin_max * -self.joystick_axis_left_value[0],
                        body_speed_ang_max * -self.joystick_axis_right_value[0],
                    ]
                )

                # Jason 2024-02-26:
                # Use the joystick button R2 to switch between walking and standing
                # It it like a safety catch, when the button is released, the robot will stand still
                # if self.joystick_button_R2_value == 1:
                #     self.rl_walk_encoder_algorithm_model.gait_phase_ratio = \
                #         self.rl_walk_encoder_algorithm_model.gait_phase_ratio_walk
                # else:
                #     self.rl_walk_encoder_algorithm_model.gait_phase_ratio = \
                #         self.rl_walk_encoder_algorithm_model.gait_phase_ratio_stand
                #     commands = numpy.array([0, 0, 0])
                self.rl_walk_encoder_algorithm_model.gait_phase_ratio = (
                    self.rl_walk_encoder_algorithm_model.gait_phase_ratio_walk
                )

                joint_pd_control_target, encoder_output, encoder_output_raw = self.rl_walk_encoder_algorithm_model.run(
                    init_output=self.joint_pd_control_target,
                    commands=commands,
                    base_measured_xyz_to_world=self.base_measured_xyz_to_world
                    + numpy.random.normal(0, 0.00, 3),  # 0.03
                    base_measured_quat_to_world=self.base_measured_quat_to_world_avg
                    + numpy.random.normal(0, 0.00, 4),  # 0.02
                    base_measured_xyz_vel_to_world=self.base_measured_xyz_vel_to_self
                    + numpy.random.normal(0, 0.00, 3),  # 0.05
                    base_measured_rpy_vel_to_world=self.base_measured_rpy_vel_to_self_avg
                    + numpy.random.normal(0, 0.00, 3),  # 0.04
                    joint_measured_position_urdf=self.joint_measured_position_value
                    + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.03
                    joint_measured_velocity_urdf=self.joint_measured_velocity_value_avg
                    + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.10
                )

                self.joint_pd_control_target = joint_pd_control_target
                self.encoder_output = encoder_output
                self.encoder_output_raw = encoder_output_raw

            self.rl_walk_encoder_algorithm_model_run_count += 1

        elif self.tasks[self.task_assigned] == WebotsGR1NowhlaTask.RL_STAIR_ENCODER:
            if (
                self.rl_stair_encoder_algorithm_model_run_count % self.rl_stair_encoder_algorithm_model_run_decimation
                == 0
            ):
                body_speed_lin_max = 0.70
                body_speed_ang_max = 0.35
                commands = numpy.array(
                    [
                        body_speed_lin_max * -self.joystick_axis_left_value[1],
                        body_speed_lin_max * -self.joystick_axis_left_value[0],
                        body_speed_ang_max * -self.joystick_axis_right_value[0],
                    ]
                )

                # Jason 2024-02-26:
                # Use the joystick button R2 to switch between walking and standing
                # It it like a safety catch, when the button is released, the robot will stand still
                # if self.joystick_button_R2_value == 1:
                #     self.rl_stair_encoder_algorithm_model.gait_phase_ratio = \
                #         self.rl_stair_encoder_algorithm_model.gait_phase_ratio_walk
                # else:
                #     self.rl_stair_encoder_algorithm_model.gait_phase_ratio = \
                #         self.rl_stair_encoder_algorithm_model.gait_phase_ratio_stand
                #     commands = numpy.array([0, 0, 0])

                self.rl_stair_encoder_algorithm_model.gait_phase_ratio = (
                    self.rl_stair_encoder_algorithm_model.gait_phase_ratio_walk
                )

                joint_pd_control_target, encoder_output, encoder_output_raw = self.rl_stair_encoder_algorithm_model.run(
                    init_output=self.joint_pd_control_target,
                    commands=commands,
                    base_measured_xyz_to_world=self.base_measured_xyz_to_world
                    + numpy.random.normal(0, 0.00, 3),  # 0.03
                    base_measured_quat_to_world=self.base_measured_quat_to_world_avg
                    + numpy.random.normal(0, 0.00, 4),  # 0.02
                    base_measured_xyz_vel_to_world=self.base_measured_xyz_vel_to_self
                    + numpy.random.normal(0, 0.00, 3),  # 0.05
                    base_measured_rpy_vel_to_world=self.base_measured_rpy_vel_to_self_avg
                    + numpy.random.normal(0, 0.00, 3),  # 0.04
                    joint_measured_position_urdf=self.joint_measured_position_value
                    + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.03
                    joint_measured_velocity_urdf=self.joint_measured_velocity_value_avg
                    + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.10
                    measured_surround_heights=numpy.zeros(11 * 11),
                )

                self.joint_pd_control_target = joint_pd_control_target
                self.encoder_output = encoder_output
                self.encoder_output_raw = encoder_output_raw

            self.rl_stair_encoder_algorithm_model_run_count += 1

        else:
            pass

    def control_loop_output(self):
        # Jason 2024-02-27:
        # add delay to the joint_pd_control_target
        self.joint_pd_control_target_buffer = self.joint_pd_control_target_buffer[1:]
        self.joint_pd_control_target_buffer.append(self.joint_pd_control_target)

        # self.joint_pd_control_target_to_sim = self.joint_pd_control_target_buffer[0]  # use the first element of the buffer
        self.joint_pd_control_target_to_sim = self.joint_pd_control_target

        # PD Control
        if self.tasks[self.task_assigned] != WebotsGR1NowhlaTask.IDLE:
            if self.use_actuator_network is True:
                if self.actuator_run_count % self.actuator_run_decimation == 0:
                    if self.actuator_network_type == "lstm":
                        # actuator network
                        with torch.inference_mode():
                            self.actuator_network_input[:, 0, 0] = torch.from_numpy(
                                self.joint_pd_control_target_to_sim - self.joint_measured_position_value
                            )
                            self.actuator_network_input[:, 0, 1] = torch.from_numpy(self.joint_measured_velocity_value)

                            (
                                self.joint_pd_control_output,
                                (self.actuator_network_hidden_state[:], self.actuator_network_cell_state[:]),
                            ) = self.actuator_network(
                                self.actuator_network_input,
                                (self.actuator_network_hidden_state, self.actuator_network_cell_state),
                            )
                            self.joint_pd_control_output = self.actuator_direction * self.joint_pd_control_output

                    elif self.actuator_network_type == "mlp":
                        # actuator network
                        with torch.inference_mode():
                            for i in range(self.actuator_network_input_size // 2 - 1):
                                self.actuator_network_input[:, 0 + i] = self.actuator_network_input[:, 0 + i + 1]
                                self.actuator_network_input[:, self.actuator_network_input_size // 2 - 1 + i] = (
                                    self.actuator_network_input[:, self.actuator_network_input_size // 2 - 1 + i + 1]
                                )
                            self.actuator_network_input[:, self.actuator_network_input_size // 2 * 1 - 1 - 1] = (
                                torch.from_numpy(
                                    self.joint_pd_control_target_to_sim - self.joint_measured_position_value
                                )
                            )
                            self.actuator_network_input[:, self.actuator_network_input_size // 2 * 2 - 1 - 0] = (
                                torch.from_numpy(self.joint_measured_velocity_value)
                            )

                            self.joint_pd_control_output = self.actuator_network(self.actuator_network_input)
                            self.joint_pd_control_output = self.actuator_direction * self.joint_pd_control_output

                            self.joint_pd_control_output = self.joint_pd_control_output.detach().numpy().flatten()

                    else:
                        Exception("actuator network type is not supported")

                self.actuator_run_count += 1

            elif self.use_actuator_networks is True:
                if self.actuator_run_count % self.actuator_run_decimation == 0:
                    # actuator network
                    with torch.inference_mode():
                        for i in range(self.actuator_network_input_size // 2 - 1):
                            self.actuator_network_input[:, 0 + i] = self.actuator_network_input[:, 0 + i + 1]
                            self.actuator_network_input[:, self.actuator_network_input_size // 2 - 1 + i] = (
                                self.actuator_network_input[:, self.actuator_network_input_size // 2 - 1 + i + 1]
                            )
                        self.actuator_network_input[:, self.actuator_network_input_size // 2 * 1 - 1 - 1] = (
                            torch.from_numpy(self.joint_pd_control_target_to_sim - self.joint_measured_position_value)
                        )
                        self.actuator_network_input[:, self.actuator_network_input_size // 2 * 2 - 1 - 0] = (
                            torch.from_numpy(self.joint_measured_velocity_value)
                        )

                        self.joint_pd_control_output = numpy.zeros(self.num_of_joints)

                        for i in range(len(self.actuator_networks)):
                            actuator_type = self.actuator_networks_types[i]
                            actuator_network = self.actuator_networks[i]
                            match_indexes = numpy.array(self.actuator_match_indexes[i])

                            if actuator_type == "mlp":
                                _joint_pd_control_output = actuator_network(self.actuator_network_input)
                                _joint_pd_control_output = _joint_pd_control_output.view(self.num_of_joints)
                            elif actuator_type == "pd":
                                _joint_pd_control_output = self.joint_pd_control_kp * (
                                    self.joint_pd_control_target_to_sim - self.joint_measured_position_value
                                ) - self.joint_pd_control_kd * (self.joint_measured_velocity_value)
                            else:
                                Exception("actuator network type is not supported")

                            for j in range(len(match_indexes)):
                                match_index = match_indexes[j]

                                self.joint_pd_control_output[match_index] = _joint_pd_control_output[match_index]
                                self.joint_pd_control_output[match_index] *= self.actuator_directions[match_index]

                else:
                    Exception("actuator network type is not supported")

            else:
                # pd control
                self.joint_pd_control_output = self.joint_pd_control_kp * (
                    self.joint_pd_control_target_to_sim - self.joint_measured_position_value
                ) - self.joint_pd_control_kd * (self.joint_measured_velocity_value)

            self.joint_pd_control_output = numpy.clip(
                self.joint_pd_control_output, self.joint_pd_control_min, self.joint_pd_control_max
            )

            # output
            for i in range(self.num_of_joints):
                if self.task_algorithm_model.flag_joint_pd_torque_control[i] == FlagState.SET:
                    self.joints[i].setTorque(self.joint_pd_control_output[i])

                if self.task_algorithm_model.flag_joint_position_control[i] == FlagState.SET:
                    self.joints[i].setPosition(self.joint_pd_control_target_to_sim[i])

    def control_loop_record_stack(self):
        if self.task_assigned == WebotsGR1NowhlaTask.RL_WALK_ENCODER.value:
            self.record_joint_position_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        numpy.round(self.joint_measured_position_value, 3),
                        numpy.round(self.joint_pd_control_target_to_sim, 3),
                        numpy.round(self.rl_walk_encoder_algorithm_model.joint_measured_position[0], 3),
                    )
                )
            )

            self.record_joint_velocity_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        numpy.round(self.joint_measured_velocity_value, 3),
                        numpy.round(self.rl_walk_encoder_algorithm_model.joint_measured_velocity[0], 3),
                    )
                )
            )

            self.record_joint_torque_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        numpy.round(self.joint_measured_torque_value, 3),
                        numpy.round(self.joint_pd_control_output, 3),
                    )
                )
            )

            self.record_base_x_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_vel_to_self[0],
                        self.encoder_output[0],
                        self.encoder_output_raw[0],
                        self.rl_walk_encoder_algorithm_model.base_xyz_vel_to_self[0, 0],
                    )
                )
            )

            self.record_base_y_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_vel_to_self[1],
                        self.encoder_output[1],
                        self.encoder_output_raw[1],
                        self.rl_walk_encoder_algorithm_model.base_xyz_vel_to_self[0, 1],
                    )
                )
            )

            self.record_base_z_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_vel_to_self[2],
                        self.encoder_output[2],
                        self.encoder_output_raw[2],
                        self.rl_walk_encoder_algorithm_model.base_xyz_vel_to_self[0, 2],
                    )
                )
            )

            self.record_base_roll_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_rpy_vel_to_self[0],
                        self.rl_walk_encoder_algorithm_model.base_rpy_vel_to_self[0, 0],
                    )
                )
            )

            self.record_base_pitch_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_rpy_vel_to_self[1],
                        self.rl_walk_encoder_algorithm_model.base_rpy_vel_to_self[0, 1],
                    )
                )
            )

            self.record_base_yaw_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_rpy_vel_to_self[2],
                        self.rl_walk_encoder_algorithm_model.base_rpy_vel_to_self[0, 2],
                    )
                )
            )

            self.record_base_z_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_to_world[2],
                        self.encoder_output[3],
                        self.encoder_output_raw[3],
                        self.rl_walk_encoder_algorithm_model.base_xyz_to_world[0, 2],
                    )
                )
            )

            self.record_base_quat_x_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[0],
                        self.rl_walk_encoder_algorithm_model.base_quat_to_world[0, 0],
                    )
                )
            )

            self.record_base_quat_y_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[1],
                        self.rl_walk_encoder_algorithm_model.base_quat_to_world[0, 1],
                    )
                )
            )

            self.record_base_quat_z_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[2],
                        self.rl_walk_encoder_algorithm_model.base_quat_to_world[0, 2],
                    )
                )
            )

            self.record_base_quat_w_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[3],
                        self.rl_walk_encoder_algorithm_model.base_quat_to_world[0, 3],
                    )
                )
            )

        if self.task_assigned == WebotsGR1NowhlaTask.RL_STAIR_ENCODER.value:
            self.record_joint_position_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        numpy.round(self.joint_measured_position_value, 3),
                        numpy.round(self.joint_pd_control_target_to_sim, 3),
                        numpy.round(self.rl_stair_encoder_algorithm_model.joint_measured_position[0], 3),
                    )
                )
            )

            self.record_joint_velocity_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        numpy.round(self.joint_measured_velocity_value, 3),
                        numpy.round(self.rl_stair_encoder_algorithm_model.joint_measured_velocity[0], 3),
                    )
                )
            )

            self.record_joint_torque_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        numpy.round(self.joint_measured_torque_value, 3),
                        numpy.round(self.joint_pd_control_output, 3),
                    )
                )
            )

            self.record_base_x_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_vel_to_self[0],
                        self.encoder_output[0],
                        self.encoder_output_raw[0],
                        self.rl_stair_encoder_algorithm_model.base_xyz_vel_to_self[0, 0],
                    )
                )
            )

            self.record_base_y_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_vel_to_self[1],
                        self.encoder_output[1],
                        self.encoder_output_raw[1],
                        self.rl_stair_encoder_algorithm_model.base_xyz_vel_to_self[0, 1],
                    )
                )
            )

            self.record_base_z_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_vel_to_self[2],
                        self.encoder_output[2],
                        self.encoder_output_raw[2],
                        self.rl_stair_encoder_algorithm_model.base_xyz_vel_to_self[0, 2],
                    )
                )
            )

            self.record_base_roll_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_rpy_vel_to_self[0],
                        self.rl_stair_encoder_algorithm_model.base_rpy_vel_to_self[0, 0],
                    )
                )
            )

            self.record_base_pitch_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_rpy_vel_to_self[1],
                        self.rl_stair_encoder_algorithm_model.base_rpy_vel_to_self[0, 1],
                    )
                )
            )

            self.record_base_yaw_vel_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_rpy_vel_to_self[2],
                        self.rl_stair_encoder_algorithm_model.base_rpy_vel_to_self[0, 2],
                    )
                )
            )

            self.record_base_z_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_xyz_to_world[2],
                        self.encoder_output[3],
                        self.encoder_output_raw[3],
                        self.rl_stair_encoder_algorithm_model.base_xyz_to_world[0, 2],
                    )
                )
            )

            self.record_base_quat_x_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[0],
                        self.rl_stair_encoder_algorithm_model.base_quat_to_world[0, 0],
                    )
                )
            )

            self.record_base_quat_y_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[1],
                        self.rl_stair_encoder_algorithm_model.base_quat_to_world[0, 1],
                    )
                )
            )

            self.record_base_quat_z_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[2],
                        self.rl_stair_encoder_algorithm_model.base_quat_to_world[0, 2],
                    )
                )
            )

            self.record_base_quat_w_buffer.append(
                numpy.hstack(
                    (
                        self.record_tick - self.record_start,
                        self.base_measured_quat_to_world[3],
                        self.rl_stair_encoder_algorithm_model.base_quat_to_world[0, 3],
                    )
                )
            )
