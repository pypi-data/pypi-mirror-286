import numpy
from fourier_core.logger.fi_logger import Logger
from fourier_core.predefine.fi_actuator_control_mode import ActuatorControlMode
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_joint_control_mode import JointControlMode
from fourier_core.predefine.fi_robot_work_space import RobotWorkSpace
from fourier_core.predefine.fi_task_stage import TaskStage


class RobotGR1NowhlaAlgorithmBasicControlModel:
    def __init__(self):
        self.num_of_joints = 6 + 6 + 4 + 4
        self.joint_default_position = numpy.array(
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
        )

        self.num_of_joints_controlled = 6 + 6 + 4 + 4
        self.index_of_joints_controlled = numpy.array(
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

        self.flag_joint_pd_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_pd_torque_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_velocity_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_kinetic_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)


class RobotGR1NowhlaAlgorithmStandControlModel(RobotGR1NowhlaAlgorithmBasicControlModel):
    def __init__(self):
        super().__init__()

        self.target_velocity = 0.0
        self.target_direction = 0.0

        self.stage = 0

        self.joint_start_position = numpy.zeros(self.num_of_joints)
        self.joint_target_position = numpy.array(
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
        )

        self.transform_move_count = 0
        self.transform_move_count_max = 100
        self.transform_move_ratio = 0

        self.output_work_space = RobotWorkSpace.NONE

        self.output_actuator_control_mode = numpy.zeros(self.num_of_joints)
        self.output_actuator_position = numpy.zeros(self.num_of_joints)
        self.output_actuator_velocity = numpy.zeros(self.num_of_joints)
        self.output_actuator_kinetic = numpy.zeros(self.num_of_joints)

        self.output_joint_control_mode = numpy.zeros(self.num_of_joints)
        self.output_joint_position = numpy.zeros(self.num_of_joints)
        self.output_joint_velocity = numpy.zeros(self.num_of_joints)
        self.output_joint_kinetic = numpy.zeros(self.num_of_joints)

    def run(
        self,
        joint_measured_position_urdf,
        joint_measured_velocity_urdf,
    ):
        """
        Input:
        joint_measured_position_urdf: measured joint position in URDF, rad
        joint_measured_velocity_urdf: measured joint velocity in URDF, rad/s

        Output:
        work_space: work space of output joint control target
        control_mode: control mode of output joint control target
        joint_pd_control_target: output joint control target, rad
        """

        # use measured position as default pd target
        work_space = RobotWorkSpace.NONE
        control_mode = 0
        joint_pd_control_target = joint_measured_position_urdf

        if self.stage == TaskStage.STAGE_INIT:
            # reset count and ratio
            self.transform_move_count = 0
            self.transform_move_ratio = 0

            # reset start position
            self.joint_start_position = joint_measured_position_urdf

            self.output_work_space = RobotWorkSpace.ACTUATOR_SPACE
            self.output_actuator_control_mode = ActuatorControlMode.SERVO_ON * numpy.ones(self.num_of_joints)

            # output
            work_space = self.output_work_space
            control_mode = self.output_actuator_control_mode

            # update task stage
            self.stage = TaskStage.STAGE_START

        elif self.stage == TaskStage.STAGE_START:
            # reset count
            self.transform_move_count = 0

            # reset start position
            self.joint_start_position = joint_measured_position_urdf

            self.output_work_space = RobotWorkSpace.JOINT_SPACE
            self.output_joint_control_mode = numpy.ones(self.num_of_joints) * JointControlMode.POSITION
            self.output_joint_position = numpy.zeros(self.num_of_joints)
            self.output_joint_velocity = numpy.zeros(self.num_of_joints)
            self.output_joint_kinetic = numpy.zeros(self.num_of_joints)

            # move to start position
            self.output_joint_position = self.joint_start_position

            # output
            work_space = self.output_work_space
            control_mode = self.output_joint_control_mode
            joint_pd_control_target = self.output_joint_position

            # update task stage
            self.stage = TaskStage.STAGE_PROCESS_1

        elif self.stage == TaskStage.STAGE_PROCESS_1:
            # update ratio
            self.transform_move_ratio = self.transform_move_count / self.transform_move_count_max

            self.output_work_space = RobotWorkSpace.JOINT_SPACE
            self.output_joint_control_mode = numpy.ones(self.num_of_joints) * JointControlMode.POSITION
            self.output_joint_position = numpy.zeros(self.num_of_joints)
            self.output_joint_velocity = numpy.zeros(self.num_of_joints)
            self.output_joint_kinetic = numpy.zeros(self.num_of_joints)

            # move from start position to target position
            self.output_joint_position = (
                self.joint_start_position
                + (self.joint_target_position - self.joint_start_position) * self.transform_move_ratio
            )

            # add count
            self.transform_move_count += 1

            if self.transform_move_count >= self.transform_move_count_max:
                self.transform_move_count = self.transform_move_count_max

                # update task stage
                self.stage = TaskStage.STAGE_PROCESS_2

            Logger().print_trace("transform_move_ratio = ", round(self.transform_move_ratio * 100, 1), "%")
            # Logger().print_trace("self.joint_target_position = ",
            #                      self.joint_target_position)
            # Logger().print_trace("joint_measured_position_value = ",
            #                      numpy.round(joint_measured_position_value, 3))

            # output
            work_space = self.output_work_space
            control_mode = self.output_joint_control_mode
            joint_pd_control_target = self.output_joint_position

        elif self.stage == TaskStage.STAGE_PROCESS_2:
            self.output_work_space = RobotWorkSpace.JOINT_SPACE
            self.output_joint_control_mode = numpy.ones(self.num_of_joints) * JointControlMode.POSITION
            self.output_joint_position = self.joint_target_position
            self.output_joint_velocity = numpy.zeros(self.num_of_joints)

            # output
            work_space = self.output_work_space
            control_mode = self.output_joint_control_mode
            joint_pd_control_target = self.output_joint_position

            # update task stage
            self.stage = TaskStage.STAGE_FINISH

        elif self.stage == TaskStage.STAGE_FINISH:
            # do not change anything

            # output
            work_space = self.output_work_space
            control_mode = self.output_joint_control_mode
            joint_pd_control_target = self.output_joint_position

        else:
            self.stage = TaskStage.STAGE_START

            # output
            work_space = self.output_work_space
            control_mode = self.output_joint_control_mode
            joint_pd_control_target = self.output_joint_position

        return work_space, control_mode, joint_pd_control_target
