# Copyright 2024 Fourier Intelligence
# Author: Yuxiang Gao <yuxiang.gao@fftai.com>

import json
import socket
import threading
import time
from collections import defaultdict
from enum import Enum, IntEnum

import zenoh
from loguru import logger

from .exceptions import FourierBaseException
from .fourier_intelligence import (
    FIFastIdentifier,
    FIFastProtocol,
    FIUDPClient,
    FourierServer,
    FourierServerType,
    UDPDiscoverFailedException,
    discover_servers,
)
from .fourier_intelligence.common import (
    FIProtocol,
    FourierActuatorUDPPort,
    FourierEncoderUDPPort,
)
from .utils import Serde, ServiceStatus
from .zenoh import ZenohSession


class HWILifecycleState(IntEnum):
    """Lifecycle state of a hardware component."""

    UNKNOWN = 0
    UNINITIALIZED = 1
    INACTIVE = 2
    ACTIVE = 3
    FINALIZED = 4


class HWITypeValue(str, Enum):
    """Hardware interface type value."""

    POSITION = "position"
    VELOCITY = "velocity"
    ACCELERATION = "acceleration"
    EFFORT = "effort"
    FORCE = "force"
    TORQUE = "torque"
    CURRENT = "current"
    TEMPERATURE = "temperature"

    # gains
    GAIN_PROPORTIONAL = "gain_proportional"
    GAIN_INTEGRAL = "gain_integral"
    GAIN_DERIVATIVE = "gain_derivative"
    GAIN_FEEDFORWARD = "gain_feedforward"


zenoh.init_logger()


def devices_from_client(client: FIUDPClient, ip_dict: dict[str, str]):
    """Generate hardware devices from a Fourier Intelligence UDP client.

    Args:
        client (FIUDPClient): Fourier Intelligence UDP client.
        ip_dict (dict[str, str]): Dictionary of IP addresses and names.
    """
    if not client.discovered_servers:
        client.discover()
    servers = client.discovered_servers
    for ip, server in servers.items():
        if ip not in ip_dict:
            continue
        match server.type:
            case FourierServerType.ACTUATOR:
                yield FIActuator(ip_dict[ip], ip, client)
            case FourierServerType.ABS_ENCODER:
                yield FIEncoder(ip_dict[ip], ip, client)
            case _:
                pass


class FIServer:
    def __init__(self, name: str, type_: FourierServerType, ip: str, client: FIUDPClient):
        self.name = name
        self.type = type_
        self.state = HWILifecycleState.UNKNOWN
        self.server: FourierServer | None = None
        self.ip = ip
        self._client = client

    def __str__(self) -> str:
        return f"<[{self.type}] {self.name}@{self.ip} {self.state.name}>"

    def __repr__(self) -> str:
        return str(self)

    def on_init(self):
        if not self._client.running:
            self._client.start()
        self._client.activate([(self.name, self.ip)])
        self.server = self._client.discovered_servers[self.ip]

        if self.server is None:
            raise FourierBaseException("Server not initialized.")

        if self.server.type != self.type:
            raise FourierBaseException(f"Server type mismatch: {self.server.type} != {self.type}")

        self.state = HWILifecycleState.ACTIVE

    @property
    def udp_fast_addr(self):
        if self.server is None:
            raise FourierBaseException("Server not initialized.")
        if self.type == FourierServerType.ACTUATOR:
            port = FourierActuatorUDPPort.FAST
        elif self.type == FourierServerType.ABS_ENCODER:
            port = FourierEncoderUDPPort.FAST
        else:
            raise FourierBaseException("Unknown server type.")
        return (self.server.ip, port)

    @property
    def udp_addr(self):
        if self.server is None:
            raise FourierBaseException("Server not initialized.")
        if self.type == FourierServerType.ACTUATOR:
            port = FourierActuatorUDPPort.CTRL
        elif self.type == FourierServerType.ABS_ENCODER:
            port = FourierEncoderUDPPort.CTRL
        else:
            raise FourierBaseException("Unknown server type.")
        return (self.server.ip, port)

    def get_root(self):
        if self.server is None:
            raise FourierBaseException("Server not initialized.")
        if not self._client.running:
            raise FourierBaseException("Client not running.")
        res = self._client.get_root(self.udp_addr)
        return res


