import json
from dataclasses import dataclass
import socket
from typing import TypeAlias


PORT_REQUEST = 4197
PORT_STATES = 4198


@dataclass(slots=True, frozen=True)
class StandCmd:
    # x: float
    # y: float
    # z: float
    # a: float
    # b: float
    # c: float

    def to_dict(self):
        return {
            "function": "SonnieCommand",
            "data": {
                "stand": {}
                # {
                #     "pos_cmd": {"body": {"x": self.x, "y": self.y, "z": self.z, "a": self.a, "b": self.b, "c": self.c}}
                # }
            },
        }

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass(slots=True, frozen=True)
class ZeroCmd:
    def to_dict(self):
        return {"function": "SonnieCommand", "data": {"zero": {}}}

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass(slots=True, frozen=True)
class WalkCmd:
    vx: float
    vy: float
    vc: float  # rad/s

    def to_dict(self):
        return {
            "function": "SonnieCommand",
            "data": {"walk": {"vel_cmd": {"vx": self.vx, "vy": self.vy, "vc": self.vc}}},
        }

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass(slots=True, frozen=True)
class StopCmd:
    def to_dict(self):
        return {"function": "SonnieCommand", "data": {"stop": {}}}

    def to_json(self):
        return json.dumps(self.to_dict())


SonnieCommand: TypeAlias = StandCmd | ZeroCmd | WalkCmd | StopCmd


class SonnieControl:
    def __init__(self, server_ip: str = "localhost"):
        self.sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock_states = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock_cmd.connect((server_ip, PORT_REQUEST))
        # self.sock_states.connect((server_ip, PORT_STATES))

    def _send(self, cmd: SonnieCommand):
        self.sock_cmd.send(cmd.to_json().encode())

    def zero(self):
        self._send(ZeroCmd())

    def stand(self):
        self._send(StandCmd())

    def walk(self, vx: float, vy: float, vc: float):
        self._send(WalkCmd(vx, vy, vc))

    def stop(self):
        self._send(StopCmd())

    # def recv(self):
    #     try:
    #         res = json.loads(self.sock_states.recv(1024))
    #     except Exception as e:
    #         print(e)
    #         return None
