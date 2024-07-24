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
            self.initial_ra1 = np.array([0, 27, 284])
            self.initial_ra2 = np.array([0, -27, 218])
            self.initial_rb1 = np.array([-50.22, 27, 297.48])
            self.initial_rb2 = np.array([-50.22, -27, 231.48])
            self.initial_rc1 = np.array([-50.22, 27, 13.48])
            self.initial_rc2 = np.array([-50.22, -27, 13.48])
            self.length_bar1 = 52
            self.length_bar2 = 52
            self.length_rod1 = 284
            self.length_rod2 = 218
            self.initial_offset = 15.022
        elif type == "right":
            self.isLeft = False
            self.initial_ra1 = np.array([0, 27, 218])
            self.initial_ra2 = np.array([0, -27, 284])
            self.initial_rb1 = np.array([-50.22, 27, 231.48])
            self.initial_rb2 = np.array([-50.22, -27, 297.48])
            self.initial_rc1 = np.array([-50.22, 27, 13.48])
            self.initial_rc2 = np.array([-50.22, -27, 13.48])
            self.length_bar1 = 52
            self.length_bar2 = 52
            self.length_rod1 = 218
            self.length_rod2 = 284
            self.initial_offset = 15.022

    def left_fk_nnfit(self, joint_position_l, joint_position_r):
        b_a = np.array(
            [
                0.72034981817963717,
                -2.513105268375365,
                -0.45478509274759116,
                -1.8832603434772739,
                1.1148547987689044,
                -5.2060262825835739,
                -1.3371830369502122,
                -3.685790326894089,
                1.393595285517113,
                1.7974554409016812,
                0.37729090464150017,
                0.36903883853529862,
                2.5128998893902583,
                -2.1744279980510095,
                -0.27951119084874859,
                -1.1562637659465282,
                1.3626684637780433,
                -5.0751432350285954,
                -0.61803013435987686,
                0.6974228121699837,
                2.3488995783654039,
                -1.8860475370015946,
                1.3974627960367467,
                2.7804077761335595,
                -0.34380484368905795,
                -0.8138823905050272,
                -0.432766497999279,
                -2.4009241709787834,
                0.13039397084901441,
                0.073788773125008839,
                0.44892081734187589,
                0.44360625827825589,
                1.0740408414420262,
                -0.66520045870372324,
                1.444778786484779,
                0.40288761449023408,
                -0.65989860658718924,
                4.7062241384866192,
                3.3718275656962806,
                1.7261380683219589,
            ]
        )

        c_a = np.array(
            [
                -0.14200689866418878,
                -0.055401089679771587,
                -0.10399880188934751,
                -0.04994701476265323,
                -1.7608239354654984,
                -0.93914764469658851,
                -0.61024383672098248,
                -0.624144702078267,
                1.2587441468049556,
                -0.33739288503852416,
                0.00195569721891914,
                0.00054011596165920526,
                -0.86337125514628088,
                -0.18276444178360873,
                -0.000978536142432207,
                -0.00046298462798891233,
                1.6108183724414076,
                -0.0066934941610140436,
                -0.41848179555266535,
                0.010481540563419352,
                -1.3095542833260314,
                1.3190919285464002,
                -3.3752826169002503,
                0.75057898682314472,
                -0.048674765271914472,
                0.0016886842561632488,
                -0.14929488285647768,
                0.0084354093410768,
                0.95089570762238329,
                0.65578052651423535,
                -3.5670595541688579,
                -0.42464769993128421,
                -0.84901355639641929,
                -0.68897952991865463,
                -1.0919427834991915,
                0.098174361279342,
                0.60801514384092614,
                -0.11951260751247149,
                -0.054736883415736882,
                0.15936327535931344,
            ]
        )

        a = np.array(
            [
                -3.4335544891248735,
                3.815006141388932,
                1.1483645728180982,
                3.6349103821785529,
                -1.6297665085008401,
                3.1464173689389794,
                1.2592489248308043,
                0.5640845786405706,
                -0.22210584821189769,
                -0.32560980948244117,
                0.41022589480994404,
                -0.63915907594498311,
                1.4094488304873742,
                -1.1779977673505233,
                1.1658536193760891,
                -1.2041140680485694,
                1.4413539194270863,
                -5.4349134651432136,
                -5.1226127873170242,
                2.6708663077350985,
            ]
        )

        b = np.zeros(20)
        xp1 = np.array([-0.77548711306897011, 0.72528784604706187])
        ankle_position = np.zeros(2)

        d = (joint_position_l - -1.08069160604814) * 1.12750777134478 - 1.0
        d1 = (joint_position_r - -1.08094745185491) * 1.12844974932796 - 1.0

        for k in range(20):
            b[k] = 2.0 / (np.exp(-2.0 * (a[k] + (b_a[k] * d + b_a[k + 20] * d1))) + 1.0) - 1.0

        for k in range(2):
            d = 0.0
            for i in range(20):
                d += c_a[k + (i << 1)] * b[i]
            ankle_position[k] = ((xp1[k] + d) - -1.0) / (-0.76394765751989024 * float(k) + 2.29183618246084) + (
                -0.436332512356777 * float(k) + -0.436332007666317
            )

        # (ankle_position_roll, ankle_position_pitch)
        return ankle_position[0], ankle_position[1]

    def right_fk_nnfit(self, joint_position_l, joint_position_r):
        b_a = np.array(
            [
                -5.6734392636099376,
                -1.6442488194411198,
                -5.8446038997673915,
                4.8131404315139417,
                -2.0725570710637187,
                3.1382567879494641,
                3.0778682773526187,
                -3.1723232665255017,
                1.3052847491313322,
                0.86629504031873972,
                -2.9009986505079879,
                1.0280231691897141,
                -2.3114832862675954,
                1.5995049441792348,
                1.9980729715620007,
                -4.2192472350950219,
                4.3493478596489652,
                -3.0279554025521942,
                0.81471709934295333,
                5.4603945525826907,
                1.7704256083685792,
                -5.1122694251640208,
                -1.9439388232645545,
                -3.5045270382586673,
                -4.9185015538358039,
                -3.910937140606757,
                -1.8401477128023636,
                -1.2764139417932165,
                -1.8603242289070929,
                -0.52189297681925928,
                -3.1639130073692585,
                -1.3986837083153527,
                -4.6137698697313327,
                -0.99262480996384206,
                -2.5287774278451058,
                4.75066446801609,
                -3.6419255137273971,
                0.03007827997809235,
                3.8591605724117191,
                -2.3068238136901957,
            ]
        )

        c_a = np.array(
            [
                0.13095558576524352,
                -0.00980278424339123,
                -0.013523645058363183,
                -0.0023562043372193403,
                -0.0028467194190393928,
                0.00025290521135056671,
                0.013187714371402199,
                0.048829839713351392,
                -0.0019553325641620246,
                -0.0011078994798509611,
                0.15741844343683037,
                -0.064483608133763623,
                -0.013536863806129049,
                0.039600535103752672,
                -0.0087712724443853949,
                0.00071001351310679252,
                0.65400218241545083,
                -0.41499262520144653,
                0.60548399742023329,
                2.1863628247098537,
                -0.00347405055687547,
                0.00085834260235789176,
                0.63970993265480536,
                -1.0740287218565634,
                -0.0027501714459721026,
                0.00035994884257957519,
                0.60222588171809366,
                0.47078779919141217,
                0.12665081622893806,
                -0.27683138625894405,
                -0.057903112373314893,
                0.13857451272091414,
                0.39960880224674233,
                0.5945453151832274,
                -0.12180064491386092,
                -0.015683940376599675,
                -0.043769235166464832,
                0.0015011843203987653,
                -0.564907105464816,
                -0.26498055618496286,
            ]
        )

        a = np.array(
            [
                6.2168559246284154,
                5.4965657614807268,
                3.7977221822922527,
                -3.7354754358864986,
                3.815530818520855,
                -2.940252572594674,
                -1.8205504939511306,
                1.074638873884421,
                -1.0552443577022075,
                -0.24932435129837802,
                -0.27926206124641278,
                0.0943623222454731,
                -1.9975887609505918,
                0.970261299438189,
                1.3126471537072235,
                -3.3379360122408976,
                4.1940805289110319,
                -3.355890683159779,
                4.3052213075687176,
                6.6472191721746743,
            ]
        )

        b = np.zeros(20)
        xp1 = np.array([0.11528270081877497, 0.060226567895293626])
        ankle_position = np.zeros(2)

        d = (joint_position_l - -1.08094152764617) * 1.12841689393192 - 1.0
        d1 = (joint_position_r - -1.08069752700211) * 1.12754056654678 - 1.0

        for k in range(20):
            b[k] = 2.0 / (np.exp(-2.0 * (a[k] + (b_a[k] * d + b_a[k + 20] * d1))) + 1.0) - 1.0

        for k in range(2):
            d = 0.0
            for i in range(20):
                d += c_a[k + (i << 1)] * b[i]
            ankle_position[k] = ((xp1[k] + d) - -1.0) / (-0.76394765751989024 * float(k) + 2.29183618246084) + (
                -0.436332512356777 * float(k) + -0.436332007666317
            )

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
        J_theta = np.array([[np.dot(s11, np.cross(r_bar1, r_rod1)), 0], [0, np.dot(s21, np.cross(r_bar2, r_rod2))]])

        # G_matrix
        G_matrix = np.array(
            [[0, 0, 0, np.cos(ankle_position_pitch), 0, -np.sin(ankle_position_pitch)], [0, 0, 0, 0, 1, 0]]
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

        c1 = (self.length_rod1**2 - self.length_bar1**2 - norm_1**2) / (2 * self.length_bar1)
        c2 = (self.length_rod2**2 - self.length_bar2**2 - norm_2**2) / (2 * self.length_bar2)

        # joint position
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
            [[0, 0, 0, np.cos(ankle_position_pitch), 0, -np.sin(ankle_position_pitch)], [0, 0, 0, 0, 1, 0]]
        ).T

        # joint velocity
        ankle_velocity = np.array([ankle_velocity_roll, ankle_velocity_pitch])
        joint_velocity_l, joint_velocity_r = np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix)).dot(ankle_velocity)

        # joint torque
        ankle_torque = np.array([ankle_torque_roll, ankle_torque_pitch])
        joint_torque_l, joint_torque_r = np.linalg.inv(np.dot(np.linalg.inv(J_theta), np.dot(Jx, G_matrix))).T.dot(
            ankle_torque
        )

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

        # testing demo


# left_ankle = ankle('left')
# ankle_position_roll, ankle_position_pitch, ankle_velocity_roll, ankle_velocity_pitch, ankle_torque_roll, ankle_torque_pitch = left_ankle.inverse(0.1, -0.4, 1.1, 0.3, 1.1, 0.3)

# right_ankle = ankle('right')
# joint_position_l, joint_position_r, joint_velocity_l, joint_velocity_r, joint_torque_l, joint_torque_r = right_ankle.inverse(0.1, -0.4, 1.1, 0.3, 1.1, 0.3)
