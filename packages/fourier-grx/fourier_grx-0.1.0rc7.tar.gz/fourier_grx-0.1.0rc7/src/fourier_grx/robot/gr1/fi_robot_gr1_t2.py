import json
import os
import time

import numpy
from fourier_core.config.fi_config import gl_config
from fourier_core.logger.fi_logger import Logger
from fourier_core.operator import operator_joystick
from fourier_core.predefine.fi_deploy_mode import DeployMode
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_function_result import FunctionResult
from fourier_core.predefine.fi_joint_control_mode import JointControlMode
from fourier_core.predefine.fi_robot_work_space import RobotWorkSpace
from fourier_core.sensor.fi_sensor_fi_fse import SensorFIFSE

from fourier_grx.robot.gr1.fi_parallel_ankle_gr1_t2 import ParallelAnkle
from fourier_grx.robot.gr1.fi_parallel_head_gr1_t2 import ParallelHead
from fourier_grx.robot.gr1.fi_parallel_wrist_gr1_t2 import ParallelWrist
from fourier_grx.robot.gr1.fi_robot_gr1 import RobotGR1
from fourier_grx.robot.gr1.fi_robot_gr1_t1 import RobotGR1T1
from fourier_grx.robot.gr1.fi_robot_gr1_task import RobotGR1Task


