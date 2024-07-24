from enum import Enum

import numpy
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.webots.webots_robot import WebotsRobot, WebotsRobotTask
from fourier_grx.robot.gr1_nohla.fi_robot_gr1_nohla_algorithm import RobotGR1NohlaAlgorithmStandControlModel
from fourier_grx.robot.gr1_nohla.fi_robot_gr1_nohla_algorithm_rl import RobotGR1NohlaAlgorithmRLWalkControlModel


class WebotsGR1NohlaTask(Enum):
    IDLE = WebotsRobotTask.IDLE.value
    STAND = 1
    RL_WALK = 2


class WebotsGR1Nohla(WebotsRobot):
    def __init__(self, sim_dt):
        super().__init__(sim_dt=sim_dt)

        self.robot_name = "GR1Nohla"

        self.base_target_height = 0.85

        self.num_of_legs = 2

        self.num_of_links = 6 + 6 + 3 + 4 + 4
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
            # waist
            "waist_yaw",
            "waist_pitch",
            "waist_roll",
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

        self.num_of_joints = 6 + 6 + 3 + 4 + 4
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
            # waist
            "waist_yaw",
            "waist_pitch",
            "waist_roll",
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
        self.joints_kp = numpy.zeros(self.num_of_joints)
        self.joints_ki = numpy.zeros(self.num_of_joints)
        self.joints_kd = numpy.zeros(self.num_of_joints)

        self.num_of_joint_position_sensors = 6 + 6 + 3 + 4 + 4
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
            # waist
            "waist_yaw_sensor",
            "waist_pitch_sensor",
            "waist_roll_sensor",
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
            WebotsGR1NohlaTask.IDLE,
            WebotsGR1NohlaTask.STAND,
            WebotsGR1NohlaTask.RL_WALK,
        ]

        self.task_selected = WebotsGR1NohlaTask.STAND.value
        self.task_selected_last = self.task_selected
        self.task_assigned = WebotsGR1NohlaTask.STAND.value
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
        self.stand_algorithm_model = RobotGR1NohlaAlgorithmStandControlModel()

        # run under real robot control frequency
        self.rl_walk_algorithm_model = RobotGR1NohlaAlgorithmRLWalkControlModel(
            dt=0.001 * sim_dt, decimation=(1 / 100) / (0.001 * sim_dt), warmup_period=0
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
                362.5214,
                362.5214,
                362.5214,  # waist(3)
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
                10.0833,
                10.0833,
                10.0833,  # waist(3)
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
                130.0,
                130.0,
                16.0,
                8.0,  # left leg(6)
                100.0,
                82.5,
                130.0,
                130.0,
                16.0,
                8.0,  # right leg(6)
                82.5,
                82.5,
                82.5,  # waist(3)
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
                -130.0,
                -130.0,
                -16.0,
                -8.0,  # left leg(6)
                -100.0,
                -82.5,
                -130.0,
                -130.0,
                -16.0,
                -8.0,  # right leg(6)
                -82.5,
                -82.5,
                -82.5,  # waist(3)
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

    def control_loop_update_joystick_state_print_selected_task(self):
        super().control_loop_update_joystick_state_print_selected_task()

        for item in WebotsGR1NohlaTask:
            if self.tasks[self.task_selected] == item:
                print("task_selected = ", item)
                break

    def control_loop_update_joystick_state_print_assigned_task(self):
        super().control_loop_update_joystick_state_print_assigned_task()

        for item in WebotsGR1NohlaTask:
            if self.tasks[self.task_assigned] == item:
                print("task_assigned = ", item)
                break

    def before_control_loop(self):
        super().before_control_loop()

        # assign control model
        self.task_algorithm_model = self.stand_algorithm_model

    def control_loop_update_task_state(self):
        if (
            self.tasks[self.task_assigned] == WebotsGR1NohlaTask.IDLE
            and self.tasks[self.task_assigned_last] != WebotsGR1NohlaTask.IDLE
        ):
            print("Info: robot task IDLE")
            for joint in self.joints:
                joint.setPosition(0)

        elif (
            self.tasks[self.task_assigned] == WebotsGR1NohlaTask.STAND
            and self.tasks[self.task_assigned_last] != WebotsGR1NohlaTask.STAND
        ):
            print("Info: robot task STAND")
            for joint in self.joints:
                joint.setPosition(0)

            self.task_algorithm_model = self.stand_algorithm_model

        elif (
            self.tasks[self.task_assigned] == WebotsGR1NohlaTask.RL_WALK
            and self.tasks[self.task_assigned_last] != WebotsGR1NohlaTask.RL_WALK
        ):
            print("Info: robot task RL_WALK")

            self.task_algorithm_model = self.rl_walk_algorithm_model

        else:
            pass

        self.set_task_assigned(self.task_assigned)

    def control_loop_algorithm(self):
        if self.tasks[self.task_assigned] == WebotsGR1NohlaTask.IDLE:
            pass

        elif self.tasks[self.task_assigned] == WebotsGR1NohlaTask.STAND:
            self.stand_algorithm_model.run(
                joint_measured_position_urdf=self.joint_measured_position_value,
                joint_measured_velocity_urdf=self.joint_measured_velocity_value,
            )

            self.joint_pd_control_target = self.stand_algorithm_model.output_joint_position

        elif self.tasks[self.task_assigned] == WebotsGR1NohlaTask.RL_WALK:
            body_speed_lin_max = 0.70
            body_speed_ang_max = 0.35
            commands = numpy.array(
                [
                    body_speed_lin_max * -self.joystick_axis_left_value[1],
                    body_speed_lin_max * -self.joystick_axis_left_value[0],
                    body_speed_ang_max * -self.joystick_axis_right_value[0],
                ]
            )

            joint_pd_control_target = self.rl_walk_algorithm_model.run(
                init_output=self.joint_pd_control_target,
                commands=commands,
                base_measured_quat_to_world=self.base_measured_quat_to_world + numpy.random.normal(0, 0.00, 4),
                base_measured_rpy_vel_to_self=self.gyro_measured_rpy_vel_to_self + numpy.random.normal(0, 0.00, 3),
                joint_measured_position_urdf=self.joint_measured_position_value
                + numpy.random.normal(0, 0.00, self.num_of_joints),
                joint_measured_velocity_urdf=self.joint_measured_velocity_value
                + numpy.random.normal(0, 0.00, self.num_of_joints),
            )

            self.joint_pd_control_target = joint_pd_control_target

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
        if self.tasks[self.task_assigned] != WebotsGR1NohlaTask.IDLE:
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
