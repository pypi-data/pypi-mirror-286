from collections import deque

import os
import torch
import numpy

'''
The output pd target is the radian pd target for 23 joints of the robot. 
For the NN action output, we only control 21 joints, where ankle roll is not included.

The actor checkpoint is a jit file. You need to specify the path to the jit and load from it.
'''


class GR1ZXRLWalkControlModel:
    def __init__(self,
                 dt: float = 0.02,
                 decimation: int = 1,
                 actor_model_file_path=None, ):
        super().__init__()

        # --------------------------------------------------------------------
        # dt and decimation
        self.dt: float = dt
        self.decimation: int = int(decimation)
        self.decimation_count: int = 0
        self.global_timestep = 0

        # --------------------------------------------------------------------
        # real robot
        self.num_of_joints = 6 + 6 + 3 + 4 + 4

        self.index_of_joints_real_robot = numpy.array([
            0, 1, 2, 3, 4, 5,  # left leg
            6, 7, 8, 9, 10, 11,  # right leg
            12, 13, 14,  # waist
            18, 19, 20, 21,  # left arm
            25, 26, 27, 28,  # right arm
        ])
        self.pd_control_kp_real_robot = numpy.array([
            251.625, 362.5214, 200, 200, 10.9805, 10.9805,  # left leg
            251.625, 362.5214, 200, 200, 10.9805, 10.9805,  # right leg
            362.5214, 362.5214, 362.5214,  # waist
            92.85, 92.85, 112.06, 112.06,  # left arm
            92.85, 92.85, 112.06, 112.06,  # right arm
        ])
        self.pd_control_kd_real_robot = numpy.array([
            14.72, 10.0833, 11, 11, 0.5991, 0.5991,  # left leg
            14.72, 10.0833, 11, 11, 0.5991, 0.5991,  # right leg
            10.0833, 10.0833, 10.0833,  # waist
            2.575, 2.575, 3.1, 3.1,  # left arm
            2.575, 2.575, 3.1, 3.1,  # right arm
        ])

        # --------------------------------------------------------------------
        self.history_len = 10
        self.last_action = numpy.zeros(self.num_of_joints - 2)  # remove ankle roll (2)
        self.proprio_history_buf = deque(maxlen=self.history_len)

        # --------------------------------------------------------------------
        self.obs_scale_lin_vel = 0.5
        self.obs_scale_ang_vel = 0.25
        self.obs_scale_dof_pos = 1.0
        self.obs_scale_dof_vel = 0.05
        self.act_scale_action = 0.50
        self.act_clip_max = 10
        self.act_clip_min = -10

        # --------------------------------------------------------------------
        # actor
        self.actor_model_file_path: str | None = actor_model_file_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.actor = None

        self.index_of_joints_controlled = numpy.array([
            0, 1, 2, 3, 4,  # left leg (5)
            6, 7, 8, 9, 10,  # right leg (5)
            12, 13, 14,  # waist (3)
            15, 16, 17, 18,  # left arm (4)
            19, 20, 21, 22,  # right arm (4)
        ])
        self.joint_default_position = numpy.array([
            0.0, 0.0, -0.2618, 0.5236, -0.03, 0.0,  # left leg (6)
            0.0, 0.0, -0.2618, 0.5236, -0.03, 0.0,  # right leg (6)
            0.0, 0.0, 0.0,  # waist (3)
            0.0, 0.2, 0.0, -0.3,
            0.0, -0.2, 0.0, -0.3,
        ])

        # --------------------------------------------------------------------
        # output
        self.target_joint_position = numpy.zeros(self.num_of_joints)
        # --------------------------------------------------------------------

    def _load_actor(self):
        if self.actor is None:
            if self.actor_model_file_path is None:
                model_file_path = \
                    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "zx_rl_walk.pt")
            else:
                model_file_path = self.actor_model_file_path

            try:
                self.actor = torch.jit.load(model_file_path, map_location=self.device)
            except Exception as exp:
                print(f"Load actor model error: {exp}")
                self.actor = None

    def _get_phase(self):
        cycle_time = 0.64
        phase = self.global_timestep * self.dt / cycle_time
        return phase

    def run(self,
            joint_measured_position_urdf,  # dim=23
            joint_measured_velocity_urdf,  # dim=23
            init_output=None,
            commands=numpy.array([0, 0]),
            base_rpy=numpy.array([0, 0, 0]),
            base_ang_vel=numpy.array([0, 0, 0]),
            ):

        # load actor
        self._load_actor()

        # check decimation count
        if self.decimation_count % self.decimation == 0:
            # update decimation count
            self.decimation_count += 1
        else:
            # update decimation count
            self.decimation_count += 1

            target_joint_position = self.target_joint_position
            return target_joint_position

        # prepare input
        phase = self._get_phase()
        sin_pos = [numpy.sin(2 * numpy.pi * phase)]
        cos_pos = [numpy.cos(2 * numpy.pi * phase)]
        rp = base_rpy[:2]

        # actor obs
        obs_prop = numpy.concatenate([
            sin_pos,
            cos_pos,
            commands,
            base_ang_vel * self.obs_scale_ang_vel,
            rp,
            (joint_measured_position_urdf - self.joint_default_position) * self.obs_scale_dof_pos,
            joint_measured_velocity_urdf * self.obs_scale_dof_vel,
            self.last_action,
        ])

        obs_hist = numpy.array(self.proprio_history_buf).flatten()
        priv_latent = numpy.zeros(4 + 1 + 23 * 2)

        self.proprio_history_buf.append(obs_prop)

        obs_buf = numpy.concatenate([obs_prop, priv_latent, obs_hist])
        obs_tensor = torch.from_numpy(obs_buf).unsqueeze(0).float().to(self.device)

        # actor inference
        with torch.no_grad():
            raw_actions = self.actor(obs_tensor).numpy().squeeze()

        self.last_action = raw_actions.copy()

        # output
        raw_actions = numpy.clip(raw_actions, self.act_clip_min, self.act_clip_max)
        scaled_actions = raw_actions * self.act_scale_action

        step_actions = numpy.zeros(self.num_of_joints)
        step_actions[self.index_of_joints_controlled] = scaled_actions
        self.target_joint_position = self.joint_default_position + step_actions

        # update global timestep
        self.global_timestep += 1

        target_joint_position = self.target_joint_position
        return target_joint_position
