import json

import numpy
from fourier_core.actuator.fi_actuator_fi_fsa import ActuatorFIFSA
from fourier_core.actuator.fi_actuator_fi_fsa_group import ActuatorFIFSAGroup
from fourier_core.config.fi_config import gl_config
from fourier_core.end_effector.fi_end_effector_group import EndEffectorGroup
from fourier_core.joint.fi_joint_group import JointGroup
from fourier_core.joint.fi_joint_rotary import JointRotary
from fourier_core.logger.fi_logger import Logger
from fourier_core.operator import operator_joystick
from fourier_core.predefine.fi_deploy_mode import DeployMode
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_function_result import FunctionResult
from fourier_core.predefine.fi_robot_type import RobotType
from fourier_core.predefine.fi_robot_work_space import RobotWorkSpace
from fourier_core.predefine.fi_task_stage import TaskStage
from fourier_core.robot.fi_robot_base import RobotBaseTask
from fourier_core.robot.fi_robot_fftai import RobotFFTAI
from fourier_core.sensor.fi_sensor_usb_imu_hipnuc import SensorUSBIMUHipnuc
from fourier_grx.robot.gr1.fi_robot_gr1_algorithm import RobotGR1AlgorithmStandControlModel
from fourier_grx.robot.gr1.fi_robot_gr1_task import RobotGR1Task
from fourier_grx import __version__ as fourier_grx_version