class FIActuator(FIServer):
    def __init__(self, name: str, ip: str, client: FIUDPClient):
        super().__init__(name, FourierServerType.ACTUATOR, ip, client)
        self.state_interface = [
            HWITypeValue.POSITION,
            HWITypeValue.VELOCITY,
            HWITypeValue.EFFORT,
        ]
        self.command_interafce = [
            HWITypeValue.POSITION,
        ]

    def on_init(self):
        super().on_init()

    def read(self):
        data = FIFastProtocol(ident=FIFastIdentifier.GET_PVC)
        self._client.send(data.encode(), self.udp_fast_addr)
        res, ts = self._client.get_nowait(self.udp_fast_addr)
        if res is None:
            return None
        res = FIFastProtocol.from_bytes(res, ts)

        if isinstance(res.timestamp, float):
            logger.trace(f"Recv latency: {time.time() - res.timestamp}")

        if res:
            assert len(res.payload) == len(self.state_interface), "Data length mismatch."
        return res.payload

    def reboot(self):
        data = FIProtocol(method="SET", path="/reboot")
        self._client.send(data.encode(), self.udp_addr)
        res, ts = self._client.get(self.udp_addr)
        if res is None:
            return None

        logger.debug(f"reboot res: {res}")
        res = json.loads(res.decode())
        if res["status"] != "OK":
            return None
        # self.on_init()
        return True

    def write(self, data):
        if not self._client.running:
            raise FourierBaseException("Client not running.")
        data = FIFastProtocol(ident=FIFastIdentifier.SET_POSITION, payload=data)
        self._client.send(data.encode(), self.udp_fast_addr)


class FIEncoder(FIServer):
    def __init__(self, name: str, ip: str, client: FIUDPClient):
        super().__init__(name, FourierServerType.ABS_ENCODER, ip, client)
        self.state_interface = [
            HWITypeValue.POSITION,
        ]
        self.command_interafce = []

    def on_init(self):
        super().on_init()

    def read(self):
        data = FIProtocol(method="GET", path="/measured")
        self._client.send(data.encode(), self.udp_addr)
        res, ts = self._client.get_nowait(self.udp_addr)
        if res is None:
            return None
        res = json.loads(res.decode())
        if res["status"] != "OK":
            return None

        return [res.get("radian", None)]

    def write(self, data):
        raise FourierBaseException("Encoder does not support write operation.")


class MotorStatus(str, Enum):
    UNKNOWN = "unknown"
    DISABLED = "disabled"
    ENABLED = "enabled"


