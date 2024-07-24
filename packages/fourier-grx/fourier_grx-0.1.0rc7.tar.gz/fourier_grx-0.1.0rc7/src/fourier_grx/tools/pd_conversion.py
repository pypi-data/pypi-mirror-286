import fourier_core.tools.pd_conversion as pd_conversion
from fourier_core.tools.pd_conversion import ActuatorFSAType


def GR1T1_pd_dict() -> dict:
    pd_dict = {
        "l_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 251.625, 14.72],
        "l_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "l_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "l_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "l_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.599],
        "l_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.599],
        "r_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 251.625, 14.72],
        "r_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "r_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "r_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "r_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.599],
        "r_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.599],
        "waist_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_pitch": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_roll": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "head_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "head_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "head_roll": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "l_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "l_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
    }

    return pd_dict


def GR1T1V2_pd_dict() -> dict:
    pd_dict = {
        "l_hip_roll": [ActuatorFSAType.FSA_TYPE_802029, 251.625, 14.72],
        "l_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "l_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "l_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "l_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "l_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "r_hip_roll": [ActuatorFSAType.FSA_TYPE_802029, 251.625, 14.72],
        "r_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "r_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "r_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "r_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "r_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "waist_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_pitch": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_roll": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "l_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "l_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
    }

    return pd_dict


def GR1T1V3_pd_dict() -> dict:
    pd_dict = {
        "l_hip_roll": [ActuatorFSAType.FSA_TYPE_802029, 251.625, 14.72],
        "l_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "l_hip_pitch": [ActuatorFSAType.FSA_TYPE_13014E, 200, 11],
        "l_knee_pitch": [ActuatorFSAType.FSA_TYPE_13014E, 200, 11],
        "l_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "l_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "r_hip_roll": [ActuatorFSAType.FSA_TYPE_802029, 251.625, 14.72],
        "r_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "r_hip_pitch": [ActuatorFSAType.FSA_TYPE_13014E, 200, 11],
        "r_knee_pitch": [ActuatorFSAType.FSA_TYPE_13014E, 200, 11],
        "r_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "r_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.6],
        "waist_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_pitch": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_roll": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "l_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "l_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
    }

    return pd_dict


def GR1T2_pd_dict() -> dict:
    pd_dict = {
        "l_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 251.625, 14.72],
        "l_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "l_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "l_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "l_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.5991],
        "l_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.5991],
        "r_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 251.625, 14.72],
        "r_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "r_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "r_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 200, 11],
        "r_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.5991],
        "r_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 10.98, 0.5991],
        "waist_yaw": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_pitch": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "waist_roll": [ActuatorFSAType.FSA_TYPE_601750, 362.52, 10.0833],
        "head_roll": [ActuatorFSAType.FSA_TYPE_250830, 10, 1],
        "head_pitch": [ActuatorFSAType.FSA_TYPE_250830, 10, 1],
        "head_yaw": [ActuatorFSAType.FSA_TYPE_250830, 10, 1],
        "l_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "l_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "l_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "l_wrist_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 10, 1],
        "l_wrist_roll": [ActuatorFSAType.FSA_TYPE_250830, 10, 1],
        "l_wrist_pitch": [ActuatorFSAType.FSA_TYPE_250830, 10, 1],
        "r_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 92.85, 2.575],
        "r_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 112.06, 3.1],
        "r_wrist_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 10, 1],
        "r_wrist_roll": [ActuatorFSAType.FSA_TYPE_250830, 10, 1],
        "r_wrist_pitch": [ActuatorFSAType.FSA_TYPE_250830, 10, 1],
    }

    return pd_dict


def GR1T1_low_stiffness_pd_dict() -> dict:
    pd_dict = {
        "l_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 40, 40 / 10 * 1.0],
        "l_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 1.0],
        "l_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 1.0],
        "l_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 1.0],
        "l_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 1.0],
        "l_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 1.0],
        "r_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 40, 40 / 10 * 1.0],
        "r_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 1.0],
        "r_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 1.0],
        "r_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 1.0],
        "r_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 1.0],
        "r_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 1.0],
        "waist_yaw": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 1.0],
        "waist_pitch": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 1.0],
        "waist_roll": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 1.0],
        "l_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 1.0],
        "l_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 1.0],
        "l_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 1.0],
        "l_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 1.0],
        "r_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 1.0],
        "r_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 1.0],
        "r_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 1.0],
        "r_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 1.0],
    }

    return pd_dict


def GR1T1_dic_pd_dict() -> dict:
    pd_dict = {
        "l_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 40, 40 / 10 * 2.5],
        "l_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 7.5],
        "l_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 2.5],
        "l_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 2.5],
        "l_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 2.5],
        "l_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 2.5],
        "r_hip_roll": [ActuatorFSAType.FSA_TYPE_802030, 40, 40 / 10 * 2.5],
        "r_hip_yaw": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 7.5],
        "r_hip_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 2.5],
        "r_knee_pitch": [ActuatorFSAType.FSA_TYPE_1307E, 130, 130 / 10 * 2.5],
        "r_ankle_pitch": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 2.5],
        "r_ankle_roll": [ActuatorFSAType.FSA_TYPE_36B36E, 18, 18 / 10 * 2.5],
        "waist_yaw": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 7.5],
        "waist_pitch": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 7.5],
        "waist_roll": [ActuatorFSAType.FSA_TYPE_601750, 45, 45 / 10 * 7.5],
        "l_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 7.5],
        "l_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 7.5],
        "l_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 7.5],
        "l_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 7.5],
        "r_shoulder_pitch": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 7.5],
        "r_shoulder_roll": [ActuatorFSAType.FSA_TYPE_361480, 30, 30 / 10 * 7.5],
        "r_shoulder_yaw": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 7.5],
        "r_elbow_pitch": [ActuatorFSAType.FSA_TYPE_3611100, 30, 30 / 10 * 7.5],
    }

    return pd_dict


def print_pd_converted():
    pid_dict_converted = pd_conversion.pd_conversion_dict(GR1T2_pd_dict())

    for key, value in pid_dict_converted.items():
        print(key, value)


if __name__ == "__main__":
    print_pd_converted()
