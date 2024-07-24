from math import asin, sqrt

import numpy as np


##################### 注意 ######################
############# 输入输出已按照角度制统一 #############
# 坐标系已根据电机默认正方向与urdf定义的关节正方向匹配 #
# 正解的输入顺序为由上至下（即电机IP读取顺序）#########
# 逆解的输出顺序为先roll后pitch（即urdf定义顺序）#####
################################################


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


class ParallelWrist:
    def __init__(self, type):
        # params and configuration
        if type == "left":
            self.isLeft = True
        elif type == "right":
            self.isLeft = False
        self.initial_ra1 = np.array([-2.0, 12.0, 43.9])
        self.initial_ra2 = np.array([-2.0, -12.0, 43.9])
        self.initial_rb1 = np.array([-16.0, 12.0, 43.9])
        self.initial_rb2 = np.array([-16.0, -12.0, 43.9])
        self.initial_rc1 = np.array([-14.0, 12.0, 0])
        self.initial_rc2 = np.array([-14.0, -12.0, 0])
        self.length_bar1 = 14.0
        self.length_bar2 = 14.0
        self.length_rod1 = 44.0
        self.length_rod2 = 44.0
        self.initial_offset = 0.0

    # left and right hand share the same network
    def fk_nnfit(self, joint_position_1, joint_position_2):
        b_a = np.array(
            [
                3.256829015896376,
                2.962753256221569,
                -3.2258639433947778,
                4.3396088482741515,
                0.15097791754721515,
                -1.3575973708387647,
                -1.7133347785201343,
                0.28373699897767835,
                1.9346403561420413,
                0.87327116117021009,
                -1.7580991919638227,
                0.909333905922267,
                0.62349357172455455,
                -0.18472468511209295,
                1.3955085794998654,
                -4.5914330152678149,
                -0.89143801986317706,
                5.3419580654236931,
                1.3443320052939616,
                2.6259510473371752,
                1.5803670161716636,
                -4.5329840373558339,
                3.0586834432078587,
                -0.77398983003306909,
                5.300617558246393,
                -0.2104499034440987,
                1.2392257401142628,
                -2.405142351572688,
                -0.66960592465548074,
                -1.9098783358199691,
                0.86279498097011276,
                -1.0745074185726304,
                -0.48352136968853837,
                -1.9958186993538181,
                -1.550294573127724,
                1.9017516216170853,
                3.213509436889209,
                -2.7071470639825459,
                3.5425197755296516,
                -4.9113513616630735,
            ]
        )

        c_a = np.array(
            [
                0.013391334928815765,
                -0.02978364325669761,
                -0.20111957600053904,
                0.024021673066790889,
                -0.081969810709102434,
                0.13787338782954597,
                -0.017147442614174346,
                0.00010728337566475795,
                0.0027914012280719431,
                0.000791497014341046,
                1.9854981119451414,
                -0.054529020107155983,
                1.6392735982187034,
                1.102490623627123,
                0.68578657589805081,
                -0.27326908398587385,
                -1.2804238892796869,
                -0.29009337452949907,
                0.39647155319574046,
                -0.26301028552913586,
                -3.4428412227393692,
                -1.1553046444506005,
                0.50634925226696381,
                -3.1176068378909307,
                0.8092429798554025,
                7.2049057867288893,
                -0.62912311619228944,
                0.216840824788679,
                0.71298665908124081,
                -1.0837486542989647,
                2.0440080433076626,
                0.44468461836794132,
                1.3364138541947337,
                -0.35896361656303422,
                1.0527052374224177,
                0.252244814916979,
                0.83613010144624567,
                -0.10936919516966184,
                0.34914424692452273,
                -0.14131481801214235,
            ]
        )

        a = np.array(
            [
                -4.1156743285097459,
                -4.0197688025017744,
                2.6761438600430951,
                -2.0032892196425212,
                -2.2804413573951572,
                2.2670130563994615,
                0.84108173155190846,
                -1.9155801113404944,
                -0.67623130855912683,
                -0.75289716188152778,
                0.76821373730688336,
                0.13305374207253512,
                0.17235850797583452,
                -1.7305004045051249,
                1.3481449329298838,
                -4.657306021146284,
                -3.4744447396036797,
                5.0433156088683191,
                5.5486889870108023,
                4.5018999819433381,
            ]
        )

        b = np.zeros(20)
        xp1 = np.array([-1.0915786164735579, -0.25141395376511577])
        wrist_position = np.zeros(2)

        d = (joint_position_1 - -1.5149) * 0.648151148847911 - 1.0
        d1 = (joint_position_2 - -1.5106) * 0.649055624066983 - 1.0

        for k in range(20):
            b[k] = 2.0 / (np.exp(-2.0 * (a[k] + (b_a[k] * d + b_a[k + 20] * d1))) + 1.0) - 1.0

        for k in range(2):
            d = 0.0
            for i in range(20):
                d += c_a[k + (i << 1)] * b[i]
            wrist_position[k] = ((xp1[k] + d) - -1.0) / (-0.76393318623633011 * float(k) + 1.90985485103132) + (
                    -0.34906000000000004 * float(k) + -0.5236
            )

        return wrist_position[0], wrist_position[1]

    def forward(
            self,
            joint_position_up_deg,
            joint_position_lower_deg,
            joint_velocity_up_deg=0,
            joint_velocity_lower_deg=0,
            joint_torque_up=0,
            joint_torque_lower=0,
    ):
        # wrist position, retarget
        joint_position_l = np.deg2rad(-1 * joint_position_lower_deg)
        joint_position_r = np.deg2rad(joint_position_up_deg)
        joint_velocity_l = np.deg2rad(-1 * joint_velocity_lower_deg)
        joint_velocity_r = np.deg2rad(joint_velocity_up_deg)
        joint_torque_l = -1 * joint_torque_lower
        joint_torque_r = joint_torque_up
        wrist_position_pitch, wrist_position_roll = self.fk_nnfit(joint_position_l, joint_position_r)

        rotation_matrix = radian_to_rotation_matrix(wrist_position_pitch, wrist_position_roll)
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
        J_theta = np.array([[np.dot(s11, np.cross(r_bar1, r_rod1)), 0], [0, np.dot(s21, np.cross(r_bar2, r_rod2))]])

        # G_matrix
        G_matrix = np.array(
            [[0, 0, 0, np.cos(wrist_position_roll), 0, -np.sin(wrist_position_roll)], [0, 0, 0, 0, 1, 0]]
        ).T

        # wrist velocity
        joint_velocity = np.array([joint_velocity_l, joint_velocity_r])
        wrist_velocity_pitch, wrist_velocity_roll = np.linalg.inv(
            np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))
        ).dot(joint_velocity)

        # wrist torque
        joint_torque = np.array([joint_torque_l, joint_torque_r])
        wrist_torque_pitch, wrist_torque_roll = np.linalg.inv(
            np.linalg.inv(np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))).T
        ).dot(joint_torque)

        if self.isLeft:
            return (
                np.rad2deg(wrist_position_roll),
                np.rad2deg(-1 * wrist_position_pitch),
                np.rad2deg(wrist_velocity_roll),
                np.rad2deg(-1 * wrist_velocity_pitch),
                (wrist_torque_roll),
                (-1 * wrist_torque_pitch),
            )  # numpy.floa64
        else:
            return (
                np.rad2deg(-1 * wrist_position_roll),
                np.rad2deg(wrist_position_pitch),
                np.rad2deg(-1 * wrist_velocity_roll),
                np.rad2deg(wrist_velocity_pitch),
                (-1 * wrist_torque_roll),
                (wrist_torque_pitch),
            )  # numpy.floa64

    def inverse(
            self,
            wrist_position_roll_deg,
            wrist_position_pitch_deg,
            wrist_velocity_roll_deg=0,
            wrist_velocity_pitch_deg=0,
            wrist_torque_roll=0,
            wrist_torque_pitch=0,
    ):
        if self.isLeft:
            wrist_position_pitch = np.deg2rad(-1 * wrist_position_pitch_deg)
            wrist_position_roll = np.deg2rad(wrist_position_roll_deg)
            wrist_velocity_pitch = np.deg2rad(-1 * wrist_velocity_pitch_deg)
            wrist_velocity_roll = np.deg2rad(wrist_velocity_roll_deg)
            wrist_torque_pitch = -1 * wrist_torque_pitch
            wrist_torque_roll = wrist_torque_roll
        else:
            wrist_position_pitch = np.deg2rad(wrist_position_pitch_deg)
            wrist_position_roll = np.deg2rad(-1 * wrist_position_roll_deg)
            wrist_velocity_pitch = np.deg2rad(wrist_velocity_pitch_deg)
            wrist_velocity_roll = np.deg2rad(-1 * wrist_velocity_roll_deg)
            wrist_torque_pitch = wrist_torque_pitch
            wrist_torque_roll = -1 * wrist_torque_roll

        rotation_matrix = radian_to_rotation_matrix(wrist_position_pitch, wrist_position_roll)

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

        # motor position
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
        J_theta = np.array([[np.dot(s11, np.cross(r_bar1, r_rod1)), 0], [0, np.dot(s21, np.cross(r_bar2, r_rod2))]])

        # G_matrix
        G_matrix = np.array(
            [[0, 0, 0, np.cos(wrist_position_pitch), 0, -np.sin(wrist_position_pitch)], [0, 0, 0, 0, 1, 0]]
        ).T

        # motor velocity
        wrist_velocity = np.array([wrist_velocity_pitch, wrist_velocity_roll])
        joint_velocity_l, joint_velocity_r = np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix)).dot(wrist_velocity)

        # motor torque
        wrist_torque = np.array([wrist_torque_pitch, wrist_torque_roll])
        joint_torque_l, joint_torque_r = np.linalg.inv(np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))).T.dot(
            wrist_torque
        )

        return (
            np.rad2deg(joint_position_r),  # the upper motor
            np.rad2deg(-1 * joint_position_l),  # the lower motor
            np.rad2deg(joint_velocity_r),
            np.rad2deg(-1 * joint_velocity_l),
            (joint_torque_r),
            (-1 * joint_torque_l),
        )