class RobotGR1T2(RobotGR1T1):
    def __init__(self):
        super().__init__()

        # sensor
        # ...

        # actuator
        # ...

        # joint
        # ...

        # link
        # ...

        # end effector
        # ...

        # base and legs
        # ...

        # robot
        # ...

        # control algorithm
        # ...

        # task
        # ...

        # flag
        # ...

        # state estimator
        # ...

    def _init_sensor(self) -> FunctionResult:
        RobotGR1._init_sensor(self)

        # sensor
        """
        Note 2024-05-18:
        1. fi_fse direction should match the positive direction of the attached joint
        """

        # fmt: off
        self.number_of_sensor_fi_fse = 6 + 6 + 3
        sensor_fi_fse_ip = numpy.array(
            [
                # left leg
                "192.168.137.170", "192.168.137.171", "192.168.137.172", "192.168.137.173", "192.168.137.174", "192.168.137.175",
                # right leg
                "192.168.137.150", "192.168.137.151", "192.168.137.152", "192.168.137.153", "192.168.137.154", "192.168.137.155",
                # waist
                "192.168.137.190", "192.168.137.191", "192.168.137.192",
            ]
        )
        sensor_fi_fse_direction = numpy.array(
            [
                1.0, 1.0, -1.0, 1.0, 1.0, -1.0,  # left leg
                1.0, 1.0, 1.0, -1.0, -1.0, 1.0,  # right leg
                1.0, 1.0, 1.0,  # waist
            ]
        )
        sensor_fi_fse_reduction_ratio = numpy.array(
            [
                2.0, 2.77, 2.514, 1.0, 1.0, 1.0,  # left leg
                2.0, 2.77, 2.514, 1.0, 1.0, 1.0,  # right leg
                4.08, 1.0, 1.0,  # waist
            ]
        )
        # Jason 2024-01-22:
        # as the fi_fse have value jump from 0 <--> 360,
        # we set 180 raw angle value as target home angle
        sensor_fi_fse_sensor_offset = numpy.array(
            [
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # left leg
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # right leg
                0.0, 0.0, 0.0,  # waist
            ]
        )

        self.sensor_fi_fse = []
        for i in range(self.number_of_sensor_fi_fse):
            self.sensor_fi_fse.append(
                SensorFIFSE(
                    ip=sensor_fi_fse_ip[i],
                    direction=sensor_fi_fse_direction[i],
                    reduction_ratio=sensor_fi_fse_reduction_ratio[i],
                    sensor_offset=sensor_fi_fse_sensor_offset[i],
                )
            )

        self.indexes_of_joints_match_sensor_fi_fse = numpy.array(
            [
                0, 1, 2, 3, 4, 5,  # left leg
                6, 7, 8, 9, 10, 11,  # right leg
                12, 13, 14,  # waist
            ]
        )  # must match the number of sensor_fi_fse
        # fmt: on

        return FunctionResult.SUCCESS

    def _init_joint(self) -> FunctionResult:
        RobotGR1._init_joint(self)

        # joint -> joint urdf
        self.parallel_ankle_left = ParallelAnkle("left")
        self.parallel_ankle_right = ParallelAnkle("right")
        self.parallel_wrist_left = ParallelWrist("left")
        self.parallel_wrist_right = ParallelWrist("right")
        self.parallel_head = ParallelHead()

        # fmt: off
        self.indexes_of_lower_body_joints = numpy.array(
            [
                # left leg
                0, 1, 2, 3, 4, 5,
                # right leg
                6, 7, 8, 9, 10, 11,
            ]
        )
        self.number_of_lower_body_joints = len(self.indexes_of_lower_body_joints)

        self.indexes_of_upper_body_joints = numpy.array(
            [
                # waist
                12, 13, 14,
                # head
                15, 16, 17,
                # left arm
                18, 19, 20, 21, 22, 23, 24,
                # right arm
                25, 26, 27, 28, 29, 30, 31,
            ]
        )
        self.number_of_upper_body_joints = len(self.indexes_of_upper_body_joints)
        # fmt: on

        return FunctionResult.SUCCESS

    # =====================================================================================================

    def prepare(self) -> FunctionResult:
        Logger().print_trace("#################################")

        if (
            self.deploy_mode == DeployMode.DEFAULT
            or self.deploy_mode == DeployMode.DEVELOPER_MODE
            or self.deploy_mode == DeployMode.SDK_MODE
        ):
            joint_home_position = numpy.zeros(self.number_of_joint)

            # fi_fse --------------------------------------------------------------

            self._init_encoders()
            # get abs encoder value offset as offset
            abs_encoder_angle_offset = numpy.zeros(shape=self.number_of_sensor_fi_fse)
            for i in range(self.number_of_sensor_fi_fse):
                if self.sensor_fi_fse[i] is not None:
                    abs_encoder_angle_offset[i] = self.sensor_fi_fse[i].measured_angle

            joint_angle_offset = numpy.zeros(shape=self.number_of_joint)
            joint_angle_offset[0 : self.number_of_sensor_fi_fse] = abs_encoder_angle_offset[
                0 : self.number_of_sensor_fi_fse
            ].copy()

            print("joint_angle_offset = \n", numpy.round(joint_angle_offset, 1))

            # read current joint position
            # Jason 2024-01-26:
            # need to wait and send twice to allow data to upload
            self.actuator_group.upload()
            time.sleep(0.01)
            self.joint_group.update()
            time.sleep(0.01)
            self.actuator_group.upload()
            time.sleep(0.01)
            self.joint_group.update()

            for i in range(self.number_of_joint):
                self.joint_group_measured_position[i] = self.joints[i].measured_position
                self.joint_group_measured_velocity[i] = self.joints[i].measured_velocity
                self.joint_group_measured_kinetic[i] = self.joints[i].measured_kinetic

            print(
                "joint_group_measured_position (before calibration) = \n",
                numpy.round(self.joint_group_measured_position, 1),
            )

            for i in range(self.number_of_sensor_fi_fse):
                index_of_joint_match_sensor_fi_fse = self.indexes_of_joints_match_sensor_fi_fse[i]
                joint_home_position[index_of_joint_match_sensor_fi_fse] = (-1) * (
                    joint_angle_offset[i] - self.joint_group_measured_position[i]
                )

            # fi_fse --------------------------------------------------------------

            print("joint_home_position = \n", numpy.round(joint_home_position, 1))

            # change joint home position, based on encoder measured value
            for i in range(self.number_of_joint):
                if self.joints[i] is not None:
                    # use negative value to calibrate joint position
                    self.joints[i].home_position = joint_home_position[i]
                else:
                    pass  # use default home position are home position

            # update --------------------------------------------------------------

            # read current joint position
            # Jason 2024-01-26:
            # need to wait and send twice to allow data to upload
            self.actuator_group.upload()
            time.sleep(0.01)
            self.joint_group.update()
            time.sleep(0.01)
            self.actuator_group.upload()
            time.sleep(0.01)
            self.joint_group.update()

            for i in range(self.number_of_joint):
                self.joint_group_measured_position[i] = self.joints[i].measured_position
                self.joint_group_measured_velocity[i] = self.joints[i].measured_velocity
                self.joint_group_measured_kinetic[i] = self.joints[i].measured_kinetic

            print(
                "joint_group_measured_position (after calibration) = \n",
                numpy.round(self.joint_group_measured_position, 1),
            )

            Logger().print_trace("Finish joint home position calibration !")

        else:
            Logger().print_trace_warning("Unknown deploy mode: " + str(self.deploy_mode))

        return FunctionResult.SUCCESS

    @staticmethod
    def base_imu_transform(
        sensor_usb_imu_group_measured_quat,
        sensor_usb_imu_group_measured_angle,
        sensor_usb_imu_group_measured_angular_velocity,
        sensor_usb_imu_group_measured_linear_acceleration,
    ):
        # imu
        # base link imu is the first imu, change the value to match the upside down installation direction
        out_sensor_usb_imu_group_measured_quat = numpy.array(
            [
                -sensor_usb_imu_group_measured_quat[3],
                -sensor_usb_imu_group_measured_quat[2],
                -sensor_usb_imu_group_measured_quat[0],
                sensor_usb_imu_group_measured_quat[1],
            ]
        )

        out_sensor_usb_imu_group_measured_angle = numpy.array(
            [
                -(180 - sensor_usb_imu_group_measured_angle[0])
                if sensor_usb_imu_group_measured_angle[0] > 0
                else 180 + sensor_usb_imu_group_measured_angle[0],
                -sensor_usb_imu_group_measured_angle[1],
                sensor_usb_imu_group_measured_angle[2],
            ]
        )  # unit : deg

        out_sensor_usb_imu_group_measured_angular_velocity = numpy.array(
            [
                sensor_usb_imu_group_measured_angular_velocity[1],
                sensor_usb_imu_group_measured_angular_velocity[0],
                -sensor_usb_imu_group_measured_angular_velocity[2],
            ]
        )  # unit : deg/s

        out_sensor_usb_imu_group_measured_linear_acceleration = (
            numpy.array(
                [
                    sensor_usb_imu_group_measured_linear_acceleration[1],
                    sensor_usb_imu_group_measured_linear_acceleration[0],
                    -sensor_usb_imu_group_measured_linear_acceleration[2],
                ]
            )
            * -9.81
        )  # unit : m/s^2

        return (
            out_sensor_usb_imu_group_measured_quat,
            out_sensor_usb_imu_group_measured_angle,
            out_sensor_usb_imu_group_measured_angular_velocity,
            out_sensor_usb_imu_group_measured_linear_acceleration,
        )

    def control_loop_update_state(self) -> FunctionResult:
        """
        Changes:
        1. update imu data
        2. update base state
        3. update leg joint position, velocity, acceleration, torque
        4. update state estimator
        """

        RobotGR1.control_loop_update_state(self)

        # joint -> joint urdf
        # detect calibration
        if self.flag_calibration == FlagState.SET:
            """
            Notice:
            If the robot has not been calibrated, the ankle parallel calculation can have error.
            So, pass the calculation of the parallel ankle.
            """
            (
                self.joint_urdf_group_measured_position[4],
                self.joint_urdf_group_measured_position[5],
                self.joint_urdf_group_measured_velocity[4],
                self.joint_urdf_group_measured_velocity[5],
                self.joint_urdf_group_measured_kinetic[4],
                self.joint_urdf_group_measured_kinetic[5],
            ) = self.parallel_ankle_left.forward(
                joint_position_up_deg=self.joint_group_measured_position[4],
                joint_position_lower_deg=self.joint_group_measured_position[5],
                joint_velocity_up_deg=self.joint_group_measured_velocity[4],
                joint_velocity_lower_deg=self.joint_group_measured_velocity[5],
                joint_torque_up=self.joint_group_measured_kinetic[4],
                joint_torque_lower=self.joint_group_measured_kinetic[5],
            )

            (
                self.joint_urdf_group_measured_position[10],
                self.joint_urdf_group_measured_position[11],
                self.joint_urdf_group_measured_velocity[10],
                self.joint_urdf_group_measured_velocity[11],
                self.joint_urdf_group_measured_kinetic[10],
                self.joint_urdf_group_measured_kinetic[11],
            ) = self.parallel_ankle_right.forward(
                joint_position_up_deg=self.joint_group_measured_position[10],
                joint_position_lower_deg=self.joint_group_measured_position[11],
                joint_velocity_up_deg=self.joint_group_measured_velocity[10],
                joint_velocity_lower_deg=self.joint_group_measured_velocity[11],
                joint_torque_up=self.joint_group_measured_kinetic[10],
                joint_torque_lower=self.joint_group_measured_kinetic[11],
            )

            (
                self.joint_urdf_group_measured_position[23],
                self.joint_urdf_group_measured_position[24],
                self.joint_urdf_group_measured_velocity[23],
                self.joint_urdf_group_measured_velocity[24],
                self.joint_urdf_group_measured_kinetic[23],
                self.joint_urdf_group_measured_kinetic[24],
            ) = self.parallel_wrist_left.forward(
                joint_position_up_deg=self.joint_group_measured_position[23],
                joint_position_lower_deg=self.joint_group_measured_position[24],
                joint_velocity_up_deg=self.joint_group_measured_velocity[23],
                joint_velocity_lower_deg=self.joint_group_measured_velocity[24],
                joint_torque_up=self.joint_group_measured_kinetic[23],
                joint_torque_lower=self.joint_group_measured_kinetic[24],
            )

            (
                self.joint_urdf_group_measured_position[30],
                self.joint_urdf_group_measured_position[31],
                self.joint_urdf_group_measured_velocity[30],
                self.joint_urdf_group_measured_velocity[31],
                self.joint_urdf_group_measured_kinetic[30],
                self.joint_urdf_group_measured_kinetic[31],
            ) = self.parallel_wrist_right.forward(
                joint_position_up_deg=self.joint_group_measured_position[30],
                joint_position_lower_deg=self.joint_group_measured_position[31],
                joint_velocity_up_deg=self.joint_group_measured_velocity[30],
                joint_velocity_lower_deg=self.joint_group_measured_velocity[31],
                joint_torque_up=self.joint_group_measured_kinetic[30],
                joint_torque_lower=self.joint_group_measured_kinetic[31],
            )

            (
                self.joint_urdf_group_measured_position[15],
                self.joint_urdf_group_measured_position[16],
                self.joint_urdf_group_measured_velocity[15],
                self.joint_urdf_group_measured_velocity[16],
                self.joint_urdf_group_measured_kinetic[15],
                self.joint_urdf_group_measured_kinetic[16],
            ) = self.parallel_head.forward(
                joint_position_l_deg=self.joint_group_measured_position[15],
                joint_position_r_deg=self.joint_group_measured_position[16],
                joint_velocity_l_deg=self.joint_group_measured_velocity[15],
                joint_velocity_r_deg=self.joint_group_measured_velocity[16],
                joint_torque_l=self.joint_group_measured_kinetic[15],
                joint_torque_r=self.joint_group_measured_kinetic[16],
            )

        else:
            pass

        # fmt: off

        # imu
        # base link imu is the first imu, change the value to match the upside down installation direction
        (
            self.sensor_usb_imu_group_measured_quat[0:4],
            self.sensor_usb_imu_group_measured_angle[0:3],
            self.sensor_usb_imu_group_measured_angular_velocity[0:3],
            self.sensor_usb_imu_group_measured_linear_acceleration[0:3]
        ) = self.base_imu_transform(self.sensor_usb_imu_group_measured_quat,
                                    self.sensor_usb_imu_group_measured_angle,
                                    self.sensor_usb_imu_group_measured_angular_velocity,
                                    self.sensor_usb_imu_group_measured_linear_acceleration)

        # state estimation
        self.base_xyz = numpy.array([0.0, 0.0, 0.9])
        self.base_xyz_vel = numpy.array([0.0, 0.0, 0.0])

        # Note 2024-05-15:
        # use pybind function, must send copy() value, not raw value to it.
        leg_joint_position_radian = numpy.array(self.joint_group_measured_position_radian[:12]).copy()
        leg_joint_velocity_radian = numpy.array(self.joint_group_measured_velocity_radian[:12]).copy()
        leg_joint_acceleration_radian = numpy.zeros(12).copy()
        leg_joint_torque = numpy.array(self.joint_group_measured_kinetic[:12]).copy()
        imu_data = numpy.concatenate((
            self.sensor_usb_imu_group_measured_angle[[2, 1, 0]],
            self.sensor_usb_imu_group_measured_angular_velocity,
            self.sensor_usb_imu_group_measured_linear_acceleration * 10,
        )).copy()

        # print("leg_joint_position_radian = \n", leg_joint_position_radian)
        # print("leg_joint_velocity_radian = \n", leg_joint_velocity_radian)
        # print("leg_joint_acceleration_radian = \n", leg_joint_acceleration_radian)
        # print("leg_joint_torque = \n", leg_joint_torque)
        # print("imu_data = \n", imu_data)

        # leg_joint_position_radian = numpy.ones(12).copy()
        # leg_joint_velocity_radian = numpy.ones(12).copy()
        # leg_joint_acceleration_radian = numpy.ones(12).copy()
        # leg_joint_torque = numpy.ones(12).copy()
        # imu_data = numpy.ones(9).copy()
        # imu_data[8] = -9.81

        if self.state_estimator is not None:
            self.state_estimator.run(
                leg_joint_position_radian,
                leg_joint_velocity_radian,
                leg_joint_acceleration_radian,
                leg_joint_torque,
                imu_data,
            )

            base_state = self.state_estimator.get_base_state()

            self.base_xyz = base_state[0:3]
            self.base_xyz_vel = base_state[3:6]

        return FunctionResult.SUCCESS

    def control_loop_update_communication_joystick_button_triangle(self):
        # ^ button press
        if operator_joystick.button_triangle() == 1:
            self.task_command = RobotGR1Task.TASK_NOHLA_RL_WALK
            self.flag_task_command_update = FlagState.SET

            Logger().print_trace("task command: " + str(self.task_command.name))

    def control_loop_update_communication_joystick_button_circle(self):
        # o button press
        if operator_joystick.button_circle() == 1:
            self.task_command = RobotGR1Task.TASK_NOHLA_STAND
            self.flag_task_command_update = FlagState.SET

            Logger().print_trace("task command: " + str(self.task_command.name))

    def control_loop_set_control_developer_mode(self, control_dict=None) -> FunctionResult:
        if control_dict is None:
            return FunctionResult.SUCCESS

        target_control_mode = control_dict["control_mode"]
        target_kp = control_dict["kp"]
        target_kd = control_dict["kd"]
        target_position = control_dict["position"]

        # control_dict
        self.work_space = RobotWorkSpace.JOINT_SPACE

        # 1. joint control mode
        for i, joint in enumerate(self.joints):
            target_control_mode_i = target_control_mode[i]
            target_kp_i = target_kp[i]
            target_kd_i = target_kd[i]

            if target_control_mode_i == JointControlMode.POSITION:
                # urdf joint kp and kd -> joint kp and kd
                joint.set_target_control_mode(target_control_mode_i)
                joint.set_target_position_control_kp(target_kp_i)
                joint.set_target_velocity_control_kp(target_kd_i)
                joint.set_target_velocity_control_ki(0.0)

            if target_control_mode_i == JointControlMode.PD:
                # urdf joint kp and kd -> joint kp and kd
                joint.set_target_control_mode(target_control_mode_i)
                joint.set_target_pd_control_kp(target_kp_i)
                joint.set_target_pd_control_kd(target_kd_i)

            if target_control_mode_i == JointControlMode.POSITION_PSEUDO_PD:
                # urdf joint kp and kd -> joint kp and kd
                joint.set_target_control_mode(target_control_mode_i)
                target_pseudo_kp_i, target_pseudo_kd_i = joint.calculate_position_pseudo_pd_kp_kd(
                    target_kp_i, target_kd_i
                )
                joint.set_target_position_control_kp(target_pseudo_kp_i)
                joint.set_target_velocity_control_kp(target_pseudo_kd_i)
                joint.set_target_velocity_control_ki(0.0)

        # 4. position (unit: degree)
        joint_control_position = target_position.copy()

        (
            joint_control_position[4],
            joint_control_position[5],
            joint_control_position[10],
            joint_control_position[11],
        ) = self._calculate_parallel_ankle_inverse_kinematic(
            joint_control_position[4],
            joint_control_position[5],
            joint_control_position[10],
            joint_control_position[11],
        )

        (
            joint_control_position[23],
            joint_control_position[24],
            joint_control_position[30],
            joint_control_position[31],
        ) = self._calculate_parallel_wrist_inverse_kinematic(
            joint_control_position[23],
            joint_control_position[24],
            joint_control_position[30],
            joint_control_position[31],
        )

        (joint_control_position[15], joint_control_position[16], _, _, _, _) = self.parallel_head.inverse(
            joint_control_position[15], joint_control_position[16]
        )

        for i, joint in enumerate(self.joints):
            joint.set_target_position(joint_control_position[i])

        return FunctionResult.SUCCESS
