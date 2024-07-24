import json
import os
import time

import numpy
from fourier_core.actuator.fi_actuator_fi_fsa import ActuatorFIFSA
from fourier_core.config.fi_config import gl_config
from fourier_core.logger.fi_logger import Logger
from fourier_core.predefine.fi_deploy_mode import DeployMode
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_function_result import FunctionResult
from fourier_core.robot.fi_robot_base_task import RobotBaseTask
from fourier_core.sensor.fi_sensor_fi_fse import SensorFIFSE
from fourier_grx.robot.gr1.fi_parallel_ankle_gr1_t3 import ParallelAnkle
from fourier_grx.robot.gr1.fi_parallel_wrist_gr1_t3 import ParallelWrist
from fourier_grx.robot.gr1.fi_robot_gr1_t2 import RobotGR1T2


class RobotGR1T3(RobotGR1T2):
    def __init__(self):
        super(RobotGR1T3, self).__init__()

        # sensor
        self.number_of_sensor_fi_fse = 2 + 2
        self.sensor_fi_fse_direction = numpy.array(
            [
                1.0,
                -1.0,  # left leg (ankle)
                -1.0,
                1.0,  # right leg (ankle)
            ]
        )
        self.sensor_fi_fse_reduction_ratio = numpy.array(
            [
                1.0,
                1.0,  # left leg (ankle)
                1.0,
                1.0,  # right leg (ankle)
            ]
        )
        # Jason 2024-01-22:
        # as the fi_fse have value jump from 0 <--> 360,
        # we set 180 raw angle value as target home angle
        self.sensor_fi_fse_sensor_offset = numpy.array(
            [
                0.0,
                0.0,  # left leg (ankle)
                0.0,
                0.0,  # right leg (ankle)
            ]
        )
        self.sensor_fi_fse = []
        for i in range(self.number_of_sensor_fi_fse):
            self.sensor_fi_fse.append(
                SensorFIFSE(
                    ip=gl_config.parameters["sensor_abs_encoder"]["ip"][i],
                    direction=self.sensor_fi_fse_direction[i],
                    reduction_ratio=self.sensor_fi_fse_reduction_ratio[i],
                    sensor_offset=self.sensor_fi_fse_sensor_offset[i],
                )
            )

        self.indexes_of_joints_match_sensor_fi_fse = numpy.array(
            [
                4,
                5,  # left leg (ankle)
                10,
                11,  # right leg (ankle)
            ]
        )  # must match the number of sensor_fi_fse

        # actuator
        # ...

        # joint
        # ...

        # joint -> joint urdf
        self.parallel_ankle_left = ParallelAnkle("left")
        self.parallel_ankle_right = ParallelAnkle("right")
        self.parallel_wrist_left = ParallelWrist("left")
        self.parallel_wrist_right = ParallelWrist("right")

        self.indexes_of_lower_body_joints = numpy.array(
            [
                # left leg
                0,
                1,
                2,
                3,
                4,
                5,
                # right leg
                6,
                7,
                8,
                9,
                10,
                11,
            ]
        )
        self.number_of_lower_body_joints = len(self.indexes_of_lower_body_joints)

        self.indexes_of_upper_body_joints = numpy.array(
            [
                # waist
                12,
                13,
                14,
                # head
                15,
                16,
                17,
                # left arm
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                # right arm
                25,
                26,
                27,
                28,
                29,
                30,
                31,
            ]
        )
        self.number_of_upper_body_joints = len(self.indexes_of_upper_body_joints)

        # link
        # ...

        # end effector
        # ...

        # base and legs
        # ...

        # robot
        # ...

        # control algorithm

        # task
        self.tasks.extend([])

        self.task_algorithm_models.update({})

        self.task_functions.update({})

        # flag
        # ...

        # state estimator
        self.state_estimator = None

        # get current file path
        # current_workspace_path = os.getcwd()
        # model_file_path = current_workspace_path + "/model/model.json"
        # print("state_estimator model_file_path = \n", model_file_path)
        #
        # self.state_estimator.init(model_file_path, 0.0025)

    def prepare(self) -> FunctionResult:
        if self.deploy_mode == DeployMode.DEFAULT or self.deploy_mode == DeployMode.DEVELOPER_MODE or self.deploy_mode == DeployMode.SDK_MODE:
            joint_home_position = numpy.zeros(self.number_of_joint)

            # fi_fsa --------------------------------------------------------------

            # Note:
            # The fi_fsa v2 provide the absolute position value,
            # some joints use the fi_fsa v2 will have the absolute position value when call get_pvc()

            # fi_fsa --------------------------------------------------------------

            # fi_fse --------------------------------------------------------------

            # read stored abs encoder angle
            Logger().print_trace("RobotGR1 prepare() read stored abs encoder calibrate value")
            map_fi_fses_values_stored = None
            sensor_abs_encoder_data_path = gl_config.parameters["sensor_abs_encoder"].get(
                "data_path", "./sensor_offset.json"
            )

            if os.path.exists(sensor_abs_encoder_data_path):
                Logger().print_trace("home_angle file exists")

                with open(sensor_abs_encoder_data_path) as file:
                    json_fi_fses_angle_value = file.read()
                    map_fi_fses_values_stored = json.loads(json_fi_fses_angle_value)

                Logger().print_trace_highlight("home_angle = \n", str(json_fi_fses_angle_value))

                # set flag_calibration
                self.flag_calibration = FlagState.SET

            else:
                Logger().print_trace_error(
                    sensor_abs_encoder_data_path, " file not exists, please do TASK_SET_HOME first"
                )

                # clear flag_calibration
                self.flag_calibration = FlagState.CLEAR

            # load file config
            if map_fi_fses_values_stored is not None:
                for i in range(self.number_of_sensor_fi_fse):
                    if self.sensor_fi_fse[i] is not None:
                        ip = self.sensor_fi_fse[i].ip
                        sensor_offset = map_fi_fses_values_stored[ip]

                        self.sensor_fi_fse[i].sensor_offset = sensor_offset
                    else:
                        pass

            # sensor
            Logger().print_trace("RobotGR1 prepare() upload fi_fse value")
            for i in range(self.number_of_sensor_fi_fse):
                if self.sensor_fi_fse[i] is not None:
                    self.sensor_fi_fse[i].upload()

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

            print("joint_group_measured_position = \n", numpy.round(self.joint_group_measured_position, 1))

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

            Logger().print_trace("Finish joint home position calibration !")

        else:
            Logger().print_trace_warning("Unknown deploy mode: " + str(self.deploy_mode))

        return FunctionResult.SUCCESS

    def task_set_home(self):
        # fi_fsa --------------------------------------------------------------

        for i in range(self.number_of_actuator):
            actuator: ActuatorFIFSA = self.actuators[i]
            abs_position = actuator.upload_abs_position()
            result = actuator.download_abs_offset(abs_offset=abs_position)
            if result != FunctionResult.SUCCESS:
                Logger().print_trace_warning(actuator.ip, "actuator.download_abs_offset() failed")

        # fi_fsa --------------------------------------------------------------

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
