import logging
import time
from collections import deque, namedtuple
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any

import msgpack
import msgpack_numpy as m
import numpy as np
from rich.console import Console
from rich.table import Table

m.patch()

logger = logging.getLogger(__name__)

console = Console()

log = console.log
print = console.print


class ControlMode(IntEnum):
    NONE = 0
    PD = 9


class ControlGroup(tuple, Enum):
    ALL = (0, 32)
    LEFT_LEG = (0, 6)
    RIGHT_LEG = (6, 6)
    WAIST = (12, 3)
    HEAD = (15, 3)
    LEFT_ARM = (18, 7)
    RIGHT_ARM = (25, 7)
    LOWER = (0, 18)
    UPPER = (18, 14)
    UPPER_EXTENDED = (12, 20)

    @property
    def slice(self):
        return slice(self.value[0], self.value[0] + self.value[1])

    @property
    def num_joints(self):
        return self.value[1]


ControlCommand = namedtuple("ControlCommand", ["control_mode", "kp", "kd", "position"])


class Serde:
    @staticmethod
    def pack(data: Any) -> bytes:
        return msgpack.packb(data)  # type: ignore

    @staticmethod
    def unpack(data: bytes):
        return msgpack.unpackb(data)


class ServiceStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"


class JointIdx(IntEnum):
    """Joint indices for the robot."""

    L_LEG_1 = 0
    L_LEG_2 = 1
    L_LEG_3 = 2
    L_LEG_4 = 3
    L_LEG_5 = 4
    L_LEG_6 = 5
    R_LEG_1 = 6
    R_LEG_2 = 7
    R_LEG_3 = 8
    R_LEG_4 = 9
    R_LEG_5 = 10
    R_LEG_6 = 11
    WAIST_1 = 12
    WAIST_2 = 13
    WAIST_3 = 14
    HEAD_1 = 15
    HEAD_2 = 16
    HEAD_3 = 17
    L_ARM_1 = 18
    L_ARM_2 = 19
    L_ARM_3 = 20
    L_ARM_4 = 21
    L_ARM_5 = 22
    L_ARM_6 = 23
    L_ARM_7 = 24
    R_ARM_1 = 25
    R_ARM_2 = 26
    R_ARM_3 = 27
    R_ARM_4 = 28
    R_ARM_5 = 29
    R_ARM_6 = 30
    R_ARM_7 = 31
    # L_GRIPPER = 32
    # R_GRIPPER = 33


class JointControlMode(IntEnum):
    """Joint control modes for the robot."""

    POSITION = 4
    PD = 5


@dataclass
class JointParams:
    """Joint parameters for the robot."""

    name: str
    control_mode: JointControlMode
    kp: float
    kd: float
    position: float

    def to_dict(self):
        return {
            "control_mode": self.control_mode,
            "kp": self.kp,
            "kd": self.kd,
            "position": self.position,
        }


@dataclass
class Trajectory:
    start: np.ndarray
    end: np.ndarray
    duration: float

    def at(self, t: float):
        return self.start + (self.end - self.start) * t / self.duration

    def finished(self, t: float):
        return t >= self.duration





if __name__ == "__main__":
    import doctest

    doctest.testmod()
