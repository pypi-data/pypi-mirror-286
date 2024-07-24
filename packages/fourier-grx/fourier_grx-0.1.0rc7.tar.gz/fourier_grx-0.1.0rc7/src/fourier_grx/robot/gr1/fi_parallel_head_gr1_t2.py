from math import asin, sqrt

import numpy as np


########### 注意 ###########
####### 统一单位为角度 #######
##### 电机顺序：先左后右 #####
## 姿态顺序：先pitch后roll ##
###########################


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


class ParallelHead:
    def __init__(self):
        # params and configuration
        self.initial_ra1 = np.array([0, 9.5, 44])
        self.initial_ra2 = np.array([0, -9.5, 44])
        self.initial_rb1 = np.array([-15, 9.5, 44])
        self.initial_rb2 = np.array([-15, -9.5, 44])
        self.initial_rc1 = np.array([-15, 9.5, 0])
        self.initial_rc2 = np.array([-15, -9.5, 0])
        self.length_bar1 = 15
        self.length_bar2 = 15
        self.length_rod1 = 44
        self.length_rod2 = 44
        self.initial_offset = 0.0

    def fk_nnfit(self, joint_position_1, joint_position_2):
        b_a = np.array(
            [
                1.8697050897768714,
                3.7864772428487563,
                -4.6492250336758127,
                1.6841323782857136,
                0.32740766363234114,
                -3.29072051411786,
                -1.7728576509294045,
                0.40682090837901969,
                1.1720697242428078,
                0.96643983361688146,
                -0.87395354276592641,
                1.1039102413786415,
                0.78279882868712858,
                0.19308504133869406,
                2.2284423212148852,
                -3.0570141899810821,
                -0.54222340371243272,
                3.6274770889455734,
                -1.7682554776870532,
                4.5397202573334416,
                3.8462945443182575,
                -4.1489378418383742,
                2.7179548265074991,
                4.5424983792375766,
                2.0575239402843324,
                1.3756057212538322,
                1.1562239181632421,
                -2.0201447828945107,
                0.0597003606513327,
                -1.7515510619660961,
                0.24568896228416973,
                -2.104749783480214,
                -0.086037955875044467,
                -2.0468006518287551,
                -1.7476021471922762,
                1.301115129863688,
                2.18323852282883,
                -2.2771542412715817,
                5.2366315269337207,
                -4.8762506354508135,
            ]
        )

        c_a = np.array(
            [
                0.11129238753250602,
                -0.0075582658405282587,
                1.1890827049253863,
                0.047606121377929474,
                -0.56600969534800338,
                -0.031249131358117015,
                0.016337736514226178,
                -0.0010633353049691614,
                0.29828021628742118,
                -0.030884569387188469,
                2.4949208252224579,
                0.2456333057839509,
                -0.74313329834907316,
                0.32230574282767349,
                1.1691037836118066,
                -0.20721752296911233,
                -0.93390300017787919,
                -0.22980821084451844,
                0.48947398215768129,
                -0.3498139044308114,
                0.25777639301294208,
                -1.5707178010685026,
                0.33021514231754179,
                -0.19204239494716857,
                3.0183169118181787,
                1.759138295620237,
                -0.78871527554834464,
                0.096351436074942148,
                1.6043267306959139,
                -1.0618208502491764,
                2.8241723827160929,
                0.97225551850086633,
                -0.75606948074435676,
                0.17170014769002712,
                0.15662916594429216,
                0.57777140411348182,
                0.280254852126239,
                -0.042303082075480357,
                0.3744316477411555,
                0.47492605898192036,
            ]
        )

        a = np.array(
            [
                -5.016900378781747,
                -4.859068343933318,
                4.08109798021488,
                -4.11173788330037,
                -1.5555944793197813,
                3.7712795722418289,
                1.3985617833923696,
                -1.3998745441760658,
                0.8499660909540242,
                -0.34831341594551085,
                0.90033157042193257,
                0.56626723249982558,
                0.685100639363494,
                -1.4437325397676997,
                2.6879886510162034,
                -3.6799380893547906,
                -1.5952987309441458,
                3.5743511319219232,
                5.1255980010435858,
                5.6338001100438682,
            ]
        )

        b = np.zeros(20)
        xp1 = np.array([-0.96645995634095694, 0.77778212009644032])
        neck_position = np.zeros(2)

        d = (joint_position_1 - -1.3516) * 0.753068755177348 - 1.0
        d1 = (joint_position_2 - -1.3523) * 0.752587017873942 - 1.0

        for k in range(20):
            b[k] = 2.0 / (np.exp(-2.0 * (a[k] + (b_a[k] * d + b_a[k + 20] * d1))) + 1.0) - 1.0

        for k in range(2):
            d = 0.0
            for i in range(20):
                d += c_a[k + (i << 1)] * b[i]
            neck_position[k] = ((xp1[k] + d) - -1.0) / (-0.76393318623633011 * float(k) + 1.90985485103132) + (
                    -0.34906000000000004 * float(k) + -0.5236
            )

        # (neck_position_roll, neck_position_pitch)
        return neck_position[0], neck_position[1]

    def forward(
            self,
            joint_position_l_deg,
            joint_position_r_deg,
            joint_velocity_l_deg=0,
            joint_velocity_r_deg=0,
            joint_torque_l=0,
            joint_torque_r=0,
    ):
        joint_position_l = np.deg2rad(joint_position_l_deg)
        joint_position_r = -np.deg2rad(joint_position_r_deg)
        joint_velocity_l = np.deg2rad(joint_velocity_l_deg)
        joint_velocity_r = -np.deg2rad(joint_velocity_r_deg)
        neck_position_roll, neck_position_pitch = self.fk_nnfit(joint_position_l, joint_position_r)

        rotation_matrix = radian_to_rotation_matrix(neck_position_roll, neck_position_pitch)
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
            [[0, 0, 0, np.cos(neck_position_pitch), 0, -np.sin(neck_position_pitch)], [0, 0, 0, 0, 1, 0]]
        ).T

        # neck velocity
        joint_velocity = np.array([joint_velocity_l, joint_velocity_r])
        neck_velocity_roll, neck_velocity_pitch = np.linalg.inv(
            np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))
        ).dot(joint_velocity)

        # neck torque
        joint_torque = np.array([joint_torque_l, joint_torque_r])
        neck_torque_roll, neck_torque_pitch = np.linalg.inv(
            np.linalg.inv(np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))).T
        ).dot(joint_torque)

        return (
            -np.rad2deg(neck_position_pitch),
            -np.rad2deg(neck_position_roll),
            np.rad2deg(neck_velocity_pitch),
            np.rad2deg(neck_velocity_roll),
            (neck_torque_pitch),
            (neck_torque_roll),
        )  # numpy.floa64

    def inverse(
            self,
            neck_position_pitch_deg,
            neck_position_roll_deg,
            neck_velocity_pitch_deg=0,
            neck_velocity_roll_deg=0,
            neck_torque_pitch=0,
            neck_torque_roll=0,
    ):
        neck_position_pitch = np.deg2rad(neck_position_pitch_deg)
        neck_position_roll = np.deg2rad(neck_position_roll_deg)
        neck_velocity_pitch = np.deg2rad(neck_velocity_pitch_deg)
        neck_velocity_roll = np.deg2rad(neck_velocity_roll_deg)

        rotation_matrix = radian_to_rotation_matrix(neck_position_roll, neck_position_pitch)

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
            [[0, 0, 0, np.cos(neck_position_pitch), 0, -np.sin(neck_position_pitch)], [0, 0, 0, 0, 1, 0]]
        ).T

        # motor velocity
        neck_velocity = np.array([neck_velocity_roll, neck_velocity_pitch])
        joint_velocity_l, joint_velocity_r = np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix)).dot(neck_velocity)

        # motor torque
        neck_torque = np.array([neck_torque_roll, neck_torque_pitch])
        joint_torque_l, joint_torque_r = np.linalg.inv(np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))).T.dot(
            neck_torque
        )

        return (
            -1 * np.rad2deg(joint_position_l),
            -1 * -np.rad2deg(joint_position_r),
            np.rad2deg(joint_velocity_l),
            -np.rad2deg(joint_velocity_r),
            (joint_torque_l),
            (joint_torque_r),
        )


