from enum import Enum

import numpy
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.webots.webots_joystick import WebotsJoystick, WebotsJoystickType
from fourier_core.webots.webots_robot import WebotsRobot, WebotsRobotTask
from fourier_grx.robot.gr1_simple.fi_robot_gr1_simple_algorithm \
    import RobotGR1SimpleAlgorithmStandControlModel \
    as StandControlModel
from fourier_grx.robot.gr1_simple.fi_robot_gr1_simple_algorithm_rl \
    import RobotGR1SimpleAlgorithmRLAirtimeControlModel \
    as RLAirtimeControlModel
from fourier_grx.robot.gr1_simple.fi_robot_gr1_simple_algorithm_rl_stack \
    import RobotGR1SimpleAlgorithmRLStackControlModel \
    as RLStackControlModel
from fourier_grx.robot.gr1_simple.fi_robot_gr1_simple_algorithm_rl_cpg_stack \
    import RobotGR1SimpleAlgorithmRLCPGStackControlModel \
    as RLCPGStackControlModel


# fmt: off

class WebotsGR1SimpleTask(Enum):
    IDLE = WebotsRobotTask.IDLE.value
    STAND = 1
    RL_AIRTIME = 2
    RL_STACK = 3
    RL_CPG_STACK = 4


class WebotsGR1Simple(WebotsRobot):
    def __init__(self, sim_dt):
        super().__init__(sim_dt=sim_dt)

        self.joystick = WebotsJoystick(flag_enable=True, joystick_type=WebotsJoystickType.XBOX)

        self.robot_name = "GR1Simple"

        self.base_target_height = 0.90

        self.num_of_legs = 2

        self.num_of_links = 5 + 5
        self.links_name = [
            # left leg
            "l_thigh_roll",
            "l_thigh_yaw",
            "l_thigh_pitch",
            "l_shank_pitch",
            "l_foot_pitch",
            # right leg
            "r_thigh_roll",
            "r_thigh_yaw",
            "r_thigh_pitch",
            "r_shank_pitch",
            "r_foot_pitch",
        ]

        self.num_of_joints = 5 + 5
        self.joints_name = [
            # left leg
            "l_hip_roll",
            "l_hip_yaw",
            "l_hip_pitch",
            "l_knee_pitch",
            "l_ankle_pitch",
            # right leg
            "r_hip_roll",
            "r_hip_yaw",
            "r_hip_pitch",
            "r_knee_pitch",
            "r_ankle_pitch",
        ]
        self.joints_kp = numpy.zeros(self.num_of_joints)
        self.joints_ki = numpy.zeros(self.num_of_joints)
        self.joints_kd = numpy.zeros(self.num_of_joints)

        self.num_of_joint_position_sensors = 5 + 5
        self.joint_position_sensors_name = [
            # left leg
            "l_hip_roll_sensor",
            "l_hip_yaw_sensor",
            "l_hip_pitch_sensor",
            "l_knee_pitch_sensor",
            "l_ankle_pitch_sensor",
            # right leg
            "r_hip_roll_sensor",
            "r_hip_yaw_sensor",
            "r_hip_pitch_sensor",
            "r_knee_pitch_sensor",
            "r_ankle_pitch_sensor",
        ]

        self.num_of_imus = 1
        self.imus_name = ["inertial unit"]

        self.num_of_gyros = 1
        self.gyros_name = ["gyro"]

        self.num_of_accelerometers = 1
        self.accelerometers_name = ["accelerometer"]

        # self.tasks
        self.tasks = [
            WebotsGR1SimpleTask.IDLE,
            WebotsGR1SimpleTask.STAND,
            WebotsGR1SimpleTask.RL_AIRTIME,
            WebotsGR1SimpleTask.RL_STACK,
            WebotsGR1SimpleTask.RL_CPG_STACK,
        ]

        self.task_selected = WebotsGR1SimpleTask.STAND.value
        self.task_selected_last = self.task_selected
        self.task_assigned = WebotsGR1SimpleTask.STAND.value
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
        self.stand_algorithm_model = StandControlModel()

        # run under real robot control frequency
        self.rl_airtime_algorithm_model = RLAirtimeControlModel(
            dt=0.001 * self.sim_dt,
            decimation=(1 / 50) / (0.001 * sim_dt)
        )
        self.rl_stack_algorithm_model = RLStackControlModel(
            dt=0.001 * self.sim_dt,
            decimation=(1 / 50) / (0.001 * sim_dt),
            warmup_period=0.0
        )
        self.rl_cpg_stack_algorithm_model = RLCPGStackControlModel(
            dt=0.001 * self.sim_dt,
            decimation=(1 / 50) / (0.001 * sim_dt),
            warmup_period=0.0
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
                60, 45, 130, 130, 16,  # left leg(5)
                60, 45, 130, 130, 16,  # right leg(5)
            ]
        ) / (45 / 180 * numpy.pi)
        self.joint_pd_control_kd = self.joint_pd_control_kp / 10 * 2.5
        self.joint_pd_control_max = numpy.array(
            [
                60.0, 45.0, 130.0, 130.0, 16.0,  # left leg(5)
                60.0, 45.0, 130.0, 130.0, 16.0,  # right leg(5)
            ]
        )
        self.joint_pd_control_min = numpy.array(
            [
                -60.0, -45.0, -130.0, -130.0, -16.0,  # left leg(5)
                -60.0, -45.0, -130.0, -130.0, -16.0,  # right leg(5)
            ]
        )

    def control_loop_update_joystick_state_print_selected_task(self):
        super().control_loop_update_joystick_state_print_selected_task()

        for item in WebotsGR1SimpleTask:
            if self.tasks[self.task_selected] == item:
                print("task_selected = ", item)
                break

    def control_loop_update_joystick_state_print_assigned_task(self):
        super().control_loop_update_joystick_state_print_assigned_task()

        for item in WebotsGR1SimpleTask:
            if self.tasks[self.task_assigned] == item:
                print("task_assigned = ", item)
                break

    def before_control_loop(self):
        super().before_control_loop()

        # assign control model
        self.task_algorithm_model = self.stand_algorithm_model

    def control_loop_update_task_state(self):
        if (
                self.tasks[self.task_assigned] == WebotsGR1SimpleTask.IDLE
                and self.tasks[self.task_assigned_last] != WebotsGR1SimpleTask.IDLE
        ):
            print("Info: robot task IDLE")
            for joint in self.joints:
                joint.setPosition(0)

        elif (
                self.tasks[self.task_assigned] == WebotsGR1SimpleTask.STAND
                and self.tasks[self.task_assigned_last] != WebotsGR1SimpleTask.STAND
        ):
            print("Info: robot task STAND")
            for joint in self.joints:
                joint.setPosition(0)

            self.task_algorithm_model = self.stand_algorithm_model

        elif (
                self.tasks[self.task_assigned] == WebotsGR1SimpleTask.RL_AIRTIME
                and self.tasks[self.task_assigned_last] != WebotsGR1SimpleTask.RL_AIRTIME
        ):
            print("Info: robot task RL_AIRTIME")

            self.rl_airtime_algorithm_model.flag_inited = False
            self.task_algorithm_model = self.rl_airtime_algorithm_model

        elif (
                self.tasks[self.task_assigned] == WebotsGR1SimpleTask.RL_STACK
                and self.tasks[self.task_assigned_last] != WebotsGR1SimpleTask.RL_STACK
        ):
            print("Info: robot task RL_AIRTIME_STACK")

            self.rl_stack_algorithm_model.flag_inited = False
            self.task_algorithm_model = self.rl_stack_algorithm_model

        elif (
                self.tasks[self.task_assigned] == WebotsGR1SimpleTask.RL_CPG_STACK
                and self.tasks[self.task_assigned_last] != WebotsGR1SimpleTask.RL_CPG_STACK
        ):
            print("Info: robot task RL_CPG_STACK")

            self.rl_cpg_stack_algorithm_model.flag_inited = False
            self.task_algorithm_model = self.rl_cpg_stack_algorithm_model

        else:
            pass

        self.set_task_assigned(self.task_assigned)

    def control_loop_algorithm(self):
        if self.tasks[self.task_assigned] == WebotsGR1SimpleTask.IDLE:
            pass

        elif self.tasks[self.task_assigned] == WebotsGR1SimpleTask.STAND:
            self.stand_algorithm_model.run(
                joint_measured_position_urdf=self.joint_measured_position_value,
                joint_measured_velocity_urdf=self.joint_measured_velocity_value_avg,
            )

            self.joint_pd_control_target = self.stand_algorithm_model.output_joint_position

        elif self.tasks[self.task_assigned] == WebotsGR1SimpleTask.RL_AIRTIME:
            body_speed_lin_max = 0.70
            body_speed_ang_max = 0.35
            commands = numpy.array(
                [
                    body_speed_lin_max * -self.joystick_axis_left_value[1],
                    body_speed_lin_max * -self.joystick_axis_left_value[0],
                    body_speed_ang_max * -self.joystick_axis_right_value[0],
                ]
            )

            joint_pd_control_target = self.rl_airtime_algorithm_model.run(
                init_output=self.joint_pd_control_target,
                commands=commands,
                base_measured_quat_to_world=self.imu_measured_quat_to_world + numpy.random.normal(0, 0.00, 4),  # 0.02
                base_measured_rpy_vel_to_self=self.base_measured_rpy_vel_to_self
                                              + numpy.random.normal(0, 0.00, 3),  # 0.04
                joint_measured_position_urdf=self.joint_measured_position_value
                                             + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.03
                joint_measured_velocity_urdf=self.joint_measured_velocity_value
                                             + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.10
            )

            self.joint_pd_control_target = joint_pd_control_target
            self.joint_pd_control_kp = self.rl_airtime_algorithm_model.pd_control_kp_real_robot
            self.joint_pd_control_kd = self.rl_airtime_algorithm_model.pd_control_kd_real_robot

        elif self.tasks[self.task_assigned] == WebotsGR1SimpleTask.RL_STACK:
            body_speed_lin_max = 0.70
            body_speed_ang_max = 0.35
            commands = numpy.array(
                [
                    body_speed_lin_max * -self.joystick_axis_left_value[1],
                    body_speed_lin_max * -self.joystick_axis_left_value[0],
                    body_speed_ang_max * -self.joystick_axis_right_value[0],
                ]
            )

            joint_pd_control_target = self.rl_stack_algorithm_model.run(
                init_output=self.joint_pd_control_target,
                commands=commands,
                base_measured_quat_to_world=self.imu_measured_quat_to_world + numpy.random.normal(0, 0.00, 4),  # 0.02
                base_measured_rpy_vel_to_self=self.base_measured_rpy_vel_to_self
                                              + numpy.random.normal(0, 0.00, 3),  # 0.04
                joint_measured_position_urdf=self.joint_measured_position_value
                                             + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.03
                joint_measured_velocity_urdf=self.joint_measured_velocity_value
                                             + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.10
            )

            self.joint_pd_control_target = joint_pd_control_target
            self.joint_pd_control_kp = self.rl_stack_algorithm_model.pd_control_kp_real_robot
            self.joint_pd_control_kd = self.rl_stack_algorithm_model.pd_control_kd_real_robot

        elif self.tasks[self.task_assigned] == WebotsGR1SimpleTask.RL_CPG_STACK:
            body_speed_lin_max = 0.70
            body_speed_ang_max = 0.35
            commands = numpy.array(
                [
                    body_speed_lin_max * -self.joystick_axis_left_value[1],
                    body_speed_lin_max * -self.joystick_axis_left_value[0],
                    body_speed_ang_max * -self.joystick_axis_right_value[0],
                ]
            )

            joint_pd_control_target = self.rl_cpg_stack_algorithm_model.run(
                init_output=self.joint_pd_control_target,
                commands=commands,
                base_measured_quat_to_world=self.imu_measured_quat_to_world + numpy.random.normal(0, 0.00, 4),  # 0.02
                base_measured_rpy_vel_to_self=self.base_measured_rpy_vel_to_self
                                              + numpy.random.normal(0, 0.00, 3),  # 0.04
                joint_measured_position_urdf=self.joint_measured_position_value
                                             + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.03
                joint_measured_velocity_urdf=self.joint_measured_velocity_value
                                             + numpy.random.normal(0, 0.00, self.num_of_joints),  # 0.10
            )

            self.joint_pd_control_target = joint_pd_control_target
            self.joint_pd_control_kp = self.rl_cpg_stack_algorithm_model.pd_control_kp_real_robot
            self.joint_pd_control_kd = self.rl_cpg_stack_algorithm_model.pd_control_kd_real_robot

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
        if self.tasks[self.task_assigned] != WebotsGR1SimpleTask.IDLE:
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

# fmt: on