class MotorServer(ZenohSession):
    """Simple motor server that exposes motor control services."""

    def __init__(self):
        super().__init__("gr")
        self.discovered_servers: dict[str, FourierServer] = {}
        self.motor_id_prefix = "192.168.137."

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(1 / 30)
        self._sock.bind(("", 0))

        self.readings: defaultdict[str, list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])

        self.status: defaultdict[str, MotorStatus] = defaultdict(lambda: MotorStatus.UNKNOWN)

        services = [
            "info",
            "enable",
            "disable",
            # "set_home",
            "reboot",
            "position",
            "velocity",
            "torque",
        ]
        self._services = {
            service: self.session.declare_queryable(f"{self.prefix}/motor/{service}/*", self._service_callback)
            for service in services
        }

        # start a thread to update motor readings
        self._running = False
        self._thread = threading.Thread(target=self._update_readings, daemon=True)

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def _update_readings(self):
        while self._running:
            for motor in self.discovered_servers:
                self._sock.sendto(
                    FIFastProtocol(FIFastIdentifier.GET_PVC).encode(),
                    (motor, FourierActuatorUDPPort.FAST),
                )
                try:
                    data, _ = self._sock.recvfrom(1024)
                    decoded_data = FIFastProtocol.from_bytes(data)
                    self.readings[motor] = decoded_data.payload
                except Exception:
                    logger.error(f"Failed to read motor {motor}.")
            time.sleep(1 / 120)

    def discover(self):
        """Broadcast to discover servers on the network."""
        try:
            self.discovered_servers = {s.ip: s for s in discover_servers(timeout=1.0)}

            for ip in self.discovered_servers:
                self.status[ip] = MotorStatus.DISABLED
        except UDPDiscoverFailedException:
            logger.error("Discover failed.")  # TODO: add a health check guard
            return

    def _pvc(self, query: zenoh.Query, motor_cmd: str, motor_id: int, type_: str):
        type_dict = {
            "position": 0,
            "velocity": 1,
            "torque": 2,
        }
        if type_ not in type_dict:
            logger.error(f"Invalid PVC type: {type_}")
            query.reply_err("INVALID")
            return
        idx = type_dict[type_]
        motor_ip = f"{self.motor_id_prefix}{motor_id}"
        # return current position if no value is provided
        if query.value is None:
            query.reply(
                zenoh.Sample(
                    f"{self.prefix}/motor/{motor_cmd}/{motor_id}",
                    Serde.pack(self.readings[motor_ip][idx]),
                )
            )
            return

        addr = (motor_ip, FourierActuatorUDPPort.FAST)

        try:
            if self.status[motor_ip] == MotorStatus.DISABLED:
                self._sock.sendto(
                    FIFastProtocol(FIFastIdentifier.ENABLE).encode(),
                    addr,
                )
                self.status[motor_ip] = MotorStatus.ENABLED

            value = float(Serde.unpack(query.value.payload))
            match type_:
                case "position":
                    self._sock.sendto(
                        FIFastProtocol(FIFastIdentifier.MODE_POSITION).encode(),
                        addr,
                    )
                    self._sock.sendto(
                        FIFastProtocol(FIFastIdentifier.SET_POSITION, [value, 0.0, 0.0]).encode(),
                        addr,
                    )
                case "velocity":
                    self._sock.sendto(
                        FIFastProtocol(FIFastIdentifier.MODE_VELOCITY).encode(),
                        addr,
                    )
                    self._sock.sendto(
                        FIFastProtocol(FIFastIdentifier.SET_VELOCITY, [value, 0.0]).encode(),
                        addr,
                    )
                case "torque":
                    self._sock.sendto(
                        FIFastProtocol(FIFastIdentifier.MODE_TORQUE).encode(),
                        addr,
                    )
                    self._sock.sendto(
                        FIFastProtocol(FIFastIdentifier.SET_TORQUE, [value]).encode(),
                        addr,
                    )
                case _:
                    logger.error(f"Invalid type: {type_}")
                    query.reply_err("INVALID")
                    return
        except Exception:
            logger.error("Invalid position command.")
            query.reply_err("INVALID")

    def _service_callback(self, query: zenoh.Query):
        logger.info(
            f">> [Queryable] Received Query '{query.selector}'"
            + (f" with value: {query.value.payload}" if query.value is not None else "")
        )

        motor_cmd = str(query.key_expr).split("/")[-2]
        motor_id = int(str(query.key_expr).split("/")[-1])
        motor_ip = f"{self.motor_id_prefix}{motor_id}"
        logger.info(motor_cmd)

        match motor_cmd:
            case "info":
                # get root
                data = FIProtocol(method="GET", path="/")
                self._sock.sendto(data.encode(), (motor_ip, FourierActuatorUDPPort.CTRL))
                try:
                    data, _ = self._sock.recvfrom(1024)
                    decoded_data = json.loads(data.decode("utf-8"))
                    query.reply(
                        zenoh.Sample(
                            f"{self.prefix}/motor/{motor_cmd}/{motor_id}",
                            Serde.pack(decoded_data),
                        )
                    )

                except Exception:
                    logger.error(f"Failed to read motor {motor_id}.")

            case "enable":
                self._sock.sendto(
                    FIFastProtocol(FIFastIdentifier.ENABLE).encode(),
                    (motor_ip, FourierActuatorUDPPort.FAST),
                )
                self.status[motor_ip] = MotorStatus.ENABLED

            case "disable":
                self._sock.sendto(
                    FIFastProtocol(FIFastIdentifier.DISABLE).encode(),
                    (motor_ip, FourierActuatorUDPPort.FAST),
                )
                self.status[motor_ip] = MotorStatus.DISABLED
            case "reboot":
                self._sock.sendto(
                    FIProtocol(method="SET", path="/reboot").encode(),
                    (motor_ip, FourierActuatorUDPPort.CTRL),
                )
                self.status[motor_ip] = MotorStatus.DISABLED
                self.readings[motor_ip] = [0.0, 0.0, 0.0]

            case "position" | "velocity" | "torque":
                self._pvc(query, motor_cmd, motor_id, motor_cmd)

            case _:
                logger.info(f"Invalid motor command: {motor_cmd}")
                query.reply_err("INVALID")
                return

        query.reply(
            zenoh.Sample(
                f"{self.prefix}/motor/{motor_cmd}",
                Serde.pack({"status": ServiceStatus.OK}),
            )
        )