if __name__ == "__main__":
    """
    Test Demo
    """
    myhead = ParallelHead()

    joint_l_pos_deg = 15
    joint_r_pos_deg = 15
    # joint_up_vel = 1.5
    # joint_lower_vel = 2.7
    # joint_up_torq = 3.9
    # joint_lower_torq = 4.4

    # forward
    neck_pitch_deg, neck_roll_deg, _, _, _, _ = myhead.forward(
        joint_l_pos_deg,
        joint_r_pos_deg,
        # joint_l_vel,
        # joint_r_vel,
        # joint_l_torq,
        # joint_r_torq,
    )
    print("output_neck_pitch: ", (neck_pitch_deg))
    print("output_neck_roll: ", (neck_roll_deg))
    # print(neck_roll_vel)
    # print(neck_pitch_vel)
    # print(neck_roll_torq)
    # print(neck_pitch_torq)

    # inverse
    joint_l_deg, joint_r_deg, _, _, _, _ = myhead.inverse(
        (neck_pitch_deg),
        (neck_roll_deg),
    )
    print("input_joint_l: ", (joint_l_deg))
    print("input_joint_r: ", (joint_r_deg))
    # print(joint_up_vel)
    # print(joint_lower_vel)
    # print(joint_up_torq)
    # print(joint_lower_torq)
