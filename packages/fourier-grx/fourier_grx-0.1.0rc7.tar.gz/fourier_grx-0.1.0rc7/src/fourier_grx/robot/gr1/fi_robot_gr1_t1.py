import json
import os
import time

import numpy
from fourier_core.actuator.fi_actuator_fi_fsa import ActuatorFIFSA
from fourier_core.actuator.fi_actuator_fi_fsa_group import ActuatorFIFSAGroup
from fourier_core.actuator.fi_actuator_fi_fsa_type import ActuatorFSAType
from fourier_core.config.fi_config import gl_config
from fourier_core.logger.fi_logger import Logger
from fourier_core.operator import operator_joystick
from fourier_core.predefine.fi_deploy_mode import DeployMode
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_function_result import FunctionResult
from fourier_core.predefine.fi_joint_control_mode import JointControlMode
from fourier_core.predefine.fi_robot_work_space import RobotWorkSpace
from fourier_core.robot.fi_robot_base import RobotBaseTask
from fourier_core.sensor.fi_sensor_fi_fse import SensorFIFSE

from fourier_grx.robot.gr1.fi_parallel_ankle_gr1_t1 import ParallelAnkle
from fourier_grx.robot.gr1.fi_parallel_wrist_gr1_t1 import ParallelWrist
from fourier_grx.robot.gr1.fi_robot_gr1 import RobotGR1
from fourier_grx.robot.gr1.fi_robot_gr1_algorithm import (
    RobotGR1AlgorithmBasicControlModel,
)
from fourier_grx.robot.gr1.fi_robot_gr1_task import RobotGR1Task
from fourier_grx.robot.gr1_nohla.fi_robot_gr1_nohla_algorithm import (
    RobotGR1NohlaAlgorithmStandControlModel,
)
from fourier_grx.robot.gr1_nohla.fi_robot_gr1_nohla_algorithm_rl import (
    RobotGR1NohlaAlgorithmRLWalkControlModel,
)
from fourier_grx.robot.gr1_simple.fi_robot_gr1_simple_algorithm_rl import (
    RobotGR1SimpleAlgorithmRLAirtimeControlModel,
    RobotGR1SimpleAlgorithmRLAirtimeStackControlModel,
)
from fourier_grx.tools.load_sensor_offset import load_sensor_offset_dict


