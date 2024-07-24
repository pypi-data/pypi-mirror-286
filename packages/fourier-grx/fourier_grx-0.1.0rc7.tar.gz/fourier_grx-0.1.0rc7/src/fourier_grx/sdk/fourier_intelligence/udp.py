# Copyright 2024 Fourier Intelligence
# Author: Yuxiang Gao <yuxiang.gao@fftai.com>
from __future__ import annotations

import json
import queue
import socket
import threading
import time
from collections import defaultdict
from typing import TypeAlias

from loguru import logger

from .common import (
    FIFastIdentifier,
    FIFastProtocol,
    FIProtocol,
    FourierServer,
    FourierUDPPort,
)

IpPortAddrType: TypeAlias = tuple[str, FourierUDPPort | int]
TimestampType: TypeAlias = float
QueuedMsgType: TypeAlias = tuple[bytes, IpPortAddrType, TimestampType]


class FIException(Exception): ...


class UDPRequestException(FIException): ...


class UDPDiscoverFailedException(FIException): ...


def sort_ips(ips: list[str]) -> list[str]:
    return sorted(ips, key=lambda x: int(x.split(".")[-1]))


def discover_servers(timeout=1.0, address=("192.168.137.255", 2334)):
    """Discover Fourier servers on the network

    Args:
        address (tuple): Broadcast address and port
        timeout (float): Timeout for the discovery process

    Raises:
        UDPDiscoverFailedException: Raised when no servers are discovered

    Returns:
        discovered_addresses (list): List of discovered server addresses
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

    logger.info("[DISCOVER] Start.")

    s.sendto(b"Is any fourier smart server here?", address)

    discovered_servers: list[FourierServer] = []

    while True:
        try:
            data, address = s.recvfrom(1024)
            res = json.loads(data.decode("utf-8"))
            logger.trace(f"[DISCOVER] {address} discovered. ")
            logger.trace(f"{res}")

            server = FourierServer.new(
                ip=address[0],
                type_=res.get("type"),
                status="CONNECTED" if res.get("status") == "OK" else "ERROR",
            )

            discovered_servers.append(server)

        except TimeoutError as exc:
            s.close()
            # todo: not ideal to place logic in except block
            if discovered_servers:
                logger.info(f"[DISCOVER] End. {len(discovered_servers)} servers discovered.")
                return sorted(discovered_servers)

            logger.error("[DISCOVER] Timeout.")
            raise UDPDiscoverFailedException from exc


class SendThread(threading.Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(name="UDPSendThread", daemon=False)
        self._queue: queue.Queue[QueuedMsgType] = queue.Queue()
        self._stop_event = threading.Event()
        self._sock = sock

    def stop(self):
        """Stop the thread."""
        self._stop_event.set()

    @property
    def stopped(self) -> bool:
        """Whether the thread is stopped."""
        return self._stop_event.is_set()

    def send(self, data: bytes, address: IpPortAddrType | str):
        if isinstance(address, str):
            ip, port = address.split(":")
            address = (ip, int(port))
        # TODO: drop data if queue is full or timed out
        self._queue.put_nowait((data, address, time.time()))

    def run(self):
        self._stop_event.clear()
        logger.debug(f"{self.name} started.")
        while not self.stopped:
            if self._queue.empty():
                time.sleep(1 / 500)
                continue
            try:
                data, address, timestamp = self._queue.get_nowait()
                latency = time.time() - timestamp
                self._sock.sendto(data, address)
                logger.trace(f"SendThread sending data to {address}. Latency: {latency:.3f}s")

            except queue.Empty:
                logger.trace("SendThread queue is empty.")
                time.sleep(1 / 500)
                continue
            except Exception as exp:
                logger.exception(f"SendThread error: {exp}")
                raise FIException from exp

        logger.debug(f"{self.name} stopped.")
        # self._sock.close()


class ReceiveThread(threading.Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(name="UDPReceiveThread", daemon=False)
        self._stop_event = threading.Event()
        self._sock = sock
        self._recv_dict: defaultdict[IpPortAddrType, queue.Queue[QueuedMsgType]] = defaultdict(queue.Queue)

    def stop(self):
        """Stop the thread."""
        self._stop_event.set()

    @property
    def stopped(self) -> bool:
        """Whether the thread is stopped."""
        return self._stop_event.is_set()

    def get(self, addr: IpPortAddrType, timeout=0.1) -> tuple[bytes | None, TimestampType | None]:
        try:
            data, _, ts = self._recv_dict[addr].get(timeout=timeout)
            return data, ts
        except queue.Empty:
            return None, None

    def get_nowait(self, addr: IpPortAddrType) -> tuple[bytes | None, TimestampType | None]:
        try:
            data, _, ts = self._recv_dict[addr].get_nowait()
            return data, ts
        except queue.Empty:
            return None, None

    def is_empty(self, addr: IpPortAddrType) -> bool:
        return self._recv_dict[addr].empty()

    def run(self):
        self._stop_event.clear()
        logger.debug(f"{self.name} started.")
        # self._sock.settimeout(1. / 500) # TODO: this need to be tested
        while not self.stopped:
            try:
                data, address = self._sock.recvfrom(1024)
                logger.trace(f"ReceiveThread received data from {address}")
                self._recv_dict[address].put_nowait((data, address, time.time()))
            except TimeoutError:
                # TODO: count the number of timeouts and raise an exception if it exceeds a threshold
                time.sleep(1 / 500)  # FIXME: is this sleep necessary?
                continue
            except BlockingIOError:
                # ic(err)
                time.sleep(1 / 500)
                continue
            except Exception as exp:
                logger.exception(f"ReceiveThread error: {exp}")
                raise FIException from exp

        logger.debug(f"{self.name} stopped.")
        # self._sock.close()


class FIUDPClient:  # TODO: could be a singleton?
    def __init__(self, timeout=1 / 500):
        self.discovered_servers: dict[str, FourierServer] = {}
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,128 * 1024) # TODO: test this
        # self._sock.setblocking(False)
        self._sock.settimeout(timeout)
        self._sock.bind(("", 0))
        self.send_thread = SendThread(self._sock)
        self.recv_thread = ReceiveThread(self._sock)
        self.running = False

    def discover(self, timeout=1.0):
        """Broadcast to discover servers on the network."""
        try:
            self.discovered_servers = {s.ip: s for s in discover_servers(timeout=timeout)}
        except UDPDiscoverFailedException:
            logger.error("Discover failed.")  # TODO: add a health check guard
            return

    @property
    def activated_servers(self) -> list[FourierServer]:
        return [s for s in self.discovered_servers.values() if s.activated]

    def activate(self, addresses: list[tuple[str, str]]):
        """Activate a list of FI servers by name and address.

        Args:
            addresses (list): List of tuples containing name and address of the servers
        """
        for name, addr in addresses:
            if addr not in self.discovered_servers:
                logger.warning(f"Trying to activate an address {addr} not in discovered addresses.")
                continue
            self.discovered_servers[addr].activated = True
            self.discovered_servers[addr].name = name

    def start(self):
        if not self.discovered_servers:
            logger.error("No servers discovered.")
            raise UDPDiscoverFailedException("No servers discovered.")
        self.send_thread.start()
        self.recv_thread.start()
        self.running = True

    def stop(self):
        self.running = False
        self.send_thread.stop()
        self.recv_thread.stop()
        time.sleep(0.1)
        self._sock.close()

    def send(self, data: bytes, addr: IpPortAddrType):
        self.send_thread.send(data, addr)

    def get(self, addr: IpPortAddrType, timeout=0.1) -> tuple[bytes | None, TimestampType | None]:
        return self.recv_thread.get(addr, timeout)

    def get_nowait(self, addr: IpPortAddrType) -> tuple[bytes | None, TimestampType | None]:
        return self.recv_thread.get_nowait(addr)

    def get_all(self, addr: IpPortAddrType) -> list[tuple[bytes, TimestampType]]:
        results = []
        while True:
            res, ts = self.get_nowait(addr)
            if res is None:
                return results
            results.append((res, ts))

    def enable(self, addr: IpPortAddrType):
        if addr[0] not in self.discovered_servers:
            raise FIException(f"Invalid server address {addr}")
        self.discovered_servers[addr[0]].enabled = True
        data = FIFastProtocol(ident=FIFastIdentifier.ENABLE)
        self.send(data.encode(), addr)  # type: ignore
        res, ts = self.get(addr, timeout=0.1)
        if res is None:
            return None
        return res

    def disable(self, addr: IpPortAddrType):
        if addr[0] not in self.discovered_servers:
            raise FIException(f"Invalid server address {addr}")
        self.discovered_servers[addr[0]].enabled = False
        data = FIFastProtocol(ident=FIFastIdentifier.DISABLE)
        self.send(data.encode(), addr)  # type: ignore
        res, ts = self.get(addr, timeout=0.1)
        if res is None:
            return None
        return res

    def get_root(self, addr: IpPortAddrType):
        data = FIProtocol(method="GET", path="/")
        self.send(data.encode(), addr)
        res, ts = self.get(addr, timeout=0.1)
        if res is None:
            return None
        res = json.loads(res.decode("utf-8"))
        return res

    def __del__(self):
        self.stop()
        del self.send_thread
        del self.recv_thread
        del self._sock
