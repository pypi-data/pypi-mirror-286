import numpy
from fourier_core.logger.fi_logger import Logger
from fourier_core.predefine.fi_actuator_control_mode import ActuatorControlMode
from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_joint_control_mode import JointControlMode
from fourier_core.predefine.fi_robot_work_space import RobotWorkSpace
from fourier_core.predefine.fi_task_stage import TaskStage


class RobotGR1NohlaAlgorithmBasicControlModel:
    def __init__(self):
        self.stage = TaskStage.STAGE_INIT

        # --------------------------------------------------------------------
        # real robot
        self.num_of_joints = 6 + 6 + 3 + 4 + 4

        self.flag_joint_pd_position_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_pd_torque_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_position_control = FlagState.SET * numpy.ones(self.num_of_joints)
        self.flag_joint_velocity_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)
        self.flag_joint_kinetic_control = FlagState.CLEAR * numpy.ones(self.num_of_joints)

        self.index_of_joints_real_robot = numpy.array(
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
                14,  # waist
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
        # --------------------------------------------------------------------

        self.num_of_joints_controlled = 6 + 6 + 3 + 4 + 4
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
                12,
                13,
                14,  # waist
                15,
                16,
                17,
                18,  # left arm
                19,
                20,
                21,
                22,  # right arm
            ]
        )
        self.joint_default_position = numpy.array(
            [
                0.0,
                0.0,
                -0.5236,
                1.0472,
                -0.5236,
                0.0,  # left leg
                0.0,
                0.0,
                -0.5236,
                1.0472,
                -0.5236,
                0.0,  # right leg
                0.0,
                0.0,
                0.0,  # waist
                0.0,
                0.3,
                0.0,
                -0.3,  # left arm
                0.0,
                -0.3,
                0.0,
                -0.3,  # right arm
            ]
        )


class RobotGR1NohlaAlgorithmStandControlModel(RobotGR1NohlaAlgorithmBasicControlModel):
    def __init__(self, dt=0.01):
        super().__init__()

        self.dt = dt

        """
        Move robot to stand position in motion period
        """
        self.motion_period = 2.0  # unit : s
        self.motion_dt = self.dt
        self.motion_t = 0
        self.motion_ratio = 0

        self.target_velocity = 0.0
        self.target_direction = 0.0

        self.joint_start_position = numpy.zeros(self.num_of_joints)
        self.joint_target_position = numpy.array(
            [
                0.0,
                0.0,
                -0.5236,
                1.0472,
                -0.5236,
                0.0,  # left leg (6)
                0.0,
                0.0,
                -0.5236,
                1.0472,
                -0.5236,
                0.0,  # right leg (6)
                0.0,
                0.0,
                0.0,  # waist (3)
                0.0,
                0.3,
                0.0,
                -0.3,  # left arm (4)
                0.0,
                -0.3,
                0.0,
                -0.3,  # right arm (4)
            ]
        )

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
        joint_measured_position_urdf,  # rad
        joint_measured_velocity_urdf,  # rad/s
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
            # reset t
            self.motion_t = 0

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
            # reset t
            self.motion_t = 0

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
            self.motion_ratio = self.motion_t / self.motion_period

            self.output_work_space = RobotWorkSpace.JOINT_SPACE
            self.output_joint_control_mode = numpy.ones(self.num_of_joints) * JointControlMode.POSITION
            self.output_joint_position = numpy.zeros(self.num_of_joints)
            self.output_joint_velocity = numpy.zeros(self.num_of_joints)
            self.output_joint_kinetic = numpy.zeros(self.num_of_joints)

            # move from start position to target position
            self.output_joint_position = (
                self.joint_start_position + (self.joint_target_position - self.joint_start_position) * self.motion_ratio
            )

            # add dt
            self.motion_t += self.motion_dt

            if self.motion_t >= self.motion_period:
                self.motion_t = self.motion_period

                # update task stage
                self.stage = TaskStage.STAGE_PROCESS_2

            Logger().print_trace("motion_ratio = ", round(self.motion_ratio * 100, 1), "%")
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