class RobotGR1(RobotFFTAI):
    def __init__(self):
        super(RobotGR1, self).__init__()

        # info
        self.fourier_grx_version = fourier_grx_version

        # sensor
        self._init_sensor()

        # actuator
        self._init_actuator()

        # joint
        self._init_joint()

        # link
        self._init_link()

        # end effector
        self._init_end_effector()

        # base and legs
        self.base_xyz = numpy.array([0.0, 0.0, 0.9])
        self.base_xyz_vel = numpy.array([0.0, 0.0, 0.0])

        self.number_of_legs = 2
        self.legs_connect_position = [
            [0.3822, 0.2353, 0.0],  # left front leg
            [-0.3822, 0.2353, 0.0],  # left back leg
        ]

        # robot
        self._init_robot()

        # control algorithm
        self._init_algorithm()

        # task
        self._init_task()

        # share
        self._init_share()

        # flag
        self.flag_actuator_communication_time_out = numpy.ones(shape=self.number_of_actuator) * FlagState.CLEAR
        self.actuator_communication_check_count = numpy.zeros(shape=self.number_of_actuator)

    def _init_sensor(self) -> FunctionResult:
        # fmt: off
        if gl_config.parameters.get("sensor_usb_imu") is not None:
            self.sensor_usb_imus = []

            sensor_usb_imus_usb = gl_config.parameters["sensor_usb_imu"].get("usb")

            self.number_of_sensor_usb_imu = len(sensor_usb_imus_usb)

            for i in range(self.number_of_sensor_usb_imu):
                usb = sensor_usb_imus_usb[i] if sensor_usb_imus_usb is not None else None

                self.sensor_usb_imus.append(
                    SensorUSBIMUHipnuc(usb=usb, ),
                )

        self.sensor_usb_imu_group_measured_quat = numpy.zeros(
            self.number_of_sensor_usb_imu * 4
        )
        self.sensor_usb_imu_group_measured_angle = numpy.zeros(
            self.number_of_sensor_usb_imu * 3
        )
        self.sensor_usb_imu_group_measured_angular_velocity = numpy.zeros(
            self.number_of_sensor_usb_imu * 3
        )
        self.sensor_usb_imu_group_measured_linear_acceleration = numpy.zeros(
            self.number_of_sensor_usb_imu * 3
        )
        # fmt: on

        return FunctionResult.SUCCESS

    def _init_actuator(self) -> FunctionResult:
        # fmt: off
        if gl_config.parameters.get("actuator") is not None:
            self.actuators = []

            actuators_ip = gl_config.parameters["actuator"].get("ip")
            actuators_type = gl_config.parameters["actuator"].get("type")

            self.number_of_actuator = len(actuators_ip)

            for i in range(self.number_of_actuator):
                ip = actuators_ip[i] if actuators_ip is not None else None
                type = actuators_type[i] if actuators_type is not None else None

                self.actuators.append(
                    ActuatorFIFSA(ip=ip, type=type, )
                )

        self.actuator_group = ActuatorFIFSAGroup(self.actuators, use_fast=True)
        self.actuator_group_measured_position = [0.0] * self.number_of_actuator
        self.actuator_group_measured_velocity = [0.0] * self.number_of_actuator
        self.actuator_group_measured_kinetic = [0.0] * self.number_of_actuator
        self.actuator_group_measured_current = [0.0] * self.number_of_actuator
        # fmt: on

        return FunctionResult.SUCCESS

    def _init_joint(self) -> FunctionResult:
        # fmt: off
        self.number_of_joint = 6 + 6 + 3 + 3 + 7 + 7
        self.joints_direction = numpy.array([
            -1.0, 1.0, 1.0, -1.0, -1.0, 1.0,  # left leg
            -1.0, 1.0, -1.0, 1.0, 1.0, -1.0,  # right leg
            -1.0, -1.0, -1.0,  # waist
            -1.0, -1.0, -1.0,  # head
            -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0,  # left arm
            1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  # right arm
        ])
        self.joint_home_position = numpy.array([
            0, 0, 0, 0, 0, 0,  # left leg
            0, 0, 0, 0, 0, 0,  # right leg
            0, 0, 0,  # waist
            0, 0, 0,  # head
            0, 0, 0, 0, 0, 0, 0,  # left arm
            0, 0, 0, 0, 0, 0, 0,  # right arm
        ]) * 180.0 / numpy.pi  # unit : degree
        self.joint_min_position = numpy.array([
            -0.09, -0.7, -1.75, -0.09, -1.05, -0.44,  # left leg(6)
            -0.09, -0.7, -1.75, -0.09, -1.05, -0.44,  # right leg(6)
            -1.05, -0.52, -0.7,  # waist(3)
            -2.71, -0.35, -0.52,  # head(3)
            -2.79, -0.57, -2.97, -2.27, -2.97, -0.61, -0.61,  # left arm(7)
            -2.79, -0.57, -2.97, -2.27, -2.97, -0.61, -0.61,  # right arm(7)
        ]) * 180.0 / numpy.pi  # unit : degree
        self.joint_max_position = numpy.array([
            0.79, 0.7, 0.7, 1.92, 0.52, 0.44,  # left leg(6)
            0.09, 0.7, 0.7, 1.92, 0.52, 0.44,  # right leg(6)
            1.05, 1.22, 0.7,  # waist(3)
            2.71, 0.35, 0.35,  # head(3)
            1.92, 3.27, 2.97, 2.27, 2.97, 0.61, 0.61,  # left arm(7)
            1.92, 0.57, 2.97, 2.27, 2.97, 0.61, 0.61,  # right arm(7)
        ]) * 180.0 / numpy.pi  # unit : degree
        self.joint_reduction_ratio = numpy.array([
            31, 51, 7, 7, 36, 36,  # left leg
            31, 51, 7, 7, 36, 36,  # right leg
            51, 51, 51,  # waist
            51, 51, 51,  # head
            80, 80, 100, 100, 31, 31, 31,  # left arm
            80, 80, 100, 100, 31, 31, 31,  # right arm

            # Jason 2024-01-19:
            # FSA 输出的是执行器末端角度，已经计算过减速比了
            # 1, 1, 1, 1, 1, 1,  # left leg
            # 1, 1, 1, 1, 1, 1,  # right leg
            # 1, 1, 1,  # waist
            # 1, 1, 1,  # head
            # 1, 1, 1, 1, 1, 1, 1,  # left arm
            # 1, 1, 1, 1, 1, 1, 1,  # right arm
        ])
        self.joint_kinematic_reduction_ratio = numpy.array([
            # Jason 2024-01-19:
            # FSA 输出的是执行器末端角度，已经计算过减速比了
            1, 1, 1, 1, 1, 1,  # left leg
            1, 1, 1, 1, 1, 1,  # right leg
            1, 1, 1,  # waist
            1, 1, 1,  # head
            1, 1, 1, 1, 1, 1, 1,  # left arm
            1, 1, 1, 1, 1, 1, 1,  # right arm
        ])
        self.joint_kinetic_reduction_ratio = numpy.array([
            0.121, 0.067, 0.26, 0.26, 0.06, 0.06,  # left leg
            0.121, 0.067, 0.26, 0.26, 0.06, 0.06,  # right leg
            0.067, 0.067, 0.067,  # waist
            0.06, 0.06, 0.06,  # head
            0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06,  # left arm
            0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06,  # right arm
        ]) * self.joint_reduction_ratio

        self.joints = []
        for i in range(self.number_of_joint):
            self.joints.append(
                JointRotary(
                    actuator=self.actuators[i],
                    direction=self.joints_direction[i],
                    home_position=self.joint_home_position[i],
                    min_position=self.joint_min_position[i],
                    max_position=self.joint_max_position[i],
                    kinematic_reduction_ratio=self.joint_kinematic_reduction_ratio[i],
                    kinetic_reduction_ratio=self.joint_kinetic_reduction_ratio[i],
                )
            )

        # default pid
        self.joint_position_control_kp = numpy.array([
            0.9971, 1.0228, 1.0606, 1.0606, 0.5091, 0.5091,  # left leg
            0.9971, 1.0228, 1.0606, 1.0606, 0.5091, 0.5091,  # right leg
            1.0228, 1.0228, 1.0228,  # waist
            0.1000, 0.1000, 0.1000,  # head
            1.0016, 1.0016, 1.0041, 1.0041, 1.0041, 0.1000, 0.1000,  # left arm
            1.0016, 1.0016, 1.0041, 1.0041, 1.0041, 0.1000, 0.1000,  # right arm
        ])
        self.joint_velocity_control_kp = numpy.array([
            0.0445, 0.0299, 0.2634, 0.2634, 0.0042, 0.0042,  # left leg
            0.0445, 0.0299, 0.2634, 0.2634, 0.0042, 0.0042,  # right leg
            0.0299, 0.0299, 0.0299,  # waist
            0.0050, 0.0050, 0.0050,  # head
            0.0037, 0.0037, 0.0039, 0.0039, 0.0039, 0.0050, 0.0050,  # left arm
            0.0037, 0.0037, 0.0039, 0.0039, 0.0039, 0.0050, 0.0050,  # right arm
        ])
        self.joint_pd_control_kp = numpy.array([
            251.625, 362.5214, 200, 200, 10.9805, 10.9805,  # left leg
            251.625, 362.5214, 200, 200, 10.9805, 10.9805,  # right leg
            362.5214, 362.5214, 362.5214,  # waist
            10.0, 10.0, 10.0,  # head
            92.85, 92.85, 112.06, 112.06, 112.06, 10.0, 10.0,  # left arm
            92.85, 92.85, 112.06, 112.06, 112.06, 10.0, 10.0,  # right arm
        ])
        self.joint_pd_control_kd = numpy.array([
            14.72, 10.0833, 11, 11, 0.5991, 0.5991,  # left leg
            14.72, 10.0833, 11, 11, 0.5991, 0.5991,  # right leg
            10.0833, 10.0833, 10.0833,  # waist
            1.0, 1.0, 1.0,  # head
            2.575, 2.575, 3.1, 3.1, 3.1, 1.0, 1.0,  # left arm
            2.575, 2.575, 3.1, 3.1, 3.1, 1.0, 1.0,  # right arm
        ])

        for i in range(self.number_of_joint):
            # use position control as default when power on
            self.joints[i].set_target_position_control_kp(self.joint_position_control_kp[i])
            self.joints[i].set_target_velocity_control_kp(self.joint_velocity_control_kp[i])
            self.joints[i].set_target_velocity_control_ki(0)

        self.joint_group = JointGroup(self.joints, self.actuator_group)
        self.joint_group_measured_position = numpy.array([0.0] * self.number_of_joint)
        self.joint_group_measured_velocity = numpy.array([0.0] * self.number_of_joint)
        self.joint_group_measured_kinetic = numpy.array([0.0] * self.number_of_joint)

        # joint -> joint urdf
        self.joint_urdf_group_measured_position = numpy.array([0.0] * self.number_of_joint)
        self.joint_urdf_group_measured_velocity = numpy.array([0.0] * self.number_of_joint)
        self.joint_urdf_group_measured_kinetic = numpy.array([0.0] * self.number_of_joint)

        self.indexes_of_lower_body_joints = numpy.array([
            # left leg
            0, 1, 2, 3, 4, 5,
            # right leg
            6, 7, 8, 9, 10, 11,
        ])
        self.number_of_lower_body_joints = len(self.indexes_of_lower_body_joints)

        self.indexes_of_upper_body_joints = numpy.array([
            # waist
            12, 13, 14,
            # head
            15, 16, 17,
            # left arm
            18, 19, 20, 21, 22, 23, 24,
            # right arm
            25, 26, 27, 28, 29, 30, 31,
        ])
        self.number_of_upper_body_joints = len(self.indexes_of_upper_body_joints)
        # fmt: on

        return FunctionResult.SUCCESS

    def _init_link(self) -> FunctionResult:
        self.number_of_link = 0
        self.links = None

        return FunctionResult.SUCCESS

    def _init_end_effector(self) -> FunctionResult:
        self.number_of_end_effector = 0
        self.end_effectors = None

        self.end_effector_group = EndEffectorGroup()
        self.end_effector_group_measured_position = numpy.array([[0.0] * 6] * self.number_of_end_effector)
        self.end_effector_group_measured_velocity = numpy.array([[0.0] * 6] * self.number_of_end_effector)
        self.end_effector_group_measured_kinetic = numpy.array([[0.0] * 6] * self.number_of_end_effector)

        return FunctionResult.SUCCESS

    def _init_robot(self) -> FunctionResult:
        self.robot_name = gl_config.parameters["robot"].get("name", "GR1")
        self.robot_mechanism_type = gl_config.parameters["robot"].get("mechanism", "")
        self.robot_type = RobotType.GR1

        return FunctionResult.SUCCESS

    def _init_algorithm(self) -> FunctionResult:
        self.algorithm_stand_control_model = RobotGR1AlgorithmStandControlModel(
            dt=self.control_period,
        )
        return FunctionResult.SUCCESS

    def _init_task(self) -> FunctionResult:
        self.tasks.extend(
            [
                RobotGR1Task.TASK_STAND_CONTROL,
                RobotGR1Task.TASK_STAND_PD_CONTROL,
            ]
        )

        self.task_algorithm_models.update(
            {
                RobotGR1Task.TASK_STAND_CONTROL: self.algorithm_stand_control_model,
                RobotGR1Task.TASK_STAND_PD_CONTROL: self.algorithm_stand_control_model,
            }
        )

        self.task_functions.update(
            {
                RobotGR1Task.TASK_STAND_CONTROL: self.task_stand_control,
                RobotGR1Task.TASK_STAND_PD_CONTROL: self.task_stand_pd_control,
            }
        )

        return FunctionResult.SUCCESS

    def _init_share(self) -> FunctionResult:
        # imu
        self.share_sensor_usb_imu_group_measured_quat = numpy.zeros_like(self.sensor_usb_imu_group_measured_quat)
        self.share_sensor_usb_imu_group_measured_angle = numpy.zeros_like(self.sensor_usb_imu_group_measured_angle)
        self.share_sensor_usb_imu_group_measured_angular_velocity = numpy.zeros_like(
            self.sensor_usb_imu_group_measured_angular_velocity
        )
        self.share_sensor_usb_imu_group_measured_linear_acceleration = numpy.zeros_like(
            self.sensor_usb_imu_group_measured_linear_acceleration
        )

        # joint (replace by joint_urdf)
        self.share_joint_urdf_group_measured_position = numpy.zeros_like(self.joint_urdf_group_measured_position)
        self.share_joint_urdf_group_measured_velocity = numpy.zeros_like(self.joint_urdf_group_measured_velocity)
        self.share_joint_urdf_group_measured_kinetic = numpy.zeros_like(self.joint_urdf_group_measured_kinetic)

        # end effector
        self.share_end_effector_measured_position = numpy.zeros_like(self.end_effector_group_measured_position)
        self.share_end_effector_measured_velocity = numpy.zeros_like(self.end_effector_group_measured_velocity)
        self.share_end_effector_measured_kinetic = numpy.zeros_like(self.end_effector_group_measured_kinetic)

        # base
        self.share_base_xyz = numpy.zeros_like(self.base_xyz)
        self.share_base_xyz_vel = numpy.zeros_like(self.base_xyz_vel)

        return FunctionResult.SUCCESS

    # =====================================================================================================

    def init(self) -> FunctionResult:
        super().init()

        return FunctionResult.SUCCESS

    def prepare(self) -> FunctionResult:
        super().prepare()

        return FunctionResult.SUCCESS

    def ready_state(self) -> FunctionResult:
        # set task
        self.flag_task_command_update = FlagState.SET
        self.task_command = RobotGR1Task.TASK_STAND_CONTROL

        return FunctionResult.SUCCESS

    def control_loop_update_state(self) -> FunctionResult:
        # fmt: off

        # sensor
        # Note 2024-01-26:
        # no need to read fi_fse sensor in every loop
        # fi_fse
        # for i in range(self.number_of_sensor_fi_fse):
        #     self.sensor_fi_fse[i].upload()

        # imu
        for i in range(self.number_of_sensor_usb_imu):
            self.sensor_usb_imus[i].upload()

        # IMU x 轴朝向 x，y 轴朝向 y
        # roll x, pitch y

        for i in range(self.number_of_sensor_usb_imu):
            self.sensor_usb_imu_group_measured_quat[(i + 0) * 4: (i + 1) * 4] = (
                self.sensor_usb_imus[i].get_measured_quat()
            )
            self.sensor_usb_imu_group_measured_angle[(i + 0) * 3: (i + 1) * 3] = (
                self.sensor_usb_imus[i].get_measured_angle()
            )
            self.sensor_usb_imu_group_measured_angular_velocity[(i + 0) * 3: (i + 1) * 3] = (
                self.sensor_usb_imus[i].get_measured_angular_velocity()
            )
            self.sensor_usb_imu_group_measured_linear_acceleration[(i + 0) * 3: (i + 1) * 3] = (
                self.sensor_usb_imus[i].get_measured_acceleration()
            )

        # 说明：根据 workspace 的区别，尽可能减少 get_cvp (upload) 指令的发送次数，提高控制频率
        # if self.work_space == RobotWorkSpace.NONE:
        #     self.actuator_group.upload()
        #
        # elif self.work_space == RobotWorkSpace.ACTUATOR_SPACE or \
        #         self.work_space == RobotWorkSpace.JOINT_SPACE or \
        #         self.work_space == RobotWorkSpace.TASK_SPACE:
        #     for i in range(self.number_of_actuator):
        #         if self.actuators[i].mode_of_operation == ActuatorModeOfOperation.POSITION \
        #                 or self.actuators[i].mode_of_operation == ActuatorModeOfOperation.VELOCITY \
        #                 or self.actuators[i].mode_of_operation == ActuatorModeOfOperation.KINETIC:
        #             # 如果执行器都运行在 POSITION / VELOCITY / KINETIC 模式，那么就不需要从硬件端再次获取数据
        #             pass
        #         else:
        #             self.actuator_group.upload()
        #             break
        #
        #     pass
        #
        # else:
        #     self.actuator_group.upload()

        # actuator
        # time cost: 0.1 - 0.3ms, using concurrency
        if self.actuator_group is not None:
            self.actuator_group.upload()

        for i in range(self.number_of_actuator):
            self.actuator_group_measured_position[i] = self.actuators[i].measured_position
            self.actuator_group_measured_velocity[i] = self.actuators[i].measured_velocity
            self.actuator_group_measured_kinetic[i] = self.actuators[i].measured_kinetic
            self.actuator_group_measured_current[i] = self.actuators[i].measured_current

        # joint
        if self.joint_group is not None:
            self.joint_group.update()

        for i in range(self.number_of_joint):
            self.joint_group_measured_position[i] = self.joints[i].measured_position
            self.joint_group_measured_velocity[i] = self.joints[i].measured_velocity
            self.joint_group_measured_kinetic[i] = self.joints[i].measured_kinetic

        # joint -> joint urdf
        self.joint_urdf_group_measured_position = (
            self.joint_group_measured_position.copy()
        )
        self.joint_urdf_group_measured_velocity = (
            self.joint_group_measured_velocity.copy()
        )
        self.joint_urdf_group_measured_kinetic = (
            self.joint_group_measured_kinetic.copy()
        )

        # end effector
        if self.end_effector_group is not None:
            self.end_effector_group.update()

        for i in range(self.number_of_end_effector):
            self.end_effector_group_measured_position[i] = (
                self.end_effectors[i].measured_position
            )
            self.end_effector_group_measured_velocity[i] = (
                self.end_effectors[i].measured_velocity
            )
            self.end_effector_group_measured_kinetic[i] = (
                self.end_effectors[i].measured_kinetic
            )
        # fmt: on

        return FunctionResult.SUCCESS

    def control_loop_update_share(self) -> FunctionResult.SUCCESS:
        # imu
        self.share_sensor_usb_imu_group_measured_quat = self.sensor_usb_imu_group_measured_quat.copy()
        self.share_sensor_usb_imu_group_measured_angle = self.sensor_usb_imu_group_measured_angle.copy()
        self.share_sensor_usb_imu_group_measured_angular_velocity = (
            self.sensor_usb_imu_group_measured_angular_velocity.copy()
        )
        self.share_sensor_usb_imu_group_measured_linear_acceleration = (
            self.sensor_usb_imu_group_measured_linear_acceleration.copy()
        )

        # joint (replace by joint_urdf)
        self.share_joint_urdf_group_measured_position = self.joint_urdf_group_measured_position.copy()
        self.share_joint_urdf_group_measured_velocity = self.joint_urdf_group_measured_velocity.copy()
        self.share_joint_urdf_group_measured_kinetic = self.joint_urdf_group_measured_kinetic.copy()

        # end effector
        self.share_end_effector_group_measured_position = self.end_effector_group_measured_position.copy()
        self.share_end_effector_group_measured_velocity = self.end_effector_group_measured_velocity.copy()
        self.share_end_effector_group_measured_kinetic = self.end_effector_group_measured_kinetic.copy()

        # base
        self.share_base_xyz = self.base_xyz.copy()
        self.share_base_xyz_vel = self.base_xyz_vel.copy()

        return FunctionResult.SUCCESS

    def control_loop_update_command_select(self) -> FunctionResult:
        result = super().control_loop_update_command_select()

        if result == FunctionResult.SUCCESS:
            return FunctionResult.SUCCESS

        # task command select
        for item in RobotGR1Task:
            if self.task_command == item:
                task_algorithm_model = self.task_algorithm_models[item]

                if task_algorithm_model is not None:
                    if self.task_state != self.task_command:
                        task_algorithm_model.stage = TaskStage.STAGE_INIT
                    else:
                        task_algorithm_model.stage = TaskStage.STAGE_START

                    return FunctionResult.SUCCESS
                else:
                    pass

        return FunctionResult.FAIL

    def control_loop_get_state(self) -> dict:
        if (
            self.deploy_mode == DeployMode.DEFAULT
            or self.deploy_mode == DeployMode.DEVELOPER_MODE
            or self.deploy_mode == DeployMode.SDK_MODE
        ):
            self.control_loop_get_state_developer_mode()

        else:
            Logger().print_trace_warning("Unknown deploy mode: " + str(self.deploy_mode))

        return self.state_dict

    def control_loop_get_state_developer_mode(self) -> dict:
        self.state_dict.update(
            {
                # imu
                "imu_quat": self.share_sensor_usb_imu_group_measured_quat,
                "imu_euler_angle": self.share_sensor_usb_imu_group_measured_angle,
                "imu_angular_velocity": self.share_sensor_usb_imu_group_measured_angular_velocity,
                "imu_acceleration": self.share_sensor_usb_imu_group_measured_linear_acceleration,
                # joint (replace by joint_urdf)
                "joint_position": self.share_joint_urdf_group_measured_position,
                "joint_velocity": self.share_joint_urdf_group_measured_velocity,
                "joint_kinetic": self.share_joint_urdf_group_measured_kinetic,
                # base
                "base_estimate_xyz": self.share_base_xyz,
                "base_estimate_xyz_vel": self.share_base_xyz_vel,
            }
        )

        return self.state_dict

    def control_loop_algorithm(self) -> FunctionResult:
        result = super().control_loop_algorithm()

        if result == FunctionResult.SUCCESS:
            return FunctionResult.SUCCESS

        for item in RobotGR1Task:
            if self.task_state == item:
                # update task in process flag
                self.task_command_in_process = FlagState.SET

                # execute task algorithm
                task_function = self.task_functions[item]

                if task_function is not None:
                    task_function()
                else:
                    pass

                return FunctionResult.SUCCESS

        return FunctionResult.FAIL

    def control_loop_update_communication_print_selected_task(self):
        super().control_loop_update_communication_print_selected_task()

        for item in RobotGR1Task:
            if self.task_select == item:
                Logger().print_trace("task select: " + str(self.task_select.name))
                break

    def control_loop_update_communication_print_command_task(self):
        super().control_loop_update_communication_print_command_task()

        for item in RobotGR1Task:
            if self.task_command == item:
                Logger().print_trace("task command: " + str(self.task_command.name))
                break

    def control_loop_update_communication_joystick_button_logo(self):
        super().control_loop_update_communication_joystick_button_logo()

    def control_loop_update_communication_joystick_button_triangle(self):
        super().control_loop_update_communication_joystick_button_triangle()

    def control_loop_update_communication_joystick_button_circle(self):
        # o button press
        if operator_joystick.button_circle() == 1:
            if self.joint_use_dic:
                self.task_command = RobotGR1Task.TASK_STAND_PD_CONTROL
            else:
                self.task_command = RobotGR1Task.TASK_STAND_CONTROL

            self.flag_task_command_update = FlagState.SET

            Logger().print_trace("task command: " + str(self.task_command.name))

    def control_loop_update_communication_joystick_button_square(self):
        super().control_loop_update_communication_joystick_button_square()

    def control_loop_update_communication_joystick_button_cross(self):
        super().control_loop_update_communication_joystick_button_cross()

    def task_set_home(self):
        # fi_fse --------------------------------------------------------------
        map_fi_fses_angle_value = {}

        for i in range(self.number_of_sensor_fi_fse):
            if self.sensor_fi_fse[i] is not None:
                ip = self.sensor_fi_fse[i].ip
                sensor_offset = self.sensor_fi_fse[i].set_home()

                map_fi_fses_angle_value[ip] = sensor_offset

        Logger().print_trace("map_fi_fses_angle_value = \n", str(map_fi_fses_angle_value))

        # 保存 fi_fse 的角度值到文件
        Logger().print_trace("save fi_fse value to file")
        json_fi_fses_angle_value = json.dumps(map_fi_fses_angle_value, indent=4, separators=(",", ": "))
        sensor_abs_encoder_data_path = gl_config.parameters["sensor_abs_encoder"].get(
            "data_path", "./sensor_offset.json"
        )

        with open(sensor_abs_encoder_data_path, "w") as file:
            file.write(json_fi_fses_angle_value)
        # fi_fse --------------------------------------------------------------

        # change task_command and task_state
        self.task_command = RobotBaseTask.TASK_NONE
        self.task_state = RobotBaseTask.TASK_NONE

        return FunctionResult.SUCCESS

    def task_stand_control(self):
        # joint -> urdf
        joint_measured_position_urdf = self.joint_urdf_group_measured_position.copy() * numpy.pi / 180.0  # unit : rad
        joint_measured_velocity_urdf = self.joint_urdf_group_measured_velocity.copy() * numpy.pi / 180.0  # unit : rad/s

        # algorithm
        work_space, control_mode, joint_target_position_urdf = self.algorithm_stand_control_model.run(
            joint_measured_position_urdf=joint_measured_position_urdf,
            joint_measured_velocity_urdf=joint_measured_velocity_urdf,
        )

        # urdf -> joint
        joint_target_position_urdf = joint_target_position_urdf / numpy.pi * 180.0  # unit : deg
        joint_target_position_real = joint_target_position_urdf.copy()

        if work_space == RobotWorkSpace.ACTUATOR_SPACE:
            self.work_space = work_space
            for i in range(self.number_of_actuator):
                self.actuators[i].set_target_control_mode(control_mode[i])

        elif work_space == RobotWorkSpace.JOINT_SPACE:
            self.work_space = work_space
            for i in range(self.number_of_joint):
                self.joints[i].set_target_control_mode(control_mode[i])
                self.joints[i].set_target_position(joint_target_position_real[i])

        else:
            Logger().print_trace_error("algorithm_stand_control() unknown work_space")

        return FunctionResult.SUCCESS

    def task_stand_pd_control(self):
        return FunctionResult.SUCCESS
