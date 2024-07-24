from math import asin, sqrt

import numpy as np


#################### working range ####################
# motor: -60~30 deg # -1.0472~0.5236 rad # forwad input
# ankle(roll): -25~25 deg, -0.43663~0.4363 rad
# ankle(pitch): -60~30 deg, -1.0472~0.5236 rad
#######################################################


# @njit
# def single_radian_rotation_matrix(angle_radian: float):
#     return np.array([[np.cos(angle_radian), 0, np.sin(angle_radian)],
#                      [0, 1, 0],
#                      [-np.sin(angle_radian), 0, np.cos(angle_radian)]])


# @njit
# def radian_to_rotation_matrix(roll: np.float64, pitch: np.float64) -> np.ndarray:
#     roll_matrix = np.array([[1, 0, 0],
#                             [0, np.cos(roll), -np.sin(roll)],
#                             [0, np.sin(roll), np.cos(roll)]])
#     pitch_matrix = np.array([[np.cos(pitch), 0, np.sin(pitch)],
#                              [0, 1, 0],
#                              [-np.sin(pitch), 0, np.cos(pitch)]])
#
#     return np.dot(pitch_matrix, roll_matrix)


# @njit
def single_radian_rotation_matrix(angle_radian: np.float64) -> np.ndarray:
    rotation_matrix = np.zeros((3, 3))
    rotation_matrix[0, 0] = np.cos(angle_radian)
    rotation_matrix[0, 2] = np.sin(angle_radian)
    rotation_matrix[1, 1] = 1
    rotation_matrix[2, 0] = -np.sin(angle_radian)
    rotation_matrix[2, 2] = np.cos(angle_radian)

    return rotation_matrix


# @njit
def radian_to_rotation_matrix(roll: np.float64, pitch: np.float64) -> np.ndarray:
    roll_matrix = np.zeros((3, 3))
    roll_matrix[0, 0] = 1
    roll_matrix[1, 1] = np.cos(roll)
    roll_matrix[1, 2] = -np.sin(roll)
    roll_matrix[2, 1] = np.sin(roll)
    roll_matrix[2, 2] = np.cos(roll)

    pitch_matrix = np.zeros((3, 3))
    pitch_matrix[0, 0] = np.cos(pitch)
    pitch_matrix[0, 2] = np.sin(pitch)
    pitch_matrix[1, 1] = 1
    pitch_matrix[2, 0] = -np.sin(pitch)
    pitch_matrix[2, 2] = np.cos(pitch)

    return np.dot(pitch_matrix, roll_matrix)


