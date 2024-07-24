# Copyright 2024 Fourier Intelligence
# Author: Yuxiang Gao <yuxiang.gao@fftai.com>
from __future__ import annotations

import json
import struct
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from typing import Literal, TypeAlias

RequestMethodType: TypeAlias = Literal["GET", "SET"]


def pascal_to_snake(name: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def is_pascal_case(name: str) -> bool:
    return name[0].isupper() and name[1].islower() and "_" not in name


def is_snake_case(name: str) -> bool:
    return name.islower() and "_" in name


class FourierActuatorUDPPort(IntEnum):
    """Fourier UDP ports"""

    COMM = 2333
    CTRL = 2334
    FAST = 2335


class FourierEncoderUDPPort(IntEnum):
    """Fourier UDP ports"""

    COMM = 2334
    CTRL = 2333
    FAST = 2335


FourierUDPPort: TypeAlias = FourierEncoderUDPPort | FourierActuatorUDPPort


class FourierServerStatus(StrEnum):
    CONNECTED = "CONNECTED"
    # ACTIVATED = "ACTIVATED"
    # UNKNOWN = "UNKNOWN"
    ERROR = "ERROR"

    @classmethod
    def from_str(cls, name: str) -> FourierServerStatus:
        try:
            return cls[name.upper()]
        except KeyError as exc:
            raise KeyError(f"Invalid status {name}") from exc


class FourierServerType(StrEnum):
    ACTUATOR = "actuator"
    ABS_ENCODER = "abs_encoder"
    CTRL_BOX = "ctrl_box"

    @classmethod
    def from_str(cls, name: str) -> FourierServerType:
        if is_pascal_case(name):
            name = pascal_to_snake(name)
        try:
            return cls[name.upper()]
        except KeyError as exc:
            raise KeyError(f"Invalid server type {name}") from exc


@dataclass
class FourierServer:
    ip: str
    type: FourierServerType
    status: FourierServerStatus

    # TODO: these fields maybe generalized
    activated = False
    enabled = False
    name = ""

    @property
    def id(self) -> int:
        return int(self.ip.split(".")[-1])

    def __lt__(self, other: FourierServer) -> bool:
        return self.id < other.id

    def __eq__(self, other) -> bool:
        return self.id == other.id and self.type == other.type

    @classmethod
    def from_dict(cls, data: dict) -> FourierServer:
        try:
            return cls(
                ip=data["ip"],
                type=FourierServerType.from_str(data["type"]),
                status=FourierServerStatus.from_str(data["status"]),
            )
        except KeyError as exc:
            raise KeyError(f"Missing required key in data: {data}") from exc

    @classmethod
    def new(cls, ip: str, type_: str, status: str) -> FourierServer:
        try:
            return cls(
                ip=ip,
                type=FourierServerType.from_str(type_),
                status=FourierServerStatus.from_str(status),
            )
        except ValueError as exc:
            raise ValueError(f"Invalid server type {type_} or status {status}") from exc


@dataclass(slots=True, frozen=True)
class FIProtocol:
    """Helper class for building requests to FSA servers

    Args:
        method (RequestMethodType): GET or SET
        path (str): request target path. This key will be renamed to `reqTarget` during serialization.
        prop (str | None): Optional prop arg. This key will be renamed to `property` during serialization. Maybe move this to data because limited usage
        data (dict | None): Additional data for the request. During serialization, the content will be attached to the parent object.
    """

    method: RequestMethodType
    path: str = field(default_factory=str)
    prop: str = field(default_factory=str)
    data: dict = field(default_factory=dict)

    def serialize_model(self):
        res = {"method": self.method, "reqTarget": self.path, "property": ""}
        # if self.prop is not None:
        #     res["property"] = self.prop
        if self.data is not None:
            res.update(self.data)
        return res

    def encode(self):
        return json.dumps(self.serialize_model()).encode()


class FIFastIdentifier(IntEnum):
    # WATCHDOG = 0xFF
    ENABLE = 0x01
    DISABLE = 0x02
    CLEAR_FAULT = 0x03
    MODE_POSITION = 0x04
    MODE_VELOCITY = 0x05
    MODE_TORQUE = 0x06
    MODE_CURRENT = 0x07
    MODE_PD = 0x09
    SET_POSITION = 0x0A  # ">Bfff"
    SET_VELOCITY = 0x0B  # ">Bff"
    SET_TORQUE = 0x0C  # ">Bf"
    SET_CURRENT = 0x0D  # ">Bf"
    SET_PD = 0x0E  # ">Bf"
    GET_PVC = 0x1A  # ">Bfff"
    # GET_PVCT = 0x1D  # ">Bffff"
    GET_ERROR = 0x1B  # ">Bi"


@dataclass(slots=True, frozen=True)
class FIFastProtocol:
    ident: FIFastIdentifier
    payload: list[int | float] = field(default_factory=list)
    timestamp: float | None = None

    def encode(self):
        format_ = ">B"
        for i in self.payload:
            if isinstance(i, int):
                format_ += "i"
            elif isinstance(i, float):
                format_ += "f"
            else:
                raise ValueError(f"Invalid type {type(i)} for payload")
        return struct.pack(format_, self.ident, *self.payload)

    @classmethod
    def from_bytes(cls, data: bytes, ts: float | None = None) -> FIFastProtocol:
        try:
            ident = FIFastIdentifier(data[0])
        except ValueError as err:
            raise ValueError(f"Invalid identifier {data[0]} for payload") from err

        format_ = ">B"
        if ident == FIFastIdentifier.GET_PVC:
            format_ += "fff"
        # elif ident == FIFastIdentifier.GET_PVCT:
        #     format_ += "ffff"
        elif ident == FIFastIdentifier.GET_ERROR:
            format_ += "i"
        else:
            raise ValueError(f"Invalid identifier {ident} for payload")

        payload = struct.unpack(format_, data[: 1 + (len(format_) - 2) * 4])
        # for i in payload:
        #     if not isinstance(i, int | float):
        #         raise ValueError(f"Invalid type {type(i)} for payload")
        return cls(ident=ident, payload=list(payload[1:]), timestamp=ts)
