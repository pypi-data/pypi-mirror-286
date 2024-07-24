# Copyright 2024 Fourier Intelligence
# Author: Yuxiang Gao <yuxiang.gao@fftai.com>
from __future__ import annotations

import socket
import time
from collections.abc import Sequence
from typing import Literal

from loguru import logger

from fourier_grx.sdk.fourier_intelligence import (
    FIFastIdentifier,
    FIFastProtocol,
    FIProtocol,
    FourierActuatorUDPPort,
)


class Gripper:
    def __init__(self, side: Literal["left", "right"]):
        self.side = side
        self.enabled = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1 / 30)
        self.reading = [0.0, 0.0, 0.0]

        match self.side:
            case "left":
                self.addr = ("192.168.137.17", FourierActuatorUDPPort.FAST)
            case "right":
                self.addr = ("192.168.137.37", FourierActuatorUDPPort.FAST)
            case _:
                raise ValueError(f"Invalid side {side}")

    def init(self):
        logger.info("gripper init start.")
        self.enable()
        self.close()
        time.sleep(0.1)
        logger.info("gripper init done.")

    def calibrate(self):
        logger.info("gripper calib start.")
        self.open()
        time.sleep(0.5)
        self.close()
        time.sleep(0.5)
        logger.info(f"gripper calib close done. angle: {self.angle}")
        logger.info("rebooting")
        self.reboot()
        self.enabled = False
        time.sleep(1)
        # retry reading till success
        while True:
            try:
                logger.info(f"gripper calib close done. angle: {self.angle}")
                break
            except Exception:
                logger.error("waiting for gripper to reboot.")
                time.sleep(0.5)

    def enable(self):
        self.sock.sendto(FIFastProtocol(FIFastIdentifier.ENABLE).encode(), self.addr)
        self.enabled = True

    def disable(self):
        self.sock.sendto(FIFastProtocol(FIFastIdentifier.DISABLE).encode(), self.addr)
        self.enabled = False

    def read(self):
        self.sock.sendto(FIFastProtocol(FIFastIdentifier.GET_PVC).encode(), self.addr)
        try:
            data, _ = self.sock.recvfrom(1024)
            decoded_data = FIFastProtocol.from_bytes(data)
            position, velocity, current = decoded_data.payload
            return position, velocity, current
        except TimeoutError:  # fail after 1 second of no activity
            return None

        except Exception:
            # traceback.print_exc()
            return None

    @property
    def angle(self):
        sensor_reading = self.read()
        if sensor_reading is not None:
            self.reading = sensor_reading
        return self.reading[0]

    @angle.setter
    def angle(self, angle=60.0):
        if not self.enabled:
            self.sock.sendto(FIFastProtocol(FIFastIdentifier.ENABLE).encode(), self.addr)
            self.enabled = True
        self.sock.sendto(FIFastProtocol(FIFastIdentifier.MODE_POSITION).encode(), self.addr)
        self.sock.sendto(
            FIFastProtocol(FIFastIdentifier.SET_POSITION, [float(angle), 0.0, 0.0]).encode(),
            self.addr,
        )

    @property
    def torque(self):
        sensor_reading = self.read()
        if sensor_reading is not None:
            self.reading = sensor_reading
        return self.reading[2]

    @torque.setter
    def torque(self, torque=-1.0):
        if not self.enabled:
            self.sock.sendto(FIFastProtocol(FIFastIdentifier.ENABLE).encode(), self.addr)
            self.enabled = True
        self.sock.sendto(FIFastProtocol(FIFastIdentifier.MODE_TORQUE).encode(), self.addr)
        self.sock.sendto(
            FIFastProtocol(FIFastIdentifier.SET_TORQUE, [float(torque)]).encode(),
            self.addr,
        )

    def open(self):
        self.angle = 50.0

    def close(self):
        self.torque = -0.5

    def reboot(self):
        data = FIProtocol(method="SET", path="/reboot")
        self.sock.sendto(data.encode(), (self.addr[0], FourierActuatorUDPPort.CTRL))


class InspireDexHand:
    def __init__(self, ip: str, port: int = 2333, timeout: float = 0.1):
        """Simple UDP client for Inspire Dex hand control

        Args:
            ip (str): Hand IP address, usually 192.168.137.19 and 192.168.137.39
            port (int, optional): Hand UDP port. Defaults to 2333.
            timeout (float, optional): UDP timeout. Defaults to 0.1.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.ip = ip
        self.port = port

    def set_positions(self, positions: Sequence[int], id: int = 1):
        """Set positions of the hand.

        Args:
            positions (Sequence[int]): 6 DOF positions, 1000 being fully open and 0 being fully closed.
            id (int, optional): Defaults to 1.

        Returns:
            _type_: _description_
        """
        send_data = bytearray()
        send_data.append(0xEB)  # 包头
        send_data.append(0x90)  # 包头
        send_data.append(int(id))  # 灵巧手 ID 号
        send_data.append(0x0F)  # 该帧数据部分长度 12 + 3
        send_data.append(0x12)  # 写寄存器命令标志
        send_data.append(0xCE)  # 寄存器起始地址低八位
        send_data.append(0x05)  # 寄存器起始地址高八位

        # Append val1 to val6 as little-endian
        positions = [int(pos) for pos in positions]
        for pos in positions:
            send_data.append(pos & 0xFF)
            send_data.append((pos >> 8) & 0xFF)

        # Calculate checksum
        checksum = sum(send_data[2:19]) & 0xFF
        send_data.append(checksum)

        self.sock.sendto(send_data, (self.ip, self.port))
        try:
            res, _ = self.sock.recvfrom(1024)
        except Exception as e:
            print(e)
            return None

        return res

    def get_positions(self, id: int = 1):
        send_data = bytearray()
        send_data.append(0xEB)  # 包头
        send_data.append(0x90)  # 包头
        send_data.append(int(id))
        send_data.append(0x04)
        send_data.append(0x11)  # kCmd_Handg3_Read
        send_data.append(0x0A)
        send_data.append(0x06)
        send_data.append(0x0C)

        checksum = sum(send_data[2:8]) & 0xFF
        send_data.append(checksum)

        self.sock.sendto(send_data, (self.ip, self.port))
        try:
            data, _ = self.sock.recvfrom(1024)
            received_checksum = data[19]
            calculated_checksum = sum(data[2:19]) & 0xFF

            if received_checksum != calculated_checksum:
                raise ValueError("Checksum mismatch")

            # print(data)
            pos = [
                data[7] | (data[8] << 8),
                data[9] | (data[10] << 8),
                data[11] | (data[12] << 8),
                data[13] | (data[14] << 8),
                data[15] | (data[16] << 8),
                data[17] | (data[18] << 8),
            ]

            return pos

        except Exception as e:
            print(e)
            return None