class ParallelAnkle:
    def __init__(self, type):
        # params and configuration
        if type == "left":
            self.isLeft = True
            self.initial_ra1 = np.array([0, 13.5, 260])  # 初始化位置参数、连杆长度、踝关节旋转角度和力矩、旋量
            self.initial_ra2 = np.array([0, -13.5, 205])
            self.initial_rb1 = np.array([-48.6, 13.5, 261.175])
            self.initial_rb2 = np.array([-48.6, -13.5, 206.175])
            self.initial_rc1 = np.array([-48.6, 13.5, 11.75])
            self.initial_rc2 = np.array([-48.6, -13.5, 11.75])
            self.length_bar1 = 50
            self.length_bar2 = 50
            self.length_rod1 = 260
            self.length_rod2 = 205
            self.initial_offset = 13.592
        elif type == "right":
            self.isLeft = False
            self.initial_ra1 = np.array([0, 13.5, 205])
            self.initial_ra2 = np.array([0, -13.5, 260])
            self.initial_rb1 = np.array([-48.6, 13.5, 206.175])
            self.initial_rb2 = np.array([-48.6, -13.5, 261.175])
            self.initial_rc1 = np.array([-48.6, 13.5, 11.75])
            self.initial_rc2 = np.array([-48.6, -13.5, 11.75])
            self.length_bar1 = 50
            self.length_bar2 = 50
            self.length_rod1 = 205
            self.length_rod2 = 260
            self.initial_offset = 13.592

    def left_fk_nnfit(self, joint_position_l, joint_position_r):
        b_a = np.array(
            [
                -2.2792546454185323,
                2.2642161570391197,
                -5.419533381900254,
                -1.915691720647261,
                2.20667472957695,
                -4.0443726872560584,
                1.9370889515946064,
                1.0739504098009056,
                -1.8632467259439971,
                1.3794682419244875,
                2.5770189400681622,
                -2.1938439630507691,
                2.6752919435360893,
                1.6818232580329802,
                2.9790245808193356,
                2.7062830131141613,
                0.8849362498980976,
                3.1216141438161111,
                -5.4526841316981951,
                1.4789170280789614,
                -3.9345802549850286,
                2.7553002923293928,
                0.34480576021622983,
                -1.29092834537273,
                2.1382719318545096,
                0.13395401627857628,
                1.4091544240304066,
                -0.21513449181541855,
                -0.76216858538701071,
                -1.5025938114862543,
                -1.1070469350120138,
                -0.43196775159217782,
                0.24865208537160069,
                -0.86809285431090422,
                0.099145682132757956,
                -0.1093867848552806,
                -1.4906818952515357,
                0.82368244892761133,
                4.9456496779954477,
                -4.7632844976231086,
            ]
        )

        c_a = np.array(
            [
                0.13700008575098083,
                -0.17970111430946503,
                -0.13728828485551844,
                0.14341536595962917,
                -0.0041435932541297738,
                -0.0026507082038324322,
                0.92599119212395808,
                0.89506748407848913,
                -0.13267394702829918,
                0.12094814624573325,
                -0.00036261233082175774,
                -0.0043091065610663783,
                -0.23477628205184298,
                0.19502389526018549,
                2.0507978586597861,
                -0.41385306672015304,
                0.48327831043846237,
                -0.35243608493642742,
                4.0790859699896718,
                0.59415870313261743,
                -0.36752870712957453,
                0.17023789862011998,
                0.46860649831163975,
                -0.3208008035398221,
                -0.33645360185878503,
                0.22883368804503318,
                4.2480842959405143,
                -1.3676397512237475,
                -0.29845598327405187,
                0.19481289162255663,
                -0.79390564088219273,
                0.59011459551379652,
                0.39420597295114185,
                0.47584468920566236,
                0.13767415419488063,
                0.70467209477475568,
                -1.5040962709012431,
                0.82111668960622075,
                0.13483966009831111,
                1.1394953574383444,
            ]
        )

        a = np.array(
            [
                6.6097739168512195,
                -4.3746628470892581,
                4.3451446765837263,
                -4.0616625822810581,
                -3.0355290573446623,
                2.4482245431249412,
                -1.7315358824244333,
                -0.35567821597187149,
                0.70531918341902022,
                -1.4132241521957059,
                0.98268954825621635,
                -0.098766309516276574,
                0.90142699726273123,
                0.9204094940529709,
                1.7099018311114502,
                2.2885458933009093,
                1.3270497738955489,
                4.54352002008784,
                -3.9154174199487719,
                6.4700366388067057,
            ]
        )

        b = np.zeros(20)
        xp1 = np.array([0.75434480807696935, 0.60570604138673634])
        ankle_position = np.zeros(2)

        d = (joint_position_l - -1.1522) * 1.11738085926588 + -1.0
        d1 = (joint_position_r - -1.1526) * 1.11752445981661 + -1.0

        for k in range(20):
            b[k] = 2.0 / (np.exp(-2.0 * (a[k] + (b_a[k] * d + b_a[k + 20] * d1))) + 1.0) - 1.0

        for k in range(2):
            d = 0.0
            for i in range(20):
                d += c_a[k + (i << 1)] * b[i]
            ankle_position[k] = ((xp1[k] + d) - -1.0) \
                                / (-1.01860676223578 * float(k) + 2.29184332958999) \
                                + (-0.61086999999999991 * float(k) + -0.43633)

        # (ankle_position_roll, ankle_position_pitch)
        return ankle_position[0], ankle_position[1]

    def right_fk_nnfit(self, joint_position_l, joint_position_r):
        b_a = np.array(
            [
                -2.2792546454185323,
                2.2642161570391197,
                -5.419533381900254,
                -1.915691720647261,
                2.20667472957695,
                -4.0443726872560584,
                1.9370889515946064,
                1.0739504098009056,
                -1.8632467259439971,
                1.3794682419244875,
                2.5770189400681622,
                -2.1938439630507691,
                2.6752919435360893,
                1.6818232580329802,
                2.9790245808193356,
                2.7062830131141613,
                0.8849362498980976,
                3.1216141438161111,
                -5.4526841316981951,
                1.4789170280789614,
                -3.9345802549850286,
                2.7553002923293928,
                0.34480576021622983,
                -1.29092834537273,
                2.1382719318545096,
                0.13395401627857628,
                1.4091544240304066,
                -0.21513449181541855,
                -0.76216858538701071,
                -1.5025938114862543,
                -1.1070469350120138,
                -0.43196775159217782,
                0.24865208537160069,
                -0.86809285431090422,
                0.099145682132757956,
                -0.1093867848552806,
                -1.4906818952515357,
                0.82368244892761133,
                4.9456496779954477,
                -4.7632844976231086,
            ]
        )

        c_a = np.array(
            [
                0.13700008575098083,
                -0.17970111430946503,
                -0.13728828485551844,
                0.14341536595962917,
                -0.0041435932541297738,
                -0.0026507082038324322,
                0.92599119212395808,
                0.89506748407848913,
                -0.13267394702829918,
                0.12094814624573325,
                -0.00036261233082175774,
                -0.0043091065610663783,
                -0.23477628205184298,
                0.19502389526018549,
                2.0507978586597861,
                -0.41385306672015304,
                0.48327831043846237,
                -0.35243608493642742,
                4.0790859699896718,
                0.59415870313261743,
                -0.36752870712957453,
                0.17023789862011998,
                0.46860649831163975,
                -0.3208008035398221,
                -0.33645360185878503,
                0.22883368804503318,
                4.2480842959405143,
                -1.3676397512237475,
                -0.29845598327405187,
                0.19481289162255663,
                -0.79390564088219273,
                0.59011459551379652,
                0.39420597295114185,
                0.47584468920566236,
                0.13767415419488063,
                0.70467209477475568,
                -1.5040962709012431,
                0.82111668960622075,
                0.13483966009831111,
                1.1394953574383444,
            ]
        )

        a = np.array(
            [
                6.6097739168512195,
                -4.3746628470892581,
                4.3451446765837263,
                -4.0616625822810581,
                -3.0355290573446623,
                2.4482245431249412,
                -1.7315358824244333,
                -0.35567821597187149,
                0.70531918341902022,
                -1.4132241521957059,
                0.98268954825621635,
                -0.098766309516276574,
                0.90142699726273123,
                0.9204094940529709,
                1.7099018311114502,
                2.2885458933009093,
                1.3270497738955489,
                4.54352002008784,
                -3.9154174199487719,
                6.4700366388067057,
            ]
        )

        b = np.zeros(20)
        xp1 = np.array([0.75434480807696935, 0.60570604138673634])
        ankle_position = np.zeros(2)

        d = (joint_position_l - -1.1522) * 1.11738085926588 + -1.0
        d1 = (joint_position_r - -1.1526) * 1.11752445981661 + -1.0

        for k in range(20):
            b[k] = 2.0 / (np.exp(-2.0 * (a[k] + (b_a[k] * d + b_a[k + 20] * d1))) + 1.0) - 1.0

        for k in range(2):
            d = 0.0
            for i in range(20):
                d += c_a[k + (i << 1)] * b[i]
            ankle_position[k] = ((xp1[k] + d) - -1.0) \
                                / (-1.01860676223578 * float(k) + 2.29184332958999) \
                                + (-0.61086999999999991 * float(k) + -0.43633)

        # (ankle_position_roll, ankle_position_pitch)
        return ankle_position[0], ankle_position[1]

    def forward(
            self,
            joint_position_up_deg,
            joint_position_lower_deg,
            joint_velocity_up_deg=0,
            joint_velocity_lower_deg=0,
            joint_torque_up=0,
            joint_torque_lower=0,
    ):
        # ankle position
        if self.isLeft:
            joint_position_l = np.deg2rad(joint_position_up_deg)
            joint_position_r = np.deg2rad(joint_position_lower_deg)
            joint_velocity_l = np.deg2rad(joint_velocity_up_deg)
            joint_velocity_r = np.deg2rad(joint_velocity_lower_deg)
            joint_torque_l = joint_torque_up
            joint_torque_r = joint_torque_lower
            ankle_position_roll, ankle_position_pitch = self.left_fk_nnfit(joint_position_l, joint_position_r)
        else:
            joint_position_l = np.deg2rad(joint_position_lower_deg)
            joint_position_r = np.deg2rad(joint_position_up_deg)
            joint_velocity_l = np.deg2rad(joint_velocity_lower_deg)
            joint_velocity_r = np.deg2rad(joint_velocity_up_deg)
            joint_torque_l = joint_torque_lower
            joint_torque_r = joint_torque_up
            ankle_position_roll, ankle_position_pitch = self.right_fk_nnfit(joint_position_l, joint_position_r)

        rotation_matrix = radian_to_rotation_matrix(ankle_position_roll, ankle_position_pitch)
        target_rc1 = np.dot(rotation_matrix, self.initial_rc1)
        target_rc2 = np.dot(rotation_matrix, self.initial_rc2)
        target_ra1 = self.initial_ra1
        target_ra2 = self.initial_ra2

        # 根据角度得到旋转矩阵
        single_rotation_matrix_l = single_radian_rotation_matrix(joint_position_l)
        single_rotation_matrix_r = single_radian_rotation_matrix(joint_position_r)

        # 踝关节目标位置参数
        target_rb1 = target_ra1 + np.dot(single_rotation_matrix_l, (self.initial_rb1 - self.initial_ra1))
        target_rb2 = target_ra2 + np.dot(single_rotation_matrix_r, (self.initial_rb2 - self.initial_ra2))

        # bar和rod的向量表示
        r_bar1 = target_rb1 - target_ra1
        r_bar2 = target_rb2 - target_ra2
        r_rod1 = target_rc1 - target_rb1
        r_rod2 = target_rc2 - target_rb2

        # 旋量中的方向向量
        s11 = np.array([0, 1, 0])
        s21 = np.array([0, 1, 0])

        # Jx
        Jx = np.array(
            [
                r_rod1.tolist() + (np.cross(target_rc1, r_rod1)).tolist(),
                r_rod2.tolist() + (np.cross(target_rc2, r_rod2)).tolist(),
            ]
        )

        # J_theta
        J_theta = np.array([[np.dot(s11, np.cross(r_bar1, r_rod1)), 0],
                            [0, np.dot(s21, np.cross(r_bar2, r_rod2))]])

        # G_matrix
        G_matrix = np.array(
            [[0, 0, 0, np.cos(ankle_position_pitch), 0, -np.sin(ankle_position_pitch)],
             [0, 0, 0, 0, 1, 0]]
        ).T

        # ankle velocity
        joint_velocity = np.array([joint_velocity_l, joint_velocity_r])
        ankle_velocity_roll, ankle_velocity_pitch = np.linalg.inv(
            np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))
        ).dot(joint_velocity)

        # ankle torque
        joint_torque = np.array([joint_torque_l, joint_torque_r])
        ankle_torque_roll, ankle_torque_pitch = np.linalg.inv(
            np.linalg.inv(np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))).T
        ).dot(joint_torque)

        return (
            np.rad2deg(ankle_position_pitch),
            np.rad2deg(ankle_position_roll),
            np.rad2deg(ankle_velocity_pitch),
            np.rad2deg(ankle_velocity_roll),
            (ankle_torque_pitch),
            (ankle_torque_roll),
        )  # numpy.floa64

    def inverse(
            self,
            ankle_position_pitch_deg,
            ankle_position_roll_deg,
            ankle_velocity_pitch_deg=0,
            ankle_velocity_roll_deg=0,
            ankle_torque_pitch=0,
            ankle_torque_roll=0,
    ):
        ankle_position_pitch = np.deg2rad(ankle_position_pitch_deg)
        ankle_position_roll = np.deg2rad(ankle_position_roll_deg)
        ankle_velocity_pitch = np.deg2rad(ankle_velocity_pitch_deg)
        ankle_velocity_roll = np.deg2rad(ankle_velocity_roll_deg)
        ankle_torque_pitch = ankle_torque_pitch
        ankle_torque_roll = ankle_torque_roll

        rotation_matrix = radian_to_rotation_matrix(ankle_position_roll, ankle_position_pitch)

        # 旋转后的关节点
        target_rc1 = np.dot(rotation_matrix, self.initial_rc1)
        target_rc2 = np.dot(rotation_matrix, self.initial_rc2)
        target_ra1 = self.initial_ra1
        target_ra2 = self.initial_ra2

        # 得到计算公式的元素
        interm_a1 = target_rc1 - target_ra1
        a1 = interm_a1[0]
        interm_a2 = target_rc2 - target_ra2
        a2 = interm_a2[0]
        interm_b1 = target_ra1 - target_rc1
        b1 = interm_b1[2]
        interm_b2 = target_ra2 - target_rc2
        b2 = interm_b2[2]

        # 计算二阶范数
        norm_1 = np.linalg.norm(target_rc1 - target_ra1, ord=2)
        norm_2 = np.linalg.norm(target_rc2 - target_ra2, ord=2)

        c1 = (self.length_rod1 ** 2 - self.length_bar1 ** 2 - norm_1 ** 2) / (2 * self.length_bar1)
        c2 = (self.length_rod2 ** 2 - self.length_bar2 ** 2 - norm_2 ** 2) / (2 * self.length_bar2)

        # joint position
        joint_position_l = asin(
            (b1 * c1 + sqrt(b1 ** 2 * c1 ** 2 - (a1 ** 2 + b1 ** 2) * (c1 ** 2 - a1 ** 2))) / (a1 ** 2 + b1 ** 2)
        ) - np.deg2rad(self.initial_offset)
        joint_position_r = asin(
            (b2 * c2 + sqrt(b2 ** 2 * c2 ** 2 - (a2 ** 2 + b2 ** 2) * (c2 ** 2 - a2 ** 2))) / (a2 ** 2 + b2 ** 2)
        ) - np.deg2rad(self.initial_offset)

        single_rotation_matrix_l = single_radian_rotation_matrix(joint_position_l)
        single_rotation_matrix_r = single_radian_rotation_matrix(joint_position_r)

        # 踝关节目标位置参数
        target_rb1 = target_ra1 + np.dot(single_rotation_matrix_l, (self.initial_rb1 - self.initial_ra1))
        target_rb2 = target_ra2 + np.dot(single_rotation_matrix_r, (self.initial_rb2 - self.initial_ra2))

        # bar和rod的向量表示
        r_bar1 = target_rb1 - target_ra1
        r_bar2 = target_rb2 - target_ra2
        r_rod1 = target_rc1 - target_rb1
        r_rod2 = target_rc2 - target_rb2

        # 旋量中的方向向量
        s11 = np.array([0, 1, 0])
        s21 = np.array([0, 1, 0])

        # 雅可比矩阵的组成部分
        # Jx
        Jx = np.array(
            [
                r_rod1.tolist() + (np.cross(target_rc1, r_rod1)).tolist(),
                r_rod2.tolist() + (np.cross(target_rc2, r_rod2)).tolist(),
            ]
        )

        # J_theta
        J_theta = np.array([[np.dot(s11, np.cross(r_bar1, r_rod1)), 0],
                            [0, np.dot(s21, np.cross(r_bar2, r_rod2))]])

        # G_matrix
        G_matrix = np.array(
            [[0, 0, 0, np.cos(ankle_position_pitch), 0, -np.sin(ankle_position_pitch)],
             [0, 0, 0, 0, 1, 0]]
        ).T

        # joint velocity
        ankle_velocity = np.array([ankle_velocity_roll, ankle_velocity_pitch])
        joint_velocity_l, joint_velocity_r = np.dot(
            np.linalg.inv(J_theta),
            np.dot(Jx, G_matrix)
        ).dot(ankle_velocity)

        # joint torque
        ankle_torque = np.array([ankle_torque_roll, ankle_torque_pitch])
        joint_torque_l, joint_torque_r = np.linalg.inv(
            np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))
        ).T.dot(ankle_torque)

        if self.isLeft:
            return (
                np.rad2deg(joint_position_l),
                np.rad2deg(joint_position_r),
                np.rad2deg(joint_velocity_l),
                np.rad2deg(joint_velocity_r),
                (joint_torque_l),
                (joint_torque_r),
            )
        else:
            return (
                np.rad2deg(joint_position_r),
                np.rad2deg(joint_position_l),
                np.rad2deg(joint_velocity_r),
                np.rad2deg(joint_velocity_l),
                (joint_torque_r),
                (joint_torque_l),
            )


if __name__ == "__main__":
    import random
    import time

    # 测试逆运动学计算
    parallel_ankle = ParallelAnkle("left")

    test_round = 1000

    for i in range(test_round):
        if i == 1:
            start_time = time.time()

        ankle_position_pitch_deg = random.uniform(-60, 30)
        ankle_position_roll_deg = random.uniform(-25, 25)
        ankle_velocity_pitch_deg = 0
        ankle_velocity_roll_deg = 0
        ankle_torque_pitch = 0
        ankle_torque_roll = 0

        (joint_position_l, joint_position_r, joint_velocity_l, joint_velocity_r, joint_torque_l, joint_torque_r) = (
            parallel_ankle.inverse(
                ankle_position_pitch_deg,
                ankle_position_roll_deg,
                ankle_velocity_pitch_deg,
                ankle_velocity_roll_deg,
                ankle_torque_pitch,
                ankle_torque_roll,
            )
        )

    stop_time = time.time()

    print("calculate time: ", (stop_time - start_time) / (test_round - 1))

    print("joint_position_l: ", joint_position_l)
    print("joint_position_r: ", joint_position_r)
