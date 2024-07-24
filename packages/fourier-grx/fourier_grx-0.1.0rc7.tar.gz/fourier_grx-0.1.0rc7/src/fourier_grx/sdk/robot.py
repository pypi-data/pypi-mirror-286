# Copyright 2024 Fourier Intelligence
# Author: Yuxiang Gao <yuxiang.gao@fftai.com>

from __future__ import annotations

import os
from typing import TypeAlias

import numpy as np
import pink
import pinocchio as pin
from loguru import logger

PinocchioJoint: TypeAlias = (
    pin.JointModelRX
    | pin.JointModelRY
    | pin.JointModelRZ
    | pin.JointModelPX
    | pin.JointModelPY
    | pin.JointModelPZ
    | pin.JointModelFreeFlyer
    | pin.JointModelSpherical
    | pin.JointModelSphericalZYX
    | pin.JointModelPlanar
    | pin.JointModelTranslation
)


class Robot:
    def __init__(self, robot_name: str, urdf_path: str, joints_to_lock: list[str] | None = None, visualize=False):
        """Robot wrapper.

        Args:
            robot_name (str): Name of the robot.
            urdf_path (str): Path to the URDF folder.
            joints_to_lock (list[str] | None, optional): List of joints to lock during inverse kinematics. Defaults to None.
            visualize (bool, optional): Open visualizer. Defaults to False.
        """
        self.robot_name = robot_name
        self.robot = pin.RobotWrapper.BuildFromURDF(
            filename=urdf_path,
            package_dirs=os.path.dirname(urdf_path),
            root_joint=pin.JointModelFreeFlyer(),
        )

        if joints_to_lock:
            self.robot = self.robot.buildReducedRobot(joints_to_lock)

        self.configuration = pink.Configuration(self.robot.model, self.robot.data, self.robot.q0, copy_data=False)

        logger.info(f"Initiated robot {robot_name} with {len(self.dof_joint_names)} joints: {self.dof_joint_names}")

        assert self.robot.nq == 32 + 7, "nq mismatch."
        self.viz = None
        if visualize:
            self.viz = pin.visualize.MeshcatVisualizer(
                self.robot.model, self.robot.collision_model, self.robot.visual_model
            )
            self.robot.setVisualizer(self.viz, init=False)
            self.viz.initViewer(open=False)
            self.viz.loadViewerModel()
            self.viz.displayFrames(True, range(len(self.robot.model.frames)))

    # def _update_frames(self, q):
    #     # https://github.com/stack-of-tasks/pinocchio/issues/802
    #     self.robot.frameForwardKinematics(q)

    @property
    def model(self) -> pin.Model:
        return self.robot.model

    @property
    def data(self) -> pin.Data:
        return self.robot.data

    @property
    def joint_names(self) -> list[str]:
        return list(self.robot.model.names)

    @property
    def dof_joint_names(self) -> list[str]:
        """Get the names of the joints with 1 degrees of freedom."""
        nqs = self.model.nqs
        return [name for i, name in enumerate(self.model.names) if nqs[i] == 1]

    @property
    def link_names(self) -> list[str]:
        return [f.name for f in self.robot.model.frames]

    @property
    def frame_names(self) -> list[str]:
        return self.link_names

    @property
    def joint_limits(self):
        lower = self.model.lowerPositionLimit
        upper = self.model.upperPositionLimit
        return np.stack([lower, upper], axis=1)

    def _convert_qpos(self, qpos: np.ndarray, clip=True):
        # append zeros for the freeflyer
        qpos = np.hstack((np.zeros(7), qpos))
        if clip:
            qpos = np.clip(qpos, self.joint_limits[:, 0], self.joint_limits[:, 1])
        return qpos

    def get_dof_joint_index(self, name: str):
        """Get the index of a joint in the dof_joint_names list."""
        return self.dof_joint_names.index(name)

    def get_link_index(self, name: str):
        if name not in self.link_names:
            raise ValueError(f"{name} is not a link name. Valid link names: \n{self.link_names}")
        return self.model.getFrameId(name)

    def get_idx_q(self, joint_name: str):
        idx = self.robot.model.getJointId(joint_name)
        return self.robot.model.idx_qs[idx]

    def set_joint(self, joint_name: str, q_1d: float):
        idx = self.get_idx_q(joint_name)
        q_new = self.configuration.q.copy()
        q_new[idx] = q_1d
        self.configuration.update(q_new)

    def set_joints(self, joint_names: list[str], q: np.ndarray):
        q_new = self.configuration.q.copy()
        for j, qj in zip(joint_names, q, strict=True):
            idx = self.get_idx_q(j)
            q_new[idx] = qj
        self.configuration.update(q_new)

    def set_joints_from_dict(self, joint_dict: dict[str, float]):
        q_new = self.configuration.q.copy()
        for j, qj in joint_dict.items():
            idx = self.get_idx_q(j)
            q_new[idx] = qj
        self.configuration.update(q_new)

    @property
    def q(self):
        return self.configuration.q[7:].copy()

    @q.setter
    def q(self, q: np.ndarray):
        self.configuration.update(np.hstack((np.zeros(7), q)))

    @property
    def q_dict(self):
        return dict(zip(self.joint_names, self.q, strict=True))

    @q_dict.setter
    def q_dict(self, q_dict: dict):
        self.set_joints(q_dict.keys(), q_dict.values())

    def add_frame(self, name: str, parent: str, transform: np.ndarray):
        """Add a frame to the robot.

        Args:
            name (str): Name of the frame.
            parent (str): Name of the parent frame.
            transform (NDArray): Transform of the frame with respect to the parent frame. Shape: (4, 4)
        """
        parent_id = self.robot.model.getFrameId(parent)
        parent_joint_id = self.robot.model.frames[parent_id].parent
        frame_id = self.robot.model.addFrame(
            pin.Frame(name, parent_joint_id, parent_id, pin.SE3(transform), pin.FrameType.OP_FRAME)
        )
        self.robot.rebuildData()

    def get_transform(self, to_frame: str, from_frame: str, q: np.ndarray | None = None):
        """Get the pose of a frame with respect to another frame.

        Args:
            to_frame: Name of the frame to get the pose of.
            from_frame: Name of the frame to get the pose in.

        Returns:
            Current transform from the source frame to the dest frame.

        Raises:
            KeyError: if any of the frame names is not found in the model.
        """
        if from_frame not in self.frame_names:
            raise KeyError(f"Frame {from_frame} not found in the robot.")
        if to_frame not in self.frame_names:
            raise KeyError(f"Frame {to_frame} not found in the robot.")

        if q is None:
            transform = self.configuration.get_transform(to_frame, from_frame).homogeneous
            return transform
        else:
            q = self._convert_qpos(q)
            pin.forwardKinematics(self.model, self.data, q)

            source_id = self.get_link_index(to_frame)
            dest_id = self.get_link_index(from_frame)

            transform_source_to_world: pin.SE3 = pin.updateFramePlacement(self.robot.model, self.robot.data, source_id)
            transform_dest_to_world: pin.SE3 = pin.updateFramePlacement(self.robot.model, self.robot.data, dest_id)
            return transform_dest_to_world.actInv(transform_source_to_world).homogeneous

    def update(self):
        if self.viz:
            # for frame_name in self.frame_names:
            #     meshcat_shapes.frame(self.viz.viewer[frame_name], opacity=0.5)
            #     self.viz.viewer[frame_name].set_transform(
            #         self.configuration.get_transform_frame_to_world(frame_name).np
            #     )
            # for frame in self.robot.model.frames:
            #     robot_frame_viz(self.viz.viewer, self.configuration, frame, name=self.robot_name)
            # print(self.robot.state.q)
            self.viz.display(self.configuration.q)

    # -------------------------------------------------------------------------- #

    # Kinematics function
    # -------------------------------------------------------------------------- #
    def compute_forward_kinematics(self, qpos: np.ndarray):
        qpos = self._convert_qpos(qpos)
        pin.forwardKinematics(self.model, self.data, qpos)

    def get_link_pose(self, link_id: int) -> np.ndarray:
        pose: pin.SE3 = pin.updateFramePlacement(self.model, self.data, link_id)
        return pose.homogeneous

    def get_link_pose_inv(self, link_id: int) -> np.ndarray:
        pose: pin.SE3 = pin.updateFramePlacement(self.model, self.data, link_id)
        return pose.inverse().homogeneous

    def compute_single_link_local_jacobian(self, qpos, link_id: int) -> np.ndarray:
        J = pin.computeFrameJacobian(self.model, self.data, qpos, link_id)
        return J
