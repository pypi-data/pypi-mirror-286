import numpy
from fourier_grx.robot.gr1.fi_robot_gr1_t1 import RobotGR1T1


class RobotGR1T1V2(RobotGR1T1):
    def __init__(self):
        super().__init__()

        # sensor
        # ...

        # actuator
        # ...

        # joint
        # l_hip_roll change: 802030 -> 8029E
        # r_hip_roll change: 802030 -> 8029E
        index_list_joint_change = numpy.array(
            [
                0,
                6,
            ]
        )
        direction_joint_change = numpy.array(
            [
                -1.0,
                -1.0,
            ]
        )
        home_position_joint_change = (
                numpy.array(
                    [
                        0.0,
                        0.0,
                    ]
                )
                * 180.0
                / numpy.pi
        )
        min_position_joint_change = (
                numpy.array(
                    [
                        -0.09,
                        -0.09,
                    ]
                )
                * 180.0
                / numpy.pi
        )
        max_position_joint_change = (
                numpy.array(
                    [
                        0.79,
                        0.79,
                    ]
                )
                * 180.0
                / numpy.pi
        )
        reduction_ratio_joint_change = numpy.array(
            [
                29.0,
                29.0,
            ]
        )
        kinematic_reduction_ratio_joint_change = numpy.array(
            [
                1,
                1,
            ]
        )
        kinetic_reduction_ratio_joint_change = (
                numpy.array(
                    [
                        1.0,
                        1.0,
                    ]
                )
                * reduction_ratio_joint_change
        )
        position_control_kp = numpy.array(
            [
                0.99715523,
                0.99715523,
            ]
        )
        velocity_control_kp = numpy.array(
            [
                0.07590791,
                0.07590791,
            ]
        )

        for i in range(len(index_list_joint_change)):
            index = index_list_joint_change[i]
            self.joints[index].direction = direction_joint_change[i]
            self.joints[index].home_position = home_position_joint_change[i]
            self.joints[index].min_position = min_position_joint_change[i]
            self.joints[index].max_position = max_position_joint_change[i]
            self.joints[index].reduction_ratio = reduction_ratio_joint_change[i]
            self.joints[index].kinematic_reduction_ratio = kinematic_reduction_ratio_joint_change[i]
            self.joints[index].kinetic_reduction_ratio = kinetic_reduction_ratio_joint_change[i]
            # pid
            self.joints[index].set_target_position_control_kp(position_control_kp[i])
            self.joints[index].set_target_velocity_control_kp(velocity_control_kp[i])
            self.joints[index].set_target_velocity_control_ki(0)

        # joint -> joint urdf
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
