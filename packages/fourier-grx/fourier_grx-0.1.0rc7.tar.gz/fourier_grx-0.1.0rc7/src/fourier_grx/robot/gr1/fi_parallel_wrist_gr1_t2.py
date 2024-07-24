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
        self.initial_ra1 = np.array([-6.25, 8.48, 43.55])
        self.initial_ra2 = np.array([-6.25, -8.48, 43.55])
        self.initial_rb1 = np.array([-21.25, 8.48, 43.55])
        self.initial_rb2 = np.array([-21.25, -8.48, 43.55])
        self.initial_rc1 = np.array([-15, 8.48, 0])
        self.initial_rc2 = np.array([-15, -8.48, 0])
        self.length_bar1 = 15
        self.length_bar2 = 15
        self.length_rod1 = 44
        self.length_rod2 = 44
        self.initial_offset = 0.0

    # left and right hand share the same network
    def fk_nnfit(self, joint_position_1, joint_position_2):
        b_a = np.array(
            [
                6.6083239733578063,
                3.9418421836336042,
                -2.4579755519699353,
                1.108162573868255,
                3.8232989517854667,
                -6.7010279006829805,
                -3.90939104979405,
                0.69440382071476536,
                1.6276165341395585,
                0.67750057218553084,
                -1.9481321139409409,
                1.7565907447102092,
                0.57599598816792164,
                -0.3539266261104293,
                5.066696053092949,
                -6.8948099505931779,
                0.50534444116741251,
                4.7400488079328378,
                3.943324176714444,
                6.2332242987377642,
                1.7003604679980404,
                -4.0980264896075074,
                1.4667077766627297,
                4.3700608579220335,
                3.5891351090271697,
                -1.8878010943161645,
                2.8729647120127413,
                -2.2280915130643884,
                -0.24784272086873907,
                -1.1763456931934448,
                0.81636793504759042,
                -2.3530192098391787,
                -0.20578007456941028,
                -1.3495477146604256,
                -5.7164767586646219,
                3.9792871409086432,
                4.2434848165130656,
                -2.8017036471973675,
                2.5819893825943931,
                -4.3577976051817124,
            ]
        )

        c_a = np.array(
            [
                -1.5169291265489147,
                -0.2082349479874758,
                0.63316058450527379,
                0.2996056386782382,
                2.2599078320743269,
                0.27704688274368583,
                -0.69222259288372689,
                0.0677073906142498,
                0.011450728354412288,
                0.0089055312102663126,
                -1.3925769602636826,
                -0.18558366388156874,
                -0.82758370434072914,
                -0.089692106043407951,
                0.3192792910197827,
                -0.11771969242248413,
                -1.3420886980883635,
                0.31838018203516122,
                0.64743426075914312,
                -0.956773006938416,
                -2.1859788152061275,
                0.14833878121282648,
                0.32104005128513557,
                -0.0865835932184397,
                2.3105491559235687,
                2.552543170508129,
                0.16665565805937393,
                -0.010145670768076966,
                0.10328504412153576,
                -0.042011374125897276,
                0.24139603871262802,
                -0.020468625284177838,
                1.0880402063222989,
                -0.15645607441918613,
                0.18452402484240943,
                -0.93886430218258821,
                -0.00057161499415276024,
                -0.00049109778979844856,
                0.63869928739219362,
                0.28794225569607923,
            ]
        )

        a = np.array(
            [
                -6.0818720398831614,
                -6.7711169389668449,
                2.04235120902932,
                -4.088439461456014,
                -4.0260407411298464,
                6.1912563758037011,
                2.8041200014844128,
                -1.5432379439829127,
                -1.0121103104932758,
                -0.045678138984986211,
                1.1674775717225221,
                1.0927203721987468,
                0.2065181283868481,
                -0.36479786388313684,
                3.5766998199950892,
                -5.2990973406978323,
                -3.9374320125379816,
                4.883815667566541,
                3.0918170278090544,
                5.3419825747853142,
            ]
        )

        b = np.zeros(20)
        xp1 = np.array([-0.70856474721809781, 0.31863289284106455])
        wrist_position = np.zeros(2)

        d = (joint_position_1 - -1.2795) * 0.701754385964912 - 1.0
        d1 = (joint_position_2 - -1.2795) * 0.701705143498702 - 1.0

        for k in range(20):
            b[k] = 2.0 / (np.exp(-2.0 * (a[k] + (b_a[k] * d + b_a[k + 20] * d1))) + 1.0) - 1.0

        for k in range(2):
            d = 0.0
            for i in range(20):
                d += c_a[k + (i << 1)] * b[i]
            wrist_position[k] = ((xp1[k] + d) - -1.0) / (-0.54567132576597 * float(k) + 1.63702291013563) + (
                -0.26178999999999997 * float(k) + -0.61087
            )

        # (wrist_position_roll, wrist_position_pitch)
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

        c1 = (self.length_rod1**2 - self.length_bar1**2 - norm_1**2) / (2 * self.length_bar1)
        c2 = (self.length_rod2**2 - self.length_bar2**2 - norm_2**2) / (2 * self.length_bar2)

        # motor position
        joint_position_l = asin(
            (b1 * c1 + sqrt(b1**2 * c1**2 - (a1**2 + b1**2) * (c1**2 - a1**2))) / (a1**2 + b1**2)
        ) - np.deg2rad(self.initial_offset)
        joint_position_r = asin(
            (b2 * c2 + sqrt(b2**2 * c2**2 - (a2**2 + b2**2) * (c2**2 - a2**2))) / (a2**2 + b2**2)
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