class RobotGR1T1(RobotGR1):
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
        self.state_estimator = None
        try:
            if gl_config.parameters["robot"].get("state_estimator") is not None:
                if gl_config.parameters["robot"]["state_estimator"]["enable"] is True:
                    from example import Estimator

                    self.state_estimator = Estimator()
                    state_estimator_model_file_path = gl_config.parameters["robot"]["state_estimator"]["path"]

                    # get current file path
                    current_workspace_path = os.getcwd()
                    model_file_path = current_workspace_path + state_estimator_model_file_path
                    Logger().print_trace_highlight("state_estimator model_file_path = ", model_file_path)

                    init_result = self.state_estimator.init(model_file_path, 0.0025)
                    if init_result is False:
                        Logger().print_trace_error("state_estimator has no model file loaded!!!")
                        exit(0)
        except Exception:
            pass

    def _init_sensor(self) -> FunctionResult:
        RobotGR1._init_sensor(self)

        # fmt: off
        self.number_of_sensor_fi_fse = 6 + 6 + 3
        sensor_fi_fse_ip = numpy.array([
            # left leg
            "192.168.137.170", "192.168.137.171", "192.168.137.172", "192.168.137.173", "192.168.137.174",
            "192.168.137.175",
            # right leg
            "192.168.137.150", "192.168.137.151", "192.168.137.152", "192.168.137.153", "192.168.137.154",
            "192.168.137.155",
            # waist
            "192.168.137.190", "192.168.137.191", "192.168.137.192",
        ])
        sensor_fi_fse_direction = numpy.array([
            1.0, 1.0, -1.0, 1.0, 1.0, 1.0,  # left leg
            1.0, 1.0, 1.0, -1.0, -1.0, 1.0,  # right leg
            1.0, 1.0, 1.0,  # waist
        ])
        sensor_fi_fse_reduction_ratio = numpy.array([
            2.0, 2.77, 2.514, 1.0, 1.0, 1.0,  # left leg
            2.0, 2.77, 2.514, 1.0, 1.0, 1.0,  # right leg
            4.08, 1.0, 1.0,  # waist
        ])
        # Jason 2024-01-22:
        # as the fi_fse have value jump from 0 <--> 360,
        # we set 180 raw angle value as target home angle
        sensor_fi_fse_sensor_offset = numpy.array([
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # left leg
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # right leg
            0.0, 0.0, 0.0,  # waist
        ])

        self.sensor_fi_fse = []
        for i in range(self.number_of_sensor_fi_fse):
            self.sensor_fi_fse.append(
                SensorFIFSE(ip=sensor_fi_fse_ip[i],
                            direction=sensor_fi_fse_direction[i],
                            reduction_ratio=sensor_fi_fse_reduction_ratio[i],
                            sensor_offset=sensor_fi_fse_sensor_offset[i])
            )

        self.indexes_of_joints_match_sensor_fi_fse = numpy.array([
            0, 1, 2, 3, 4, 5,  # left leg
            6, 7, 8, 9, 10, 11,  # right leg
            12, 13, 14,  # waist
        ])  # must match the number of sensor_fi_fse
        # fmt: on

        return FunctionResult.SUCCESS

    def _init_actuator(self) -> FunctionResult:
        # fmt: off
        self.actuators = []

        actuators_ip = [
            # left leg
            "192.168.137.70", "192.168.137.71", "192.168.137.72", "192.168.137.73", "192.168.137.74", "192.168.137.75",
            # right leg
            "192.168.137.50", "192.168.137.51", "192.168.137.52", "192.168.137.53", "192.168.137.54", "192.168.137.55",
            # waist
            "192.168.137.90", "192.168.137.91", "192.168.137.92",
            # head
            "192.168.137.93", "192.168.137.94", "192.168.137.95",
            # left arm
            "192.168.137.10", "192.168.137.11", "192.168.137.12", "192.168.137.13", "192.168.137.14", "192.168.137.15",
            "192.168.137.16",
            # right arm
            "192.168.137.30", "192.168.137.31", "192.168.137.32", "192.168.137.33", "192.168.137.34", "192.168.137.35",
            "192.168.137.36",
        ]
        actuators_type = [
            # left leg
            ActuatorFSAType.FSA_TYPE_802030,
            ActuatorFSAType.FSA_TYPE_601750,
            ActuatorFSAType.FSA_TYPE_1307E,
            ActuatorFSAType.FSA_TYPE_1307E,
            ActuatorFSAType.FSA_TYPE_36B36E,
            ActuatorFSAType.FSA_TYPE_36B36E,
            # right leg
            ActuatorFSAType.FSA_TYPE_802030,
            ActuatorFSAType.FSA_TYPE_601750,
            ActuatorFSAType.FSA_TYPE_1307E,
            ActuatorFSAType.FSA_TYPE_1307E,
            ActuatorFSAType.FSA_TYPE_36B36E,
            ActuatorFSAType.FSA_TYPE_36B36E,
            # waist
            ActuatorFSAType.FSA_TYPE_601750,
            ActuatorFSAType.FSA_TYPE_601750,
            ActuatorFSAType.FSA_TYPE_601750,
            # head
            ActuatorFSAType.FSA_TYPE_250830,
            ActuatorFSAType.FSA_TYPE_250830,
            ActuatorFSAType.FSA_TYPE_250830,
            # left arm
            ActuatorFSAType.FSA_TYPE_361480,
            ActuatorFSAType.FSA_TYPE_361480,
            ActuatorFSAType.FSA_TYPE_3611100,
            ActuatorFSAType.FSA_TYPE_3611100,
            ActuatorFSAType.FSA_TYPE_3611100,
            ActuatorFSAType.FSA_TYPE_250830,
            ActuatorFSAType.FSA_TYPE_250830,
            # right arm
            ActuatorFSAType.FSA_TYPE_361480,
            ActuatorFSAType.FSA_TYPE_361480,
            ActuatorFSAType.FSA_TYPE_3611100,
            ActuatorFSAType.FSA_TYPE_3611100,
            ActuatorFSAType.FSA_TYPE_3611100,
            ActuatorFSAType.FSA_TYPE_250830,
            ActuatorFSAType.FSA_TYPE_250830,
        ]

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
        RobotGR1._init_joint(self)

        # default pid
        # index_list_joint_change = numpy.array([
        #     0, 1, 2, 3, 4, 5,  # left leg
        #     6, 7, 8, 9, 10, 11,  # right leg
        #     12, 13, 14,  # waist
        #     18, 19, 20, 21,  # left arm
        #     25, 26, 27, 28,  # right arm
        # ])
        # pd_control_kp = numpy.array([
        #     40, 45, 130, 130, 18, 18,  # left leg
        #     40, 45, 130, 130, 18, 18,  # right leg
        #     45, 45, 45,  # waist
        #     30, 30, 30, 30,  # left arm
        #     30, 30, 30, 30,  # right arm
        # ])
        # if self.joint_use_dic:  # DIC: dynamic inertia compensation
        #     position_control_kp = numpy.array([
        #         0.2333, 0.0406, 0.2333, 0.2333, 0.1111, 0.1111,  # left leg
        #         0.2333, 0.0406, 0.2333, 0.2333, 0.1111, 0.1111,  # right leg
        #         0.0406, 0.0406, 0.0406,  # waist
        #         0.0370, 0.0370, 0.0370, 0.0370,  # left arm
        #         0.0370, 0.0370, 0.0370, 0.0370,  # right arm
        #     ])
        #     velocity_control_kp = numpy.array([
        #         0.0302, 0.1003, 0.7782, 0.7782, 0.0317, 0.0317,  # left leg
        #         0.0302, 0.1003, 0.7782, 0.7782, 0.0317, 0.0317,  # right leg
        #         0.1003, 0.1003, 0.1003,  # waist
        #         0.0329, 0.0329, 0.0283, 0.0283,  # left arm
        #         0.0329, 0.0329, 0.0283, 0.0283,  # right arm
        #     ])
        #     pd_control_kd = numpy.array([
        #         # left leg
        #         pd_control_kp[0] / 10 * 2.5, pd_control_kp[1] / 10 * 7.5, pd_control_kp[2] / 10 * 2.5,
        #         pd_control_kp[3] / 10 * 2.5, pd_control_kp[4] / 10 * 2.5, pd_control_kp[5] / 10 * 2.5,
        #         # right leg
        #         pd_control_kp[6] / 10 * 2.5, pd_control_kp[7] / 10 * 7.5, pd_control_kp[8] / 10 * 2.5,
        #         pd_control_kp[9] / 10 * 2.5, pd_control_kp[10] / 10 * 2.5, pd_control_kp[11] / 10 * 2.5,
        #         # waist
        #         pd_control_kp[12] / 10 * 7.5, pd_control_kp[13] / 10 * 7.5, pd_control_kp[14] / 10 * 7.5,
        #         # left arm
        #         pd_control_kp[15] / 10 * 7.5, pd_control_kp[16] / 10 * 7.5,
        #         pd_control_kp[17] / 10 * 7.5, pd_control_kp[18] / 10 * 7.5,
        #         # right arm
        #         pd_control_kp[19] / 10 * 7.5, pd_control_kp[20] / 10 * 7.5,
        #         pd_control_kp[21] / 10 * 7.5, pd_control_kp[22] / 10 * 7.5,
        #     ])
        # else:
        #     position_control_kp = numpy.array([
        #         0.5833, 0.2845, 0.5833, 0.5833, 0.2778, 0.2778,  # left leg
        #         0.5833, 0.2845, 0.5833, 0.5833, 0.2778, 0.2778,  # right leg
        #         0.2845, 0.2845, 0.2845,  # waist
        #         0.2778, 0.2778, 0.2778, 0.2778,  # left arm
        #         0.2778, 0.2778, 0.2778, 0.2778,  # right arm
        #     ])
        #     velocity_control_kp = numpy.array([
        #         0.0120, 0.0134, 0.3113, 0.3113, 0.0127, 0.0127,  # left leg
        #         0.0120, 0.0134, 0.3113, 0.3113, 0.0127, 0.0127,  # right leg
        #         0.0134, 0.0134, 0.0134,  # waist
        #         0.0044, 0.0044, 0.0038, 0.0038,  # left arm
        #         0.0044, 0.0044, 0.0038, 0.0038,  # right arm
        #     ])
        #     pd_control_kd = numpy.array([
        #         # left leg
        #         pd_control_kp[0] / 10 * 1.0, pd_control_kp[1] / 10 * 1.0, pd_control_kp[2] / 10 * 1.0,
        #         pd_control_kp[3] / 10 * 1.0, pd_control_kp[4] / 10 * 1.0, pd_control_kp[5] / 10 * 1.0,
        #         # right leg
        #         pd_control_kp[6] / 10 * 1.0, pd_control_kp[7] / 10 * 1.0, pd_control_kp[8] / 10 * 1.0,
        #         pd_control_kp[9] / 10 * 1.0, pd_control_kp[10] / 10 * 1.0, pd_control_kp[11] / 10 * 1.0,
        #         # waist
        #         pd_control_kp[12] / 10 * 1.0, pd_control_kp[13] / 10 * 1.0, pd_control_kp[14] / 10 * 1.0,
        #         # left arm
        #         pd_control_kp[15] / 10 * 1.0, pd_control_kp[16] / 10 * 1.0,
        #         pd_control_kp[17] / 10 * 1.0, pd_control_kp[18] / 10 * 1.0,
        #         # right arm
        #         pd_control_kp[19] / 10 * 1.0, pd_control_kp[20] / 10 * 1.0,
        #         pd_control_kp[21] / 10 * 1.0, pd_control_kp[22] / 10 * 1.0,
        #     ])
        #
        # for i in range(len(index_list_joint_change)):
        #     index = index_list_joint_change[i]
        #     self.joint_position_control_kp[index] = position_control_kp[i]
        #     self.joint_velocity_control_kp[index] = velocity_control_kp[i]
        #     self.joint_pd_control_kp[index] = pd_control_kp[i]
        #     self.joint_pd_control_kd[index] = pd_control_kd[i]
        #
        # for i in range(len(index_list_joint_change)):
        #     # use position control as default when power on
        #     index = index_list_joint_change[i]
        #     self.joints[index].set_target_position_control_kp(self.joint_position_control_kp[index])
        #     self.joints[index].set_target_velocity_control_kp(self.joint_velocity_control_kp[index])
        #     self.joints[index].set_target_velocity_control_ki(0)

        # joint -> joint urdf
        self.parallel_ankle_left = ParallelAnkle("left")
        self.parallel_ankle_right = ParallelAnkle("right")
        self.parallel_wrist_left = ParallelWrist("left")
        self.parallel_wrist_right = ParallelWrist("right")

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
                12, 13 ,14,
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

    def _init_algorithm(self) -> FunctionResult:
        super()._init_algorithm()

        self.algorithm_test_parallel_ankle_control_model = RobotGR1AlgorithmBasicControlModel()
        self.algorithm_nohla_stand_control_model = RobotGR1NohlaAlgorithmStandControlModel(
            dt=self.control_period,
        )
        self.algorithm_nohla_rl_walk_control_model = RobotGR1NohlaAlgorithmRLWalkControlModel(
            dt=self.control_period,
            decimation=(1 / 100) / self.control_period,
        )
        self.algorithm_simple_rl_airtime_control_model = RobotGR1SimpleAlgorithmRLAirtimeControlModel(
            dt=self.control_period,
            decimation=(1 / 50) / self.control_period,
        )
        self.algorithm_simple_rl_airtime_stack_control_model = RobotGR1SimpleAlgorithmRLAirtimeStackControlModel(
            dt=self.control_period,
            decimation=(1 / 50) / self.control_period,
        )

        return FunctionResult.SUCCESS

    def _init_task(self) -> FunctionResult:
        super()._init_task()

        self.tasks.extend(
            [
                RobotGR1Task.TASK_TEST_PARALLEL_ANKLE,
                RobotGR1Task.TASK_NOHLA_STAND,
                RobotGR1Task.TASK_NOHLA_RL_WALK,
                RobotGR1Task.TASK_SIMPLE_RL_AIRTIME,
                RobotGR1Task.TASK_SIMPLE_RL_AIRTIME_STACK,
            ]
        )

        self.task_algorithm_models.update(
            {
                RobotGR1Task.TASK_TEST_PARALLEL_ANKLE: self.algorithm_test_parallel_ankle_control_model,
                RobotGR1Task.TASK_NOHLA_STAND: self.algorithm_nohla_stand_control_model,
                RobotGR1Task.TASK_NOHLA_RL_WALK: self.algorithm_nohla_rl_walk_control_model,
                RobotGR1Task.TASK_SIMPLE_RL_AIRTIME: self.algorithm_simple_rl_airtime_control_model,
                RobotGR1Task.TASK_SIMPLE_RL_AIRTIME_STACK: self.algorithm_simple_rl_airtime_stack_control_model,
            }
        )

        self.task_functions.update(
            {
                RobotGR1Task.TASK_TEST_PARALLEL_ANKLE: self.task_test_parallel_ankle_control,
                RobotGR1Task.TASK_NOHLA_STAND: self.task_nohla_stand_control,
                RobotGR1Task.TASK_NOHLA_RL_WALK: self.task_nohla_rl_walk_control,
                RobotGR1Task.TASK_SIMPLE_RL_AIRTIME: self.task_simple_rl_airtime_control,
                RobotGR1Task.TASK_SIMPLE_RL_AIRTIME_STACK: self.task_simple_rl_airtime_stack_control,
            }
        )

        return FunctionResult.SUCCESS

    # =====================================================================================================

    def _init_encoders(self):
        # read stored abs encoder angle
        Logger().print_trace("RobotGR1 prepare() read stored abs encoder calibrate value")
        map_fi_fses_values_stored = None
        sensor_abs_encoder_data_paths = []
        sensor_abs_encoder_data_paths.append(gl_config.config_dir + "/sensor_offset.json")
        sensor_abs_encoder_data_paths.append(
            gl_config.parameters["sensor_abs_encoder"].get("data_path", "./sensor_offset.json")
        )

        # load default sensor offset from ~/RoCS/bin/pythonscripts/absAngle.json
        default_sensor_offset = load_sensor_offset_dict()
        if default_sensor_offset is not None:
            Logger().print_trace(
                "default_sensor_offset loaded from ~/RoCS/bin/pythonscripts/absAngle.json = \n",
                str(default_sensor_offset),
            )
            map_fi_fses_values_stored = default_sensor_offset

        # if sensor_abs_encoder_data_paths is not None, try to load from file. If not, use default_sensor_offset
        for sensor_abs_encoder_data_path in sensor_abs_encoder_data_paths:
            if os.path.exists(sensor_abs_encoder_data_path):
                Logger().print_trace("home_angle file exists")

                with open(sensor_abs_encoder_data_path) as file:
                    json_fi_fses_angle_value = file.read()
                    map_fi_fses_values_stored = json.loads(json_fi_fses_angle_value)

                Logger().print_trace_highlight("home_angle = \n", str(json_fi_fses_angle_value))

                # set flag_calibration
                self.flag_calibration = FlagState.SET
                break

        if map_fi_fses_values_stored is None:
            Logger().print_trace_error(
                sensor_abs_encoder_data_paths,
                " file not exists, please do TASK_SET_HOME first",
            )

            # clear flag_calibration
            self.flag_calibration = FlagState.CLEAR
        else:
            self.flag_calibration = FlagState.SET

        # get raw angle
        Logger().print_trace("RobotGR1 prepare() upload fi_fse raw value")

        retry_count = 0
        retry_max = 5

        for i in range(self.number_of_sensor_fi_fse):
            retry_count = 0
            result = FunctionResult.FAIL

            while result == FunctionResult.FAIL:
                if self.sensor_fi_fse[i] is not None:
                    result = self.sensor_fi_fse[i].upload()
                else:
                    break

                retry_count += 1
                if retry_count >= retry_max:
                    Logger().print_trace_error("Upload fi_fse fail!")
                    exit(FunctionResult.FAIL)

        abs_encoder_raw_value = {}
        for i in range(self.number_of_sensor_fi_fse):
            if self.sensor_fi_fse[i] is not None:
                abs_encoder_raw_value.update(
                    {self.sensor_fi_fse[i].id: numpy.round(self.sensor_fi_fse[i].measured_angle_raw, 6)}
                )

        try:
            Logger().print_trace(
                "abs_encoder_raw_value = \n", str(json.dumps(abs_encoder_raw_value, indent=4, ensure_ascii=False))
            )
        except:
            Logger().print_trace_warning("abs_encoder_raw_value = \n", str({}))

        # load file config
        Logger().print_trace("RobotGR1 prepare() setup fi_fse offset")

        if map_fi_fses_values_stored is not None:
            for i in range(self.number_of_sensor_fi_fse):
                if self.sensor_fi_fse[i] is not None:
                    id = self.sensor_fi_fse[i].id
                    sensor_offset = map_fi_fses_values_stored[id]

                    self.sensor_fi_fse[i].sensor_offset = sensor_offset
                else:
                    pass

        # sensor
        Logger().print_trace("RobotGR1 prepare() upload fi_fse calibrate value")

        retry_count = 0
        retry_max = 5

        for i in range(self.number_of_sensor_fi_fse):
            retry_count = 0
            result = FunctionResult.FAIL

            while result == FunctionResult.FAIL:
                if self.sensor_fi_fse[i] is not None:
                    result = self.sensor_fi_fse[i].upload()
                else:
                    break

                retry_count += 1
                if retry_count >= retry_max:
                    Logger().print_trace_error("Upload fi_fse fail!")
                    exit(FunctionResult.FAIL)

        return FunctionResult.SUCCESS

    def prepare(self) -> FunctionResult:
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

            # parallel ankle
            joint_urdf_angle_offset = numpy.zeros(shape=self.number_of_joint)
            joint_urdf_angle_offset[0 : self.number_of_sensor_fi_fse] = abs_encoder_angle_offset[
                0 : self.number_of_sensor_fi_fse
            ].copy()

            print("joint_urdf_angle_offset = \n", numpy.round(joint_urdf_angle_offset, 3))

            (
                joint_urdf_angle_offset[4],
                joint_urdf_angle_offset[5],
                joint_urdf_angle_offset[10],
                joint_urdf_angle_offset[11],
            ) = self._calculate_parallel_ankle_inverse_kinematic(
                joint_urdf_angle_offset[4],
                joint_urdf_angle_offset[5],
                joint_urdf_angle_offset[10],
                joint_urdf_angle_offset[11],
            )

            joint_angle_offset = joint_urdf_angle_offset

            # joint_angle_offset[6+6+0] = 0
            print("joint_angle_offset = \n", numpy.round(joint_angle_offset, 1))

            # read current joint position
            # Jason 2024-01-26:
            # need to wait and send twice to allow data to upload
            self.actuator_group.upload()
            time.sleep(0.1)
            self.joint_group.update()
            time.sleep(0.1)
            self.actuator_group.upload()
            time.sleep(0.1)
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
                sensor_usb_imu_group_measured_quat[0],
                -sensor_usb_imu_group_measured_quat[1],
            ]
        )

        out_sensor_usb_imu_group_measured_angle = numpy.array(
            [
                180 - sensor_usb_imu_group_measured_angle[0]
                if sensor_usb_imu_group_measured_angle[0] > 0
                else -180 - sensor_usb_imu_group_measured_angle[0],
                sensor_usb_imu_group_measured_angle[1],
                sensor_usb_imu_group_measured_angle[2],
            ]
        )  # unit : deg

        out_sensor_usb_imu_group_measured_angular_velocity = numpy.array(
            [
                -sensor_usb_imu_group_measured_angular_velocity[1],
                -sensor_usb_imu_group_measured_angular_velocity[0],
                -sensor_usb_imu_group_measured_angular_velocity[2],
            ]
        )  # unit : deg/s
        out_sensor_usb_imu_group_measured_linear_acceleration = (
            numpy.array(
                [
                    -sensor_usb_imu_group_measured_linear_acceleration[1],
                    -sensor_usb_imu_group_measured_linear_acceleration[0],
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
            # parallel ankle
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
        super().control_loop_get_state_developer_mode()

        return self.state_dict

    def control_loop_set_control(self, control_dict=None) -> FunctionResult:
        if (
            self.deploy_mode == DeployMode.DEFAULT
            or self.deploy_mode == DeployMode.DEVELOPER_MODE
            or self.deploy_mode == DeployMode.SDK_MODE
        ):
            self.control_loop_set_control_developer_mode(control_dict)

        else:
            Logger().print_trace_warning("Unknown deploy mode: " + str(self.deploy_mode))

        return FunctionResult.SUCCESS

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

            # --------------------------

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

        for i, joint in enumerate(self.joints):
            joint.set_target_position(joint_control_position[i])

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

    def _calculate_parallel_ankle_inverse_kinematic(
        self,
        left_leg_ankle_position_pitch_deg,
        left_leg_ankle_position_roll_deg,
        right_leg_ankle_position_pitch_deg,
        right_leg_ankle_position_roll_deg,
    ):
        """
        Calculate parallel ankle inverse kinematic position

        Input:
        - left_leg_ankle_position_pitch_deg
        - left_leg_ankle_position_roll_deg
        - right_leg_ankle_position_pitch_deg
        - right_leg_ankle_position_roll_deg
        """

        # parallel ankle
        try:
            (
                left_leg_ankle_position_joint_upper_deg,
                left_leg_ankle_position_joint_lower_deg,
                _,
                _,
                _,
                _,
            ) = self.parallel_ankle_left.inverse(
                ankle_position_pitch_deg=left_leg_ankle_position_pitch_deg,
                ankle_position_roll_deg=left_leg_ankle_position_roll_deg,
            )

        except Exception as e:
            Logger().print_trace_warning(f"control_loop_set_control() self.parallel_ankle_left.inverse error: {e}")

            left_leg_ankle_position_joint_upper_deg = self.joint_group_measured_position[4]
            left_leg_ankle_position_joint_lower_deg = self.joint_group_measured_position[5]

            # calculate error, switch back to servo_off
            Logger().print_trace("calculate error, switch back to TASK_SERVO_OFF")
            self.task_command = RobotBaseTask.TASK_SERVO_OFF
            self.flag_task_command_update = FlagState.SET

        try:
            (
                right_leg_ankle_position_joint_upper_deg,
                right_leg_ankle_position_joint_lower_deg,
                _,
                _,
                _,
                _,
            ) = self.parallel_ankle_right.inverse(
                ankle_position_pitch_deg=right_leg_ankle_position_pitch_deg,
                ankle_position_roll_deg=right_leg_ankle_position_roll_deg,
            )

        except Exception as e:
            Logger().print_trace_warning(f"control_loop_set_control() self.parallel_ankle_right.inverse error {e}")

            right_leg_ankle_position_joint_upper_deg = self.joint_group_measured_position[10]
            right_leg_ankle_position_joint_lower_deg = self.joint_group_measured_position[11]

            # calculate error, switch back to servo_off
            Logger().print_trace("calculate error, switch back to TASK_SERVO_OFF")
            self.task_command = RobotBaseTask.TASK_SERVO_OFF
            self.flag_task_command_update = FlagState.SET

        return (
            left_leg_ankle_position_joint_upper_deg,
            left_leg_ankle_position_joint_lower_deg,
            right_leg_ankle_position_joint_upper_deg,
            right_leg_ankle_position_joint_lower_deg,
        )

    def _calculate_parallel_wrist_inverse_kinematic(
        self,
        left_leg_wrist_position_pitch_deg,
        left_leg_wrist_position_roll_deg,
        right_leg_wrist_position_pitch_deg,
        right_leg_wrist_position_roll_deg,
    ):
        """
        Calculate parallel wrist inverse kinematic position

        Input:
        - left_leg_wrist_position_pitch_deg
        - left_leg_wrist_position_roll_deg
        - right_leg_wrist_position_pitch_deg
        - right_leg_wrist_position_roll_deg
        """

        # parallel wrist
        try:
            (
                left_leg_wrist_position_joint_upper_deg,
                left_leg_wrist_position_joint_lower_deg,
                _,
                _,
                _,
                _,
            ) = self.parallel_wrist_left.inverse(
                wrist_position_pitch_deg=left_leg_wrist_position_pitch_deg,
                wrist_position_roll_deg=left_leg_wrist_position_roll_deg,
            )

        except Exception as e:
            Logger().print_trace_warning(f"control_loop_set_control() self.parallel_wrist_left.inverse error: {e}")
            # print(right_leg_wrist_position_pitch_deg, right_leg_wrist_position_roll_deg)

            left_leg_wrist_position_joint_upper_deg = self.joint_group_measured_position[23]
            left_leg_wrist_position_joint_lower_deg = self.joint_group_measured_position[24]

            # calculate error, switch back to servo_off
            Logger().print_trace("calculate error, switch back to TASK_SERVO_OFF")
            self.task_command = RobotBaseTask.TASK_SERVO_OFF
            self.flag_task_command_update = FlagState.SET

        try:
            (
                right_leg_wrist_position_joint_upper_deg,
                right_leg_wrist_position_joint_lower_deg,
                _,
                _,
                _,
                _,
            ) = self.parallel_wrist_right.inverse(
                wrist_position_pitch_deg=right_leg_wrist_position_pitch_deg,
                wrist_position_roll_deg=right_leg_wrist_position_roll_deg,
            )

        except Exception as e:
            Logger().print_trace_warning(f"control_loop_set_control() self.parallel_wrist_right.inverse error: {e}")
            # print(right_leg_wrist_position_pitch_deg, right_leg_wrist_position_roll_deg)

            right_leg_wrist_position_joint_upper_deg = self.joint_group_measured_position[30]
            right_leg_wrist_position_joint_lower_deg = self.joint_group_measured_position[31]

            # calculate error, switch back to servo_off
            Logger().print_trace("calculate error, switch back to TASK_SERVO_OFF")
            self.task_command = RobotBaseTask.TASK_SERVO_OFF
            self.flag_task_command_update = FlagState.SET

        return (
            left_leg_wrist_position_joint_upper_deg,
            left_leg_wrist_position_joint_lower_deg,
            right_leg_wrist_position_joint_upper_deg,
            right_leg_wrist_position_joint_lower_deg,
        )

    def task_test_parallel_ankle_control(self):
        # joint -> urdf
        joint_measured_position_urdf = self.joint_group_measured_position.copy()
        joint_measured_velocity_urdf = self.joint_group_measured_velocity.copy()
        joint_measured_kinetic_urdf = self.joint_group_measured_kinetic.copy()

        # parallel ankle
        (
            joint_measured_position_urdf[4],
            joint_measured_position_urdf[5],
            joint_measured_velocity_urdf[4],
            joint_measured_velocity_urdf[5],
            joint_measured_kinetic_urdf[4],
            joint_measured_kinetic_urdf[5],
        ) = self.parallel_ankle_left.forward(
            joint_position_up_deg=self.joint_group_measured_position[4],
            joint_position_lower_deg=self.joint_group_measured_position[5],
            joint_velocity_up_deg=self.joint_group_measured_velocity[4],
            joint_velocity_lower_deg=self.joint_group_measured_velocity[5],
            joint_torque_up=self.joint_group_measured_kinetic[4],
            joint_torque_lower=self.joint_group_measured_kinetic[5],
        )

        (
            joint_measured_position_urdf[10],
            joint_measured_position_urdf[11],
            joint_measured_velocity_urdf[10],
            joint_measured_velocity_urdf[11],
            joint_measured_kinetic_urdf[10],
            joint_measured_kinetic_urdf[11],
        ) = self.parallel_ankle_right.forward(
            joint_position_up_deg=self.joint_group_measured_position[10],
            joint_position_lower_deg=self.joint_group_measured_position[11],
            joint_velocity_up_deg=self.joint_group_measured_velocity[10],
            joint_velocity_lower_deg=self.joint_group_measured_velocity[11],
            joint_torque_up=self.joint_group_measured_kinetic[10],
            joint_torque_lower=self.joint_group_measured_kinetic[11],
        )

        print(
            "ankle position = \n",
            numpy.round(joint_measured_position_urdf[4], 1),
            numpy.round(joint_measured_position_urdf[5], 1),
            numpy.round(joint_measured_position_urdf[10], 1),
            numpy.round(joint_measured_position_urdf[11], 1),
        )

        return FunctionResult.SUCCESS

    # ==================================================================================================

    def task_stand_control(self):
        # pid
        for i in range(self.number_of_joint):
            self.joints[i].set_target_position_control_kp(self.joint_position_control_kp[i])
            self.joints[i].set_target_velocity_control_kp(self.joint_velocity_control_kp[i])

        super().task_stand_control()

        joint_target_position_urdf = numpy.zeros(self.number_of_joint)

        for i in range(self.number_of_joint):
            joint_target_position_urdf[i] = self.joints[i].target_position

        # joint: real robot urdf -> joint
        joint_target_position = joint_target_position_urdf.copy()

        (
            joint_target_position[4],
            joint_target_position[5],
            joint_target_position[10],
            joint_target_position[11],
        ) = self._calculate_parallel_ankle_inverse_kinematic(
            joint_target_position_urdf[4],
            joint_target_position_urdf[5],
            joint_target_position_urdf[10],
            joint_target_position_urdf[11],
        )

        (
            joint_target_position[23],
            joint_target_position[24],
            joint_target_position[30],
            joint_target_position[31],
        ) = self._calculate_parallel_wrist_inverse_kinematic(
            joint_target_position_urdf[23],
            joint_target_position_urdf[24],
            joint_target_position_urdf[30],
            joint_target_position_urdf[31],
        )

        # output
        if self.work_space == RobotWorkSpace.JOINT_SPACE:
            for i in range(self.number_of_joint):
                self.joints[i].set_target_control_mode(JointControlMode.POSITION)
                self.joints[i].set_target_position(joint_target_position[i])

        return FunctionResult.SUCCESS

    def task_stand_pd_control(self):
        # pid
        for i in range(self.number_of_joint):
            self.joints[i].set_target_pd_control_kp(self.joint_pd_control_kp[i])
            self.joints[i].set_target_pd_control_kd(self.joint_pd_control_kd[i])

        super().task_stand_control()

        joint_target_position_urdf = numpy.zeros(self.number_of_joint)

        for i in range(self.number_of_joint):
            joint_target_position_urdf[i] = self.joints[i].target_position

        # joint: real robot urdf -> joint
        joint_target_position = joint_target_position_urdf.copy()

        (
            joint_target_position[4],
            joint_target_position[5],
            joint_target_position[10],
            joint_target_position[11],
        ) = self._calculate_parallel_ankle_inverse_kinematic(
            joint_target_position_urdf[4],
            joint_target_position_urdf[5],
            joint_target_position_urdf[10],
            joint_target_position_urdf[11],
        )

        (
            joint_target_position[23],
            joint_target_position[24],
            joint_target_position[30],
            joint_target_position[31],
        ) = self._calculate_parallel_wrist_inverse_kinematic(
            joint_target_position_urdf[23],
            joint_target_position_urdf[24],
            joint_target_position_urdf[30],
            joint_target_position_urdf[31],
        )

        # output
        if self.work_space == RobotWorkSpace.JOINT_SPACE:
            for i in range(self.number_of_joint):
                self.joints[i].set_target_control_mode(JointControlMode.PD)
                self.joints[i].set_target_position(joint_target_position[i])

        return FunctionResult.SUCCESS

    # ==================================================================================================

    def task_nohla_stand_control(self):
        # joint -> urdf
        joint_measured_position_urdf = numpy.deg2rad(self.joint_urdf_group_measured_position.copy())  # unit : rad
        joint_measured_velocity_urdf = numpy.deg2rad(self.joint_urdf_group_measured_velocity.copy())  # unit : rad/s

        joint_measured_position_nohla_urdf = numpy.zeros(
            self.algorithm_nohla_stand_control_model.num_of_joints
        )  # unit : rad
        joint_measured_velocity_nohla_urdf = numpy.zeros(
            self.algorithm_nohla_stand_control_model.num_of_joints
        )  # unit : rad/s

        # joint: real robot urdf -> algorithm urdf
        for i in range(self.algorithm_nohla_stand_control_model.num_of_joints):
            index = self.algorithm_nohla_stand_control_model.index_of_joints_real_robot[i]
            joint_measured_position_nohla_urdf[i] = joint_measured_position_urdf[index]
            joint_measured_velocity_nohla_urdf[i] = joint_measured_velocity_urdf[index]

        # algorithm
        work_space_nohla, control_mode_nohla, joint_target_position_nohla_urdf = (
            self.algorithm_nohla_stand_control_model.run(
                joint_measured_position_urdf=joint_measured_position_nohla_urdf,
                joint_measured_velocity_urdf=joint_measured_velocity_nohla_urdf,
            )
        )

        joint_target_position_nohla_urdf = joint_target_position_nohla_urdf / numpy.pi * 180.0  # unit : deg

        # joint: algorithm urdf -> real robot urdf
        work_space = work_space_nohla

        control_mode = numpy.zeros(self.number_of_joint)
        joint_target_position_urdf = numpy.zeros(self.number_of_joint)  # unit : deg

        for i in range(self.algorithm_nohla_stand_control_model.num_of_joints):
            index = self.algorithm_nohla_stand_control_model.index_of_joints_real_robot[i]
            control_mode[index] = control_mode_nohla[i]
            joint_target_position_urdf[index] = joint_target_position_nohla_urdf[i]

        # joint: real robot urdf -> joint
        joint_target_position = joint_target_position_urdf.copy()

        (
            joint_target_position[4],
            joint_target_position[5],
            joint_target_position[10],
            joint_target_position[11],
        ) = self._calculate_parallel_ankle_inverse_kinematic(
            joint_target_position_urdf[4],
            joint_target_position_urdf[5],
            joint_target_position_urdf[10],
            joint_target_position_urdf[11],
        )

        # print(numpy.round(numpy.rad2deg(joint_measured_position_nohla_urdf)),
        #       numpy.round(joint_target_position_nohla_urdf))

        # output
        if work_space == RobotWorkSpace.ACTUATOR_SPACE:
            self.work_space = work_space
            for i in range(self.number_of_actuator):
                self.actuators[i].set_target_control_mode(control_mode[i])

        elif work_space == RobotWorkSpace.JOINT_SPACE:
            self.work_space = work_space
            for i in range(self.number_of_joint):
                self.joints[i].set_target_control_mode(control_mode[i])
                self.joints[i].set_target_position(joint_target_position[i])

        else:
            Logger().print_trace_error("task_nohla_stand_control() unknown work_space")

        return FunctionResult.SUCCESS

    def task_nohla_rl_walk_control(self):
        # fmt: off
        body_speed_lin_max = 0.50
        body_speed_ang_max = 0.35
        commands = \
            numpy.array(
                [body_speed_lin_max * -operator_joystick.axis_left()[1],
                 body_speed_lin_max * -operator_joystick.axis_left()[0],
                 body_speed_ang_max * -operator_joystick.axis_right()[0], ]
            )
        commands = numpy.array([0.0, 0.0, 0.0, ])
        base_measured_quat_to_world = \
            self.sensor_usb_imu_group_measured_quat.copy()
        base_measured_rpy_vel_to_self = \
            numpy.deg2rad(self.sensor_usb_imu_group_measured_angular_velocity.copy())

        # joint -> urdf
        joint_measured_position_urdf = \
            numpy.deg2rad(self.joint_urdf_group_measured_position.copy())
        joint_measured_velocity_urdf = \
            numpy.deg2rad(self.joint_urdf_group_measured_velocity.copy())

        joint_measured_position_nohla_urdf = \
            numpy.zeros(self.algorithm_nohla_rl_walk_control_model.num_of_joints)
        joint_measured_velocity_nohla_urdf = \
            numpy.zeros(self.algorithm_nohla_rl_walk_control_model.num_of_joints)

        # joint: real robot urdf -> algorithm urdf
        for i in range(self.algorithm_nohla_rl_walk_control_model.num_of_joints):
            index = self.algorithm_nohla_rl_walk_control_model.index_of_joints_real_robot[i]
            joint_measured_position_nohla_urdf[i] = joint_measured_position_urdf[index]
            joint_measured_velocity_nohla_urdf[i] = joint_measured_velocity_urdf[index]

        # TODO 2024-07-09: use default target position -> urdf joint target position
        init_output = self.algorithm_nohla_rl_walk_control_model.joint_default_position

        # TODO 2024-02-26: Use the joystick button R2 to switch between walking and standing
        self.algorithm_nohla_rl_walk_control_model.gait_phase_ratio = (
            self.algorithm_nohla_rl_walk_control_model.gait_phase_ratio_walk
        )
        # fmt: on

        joint_target_position_nohla_urdf = self.algorithm_nohla_rl_walk_control_model.run(
            init_output=init_output,
            commands=commands,
            base_measured_quat_to_world=base_measured_quat_to_world,
            base_measured_rpy_vel_to_self=base_measured_rpy_vel_to_self,
            joint_measured_position_urdf=joint_measured_position_nohla_urdf,
            joint_measured_velocity_urdf=joint_measured_velocity_nohla_urdf,
        )

        # time cost: 0.1ms
        # log_data_list = []
        # log_data_list.extend(["#init_output"])
        # log_data_list.extend(init_output)
        # log_data_list.extend(["#commands"])
        # log_data_list.extend(commands)
        # log_data_list.extend(["#base_quat"])
        # log_data_list.extend(base_measured_quat_to_world)
        # log_data_list.extend(["#base_ang_vel"])
        # log_data_list.extend(numpy.rad2deg(base_measured_rpy_vel_to_self))
        # log_data_list.extend(["#dof_pos"])
        # log_data_list.extend(numpy.rad2deg(joint_measured_position_nohla_urdf))
        # log_data_list.extend(["#dof_vel"])
        # log_data_list.extend(numpy.rad2deg(joint_measured_velocity_nohla_urdf))
        # log_data_list.extend(["#actions"])
        # log_data_list.extend(numpy.rad2deg(joint_target_position_nohla_urdf))
        # Logger().print_log_file_data(log_data_list)

        joint_target_position_nohla_urdf = numpy.rad2deg(joint_target_position_nohla_urdf)  # unit : deg

        # joint: algorithm urdf -> real robot urdf
        work_space = RobotWorkSpace.JOINT_SPACE
        control_mode = numpy.ones(self.number_of_joint) * JointControlMode.NONE
        joint_target_position_urdf = numpy.zeros(self.number_of_joint)  # unit : deg

        for i in range(self.algorithm_nohla_rl_walk_control_model.num_of_joints):
            index = self.algorithm_nohla_rl_walk_control_model.index_of_joints_real_robot[i]
            control_mode[index] = JointControlMode.POSITION
            joint_target_position_urdf[index] = joint_target_position_nohla_urdf[i]

        # joint: real robot urdf -> joint
        joint_target_position = joint_target_position_urdf.copy()

        (
            joint_target_position[4],
            joint_target_position[5],
            joint_target_position[10],
            joint_target_position[11],
        ) = self._calculate_parallel_ankle_inverse_kinematic(
            joint_target_position_urdf[4],
            joint_target_position_urdf[5],
            joint_target_position_urdf[10],
            joint_target_position_urdf[11],
        )

        # output
        self.work_space = work_space
        for i in range(self.number_of_joint):
            self.joints[i].set_target_control_mode(control_mode[i])
            self.joints[i].set_target_position(joint_target_position[i])

        return FunctionResult.SUCCESS

    # ==================================================================================================

    def task_simple_rl_airtime_control(self):
        # fmt: off
        body_speed_lin_max = 0.50
        body_speed_ang_max = 0.35
        commands = \
            numpy.array(
                [body_speed_lin_max * -operator_joystick.axis_left()[1],
                 body_speed_lin_max * -operator_joystick.axis_left()[0],
                 body_speed_ang_max * -operator_joystick.axis_right()[0], ]
            )
        commands = numpy.array([0.0, 0.0, 0.0, ])

        base_measured_quat_to_world = \
            self.sensor_usb_imu_group_measured_quat.copy()
        base_measured_rpy_vel_to_self = \
            numpy.deg2rad(self.sensor_usb_imu_group_measured_angular_velocity.copy())

        # joint -> urdf
        joint_measured_position_urdf = \
            numpy.deg2rad(self.joint_urdf_group_measured_position.copy())
        joint_measured_velocity_urdf = \
            numpy.deg2rad(self.joint_urdf_group_measured_velocity.copy())

        joint_measured_position_simple_urdf = \
            numpy.zeros(self.algorithm_simple_rl_airtime_control_model.num_of_joints)
        joint_measured_velocity_simple_urdf = \
            numpy.zeros(self.algorithm_simple_rl_airtime_control_model.num_of_joints)

        # joint: real robot urdf -> algorithm urdf
        for i in range(self.algorithm_simple_rl_airtime_control_model.num_of_joints):
            index = self.algorithm_simple_rl_airtime_control_model.index_of_joints_real_robot[i]
            joint_measured_position_simple_urdf[i] = joint_measured_position_urdf[index]
            joint_measured_position_simple_urdf[i] = joint_measured_velocity_urdf[index]

        # TODO 2024-07-09: use default target position -> urdf joint target position
        init_output = self.algorithm_simple_rl_airtime_control_model.joint_default_position

        joint_pd_control_target_simple_urdf = (
            self.algorithm_simple_rl_airtime_control_model.run(
                init_output=init_output,
                commands=commands,
                base_measured_quat_to_world=base_measured_quat_to_world,
                base_measured_rpy_vel_to_self=base_measured_rpy_vel_to_self,
                joint_measured_position_urdf=joint_measured_position_urdf,
                joint_measured_velocity_urdf=joint_measured_velocity_urdf,
            )
        )

        joint_pd_control_target_simple_urdf = \
            numpy.rad2deg(joint_pd_control_target_simple_urdf)  # unit : deg

        # joint: algorithm urdf -> real robot urdf
        work_space = RobotWorkSpace.JOINT_SPACE
        control_mode = numpy.ones(self.number_of_joint) * JointControlMode.NONE
        joint_target_position_urdf = numpy.array([
            0.0, 0.0, -0.2618, 0.5236, -0.2618, 0.0,  # left leg (6)
            0.0, 0.0, -0.2618, 0.5236, -0.2618, 0.0,  # right leg (6)
            0.0, 0.0, 0.0,  # waist (3)
            0.0, 0.0, 0.0,  # head (3)
            0.0, 0.2, 0.0, -0.3, 0.0, 0.0, 0.0,  # left arm (7)
            0.0, -0.2, 0.0, -0.3, 0.0, 0.0, 0.0,  # right arm (7)
        ]) / numpy.pi * 180  # unit : deg

        for i in range(self.algorithm_simple_rl_airtime_control_model.num_of_joints):
            index = self.algorithm_simple_rl_airtime_control_model.index_of_joints_real_robot[i]
            control_mode[index] = JointControlMode.POSITION
            joint_target_position_urdf[index] = joint_pd_control_target_simple_urdf[i]

        # joint: real robot urdf -> joint
        joint_target_position = joint_target_position_urdf.copy()

        (
            joint_target_position[4],
            joint_target_position[5],
            joint_target_position[10],
            joint_target_position[11],
        ) = self._calculate_parallel_ankle_inverse_kinematic(
            joint_target_position_urdf[4],
            joint_target_position_urdf[5],
            joint_target_position_urdf[10],
            joint_target_position_urdf[11],
        )

        # output
        self.work_space = work_space
        for i in range(self.number_of_joint):
            self.joints[i].set_target_control_mode(control_mode[i])
            self.joints[i].set_target_position(joint_target_position[i])
        # fmt: on

        return FunctionResult.SUCCESS

    def task_simple_rl_airtime_stack_control(self):
        return FunctionResult.SUCCESS

    # ==================================================================================================
