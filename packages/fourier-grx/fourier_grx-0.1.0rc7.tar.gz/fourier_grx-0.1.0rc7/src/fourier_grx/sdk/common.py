# Copyright 2024 Fourier Intelligence
# Author: Yuxiang Gao <yuxiang.gao@fftai.com>

from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import wraps
from typing import Any

import numpy as np
from loguru import logger

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa


singleton_lock = threading.Lock()


class PluginRegistrar:
    """Register plugins for a specific type."""

    _plugins = defaultdict(list)

    @staticmethod
    def register(type_: str):
        """
        Register a plugin for  a specific type.

        Args:
            type_ (str): The type of the plugin.
        """

        def wrapper(cls):
            if cls not in PluginRegistrar._plugins[type_]:
                PluginRegistrar._plugins[type_].append(cls)
            return cls

        return wrapper

    @staticmethod
    def get_plugins(type_: str):
        """
        Get all registered plugins for a specific type.

        Args:
            type_ (str): The type of the plugin.

        Returns:
            list: A list of registered plugins for the specific type.
        """

        return PluginRegistrar._plugins[type_]

    @staticmethod
    def get_plugin(type_: str, name: str):
        """
        Get a registered plugin by name for a specific type.

        Args:
            type_ (str): The type of the plugin.
            name (str): The name of the plugin.

        Returns:
            Any: The plugin instance.
        """

        for plugin in PluginRegistrar._plugins[type_]:
            if plugin.__name__ == name:
                return plugin
        return None


class Singleton(type):
    """Thread-safe Singleton metaclass. Use it to create a singleton class.
    Source: https://stackoverflow.com/a/6798042

    Usage:

    .. code-block:: python
        class MySingletonClass(metaclass=Singleton):
            pass
    """

    _instances: dict[type, Singleton] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with singleton_lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def instance(cls: Any, *args: Any, **kwargs: Any) -> Any:
        return cls(*args, **kwargs)


@dataclass
class Extrema:
    min: float = float("inf")
    max: float = float("-inf")

    def update(self, value: float):
        self.min = min(self.min, value)
        self.max = max(self.max, value)


@dataclass
class LoopManager:
    """Manages loop timing and rate for a given loop."""

    name: str
    target_frequency: float
    curr_rate_history: deque[float] = field(default_factory=lambda: deque(maxlen=100))
    exec_rate_history: deque[float] = field(default_factory=lambda: deque(maxlen=100))
    rate_extrema: Extrema = field(default_factory=Extrema)
    num_loops: int = 0
    missed_loops: int = 0

    _ts_loop_start: float = 0
    _ts_loop_end: float = 0
    _last_ts_loop_start: float = 0
    _exec_time_s: float = 0
    _sleep_time_s: float = 0
    _ts_0 = time.perf_counter()

    def start(self):
        """Start the loop timing."""

        self.num_loops += 1
        self._ts_loop_start = time.perf_counter()
        if self._last_ts_loop_start is None:
            self._last_ts_loop_start = self._ts_loop_start
            return

        curr_rate = 1 / (self._ts_loop_start - self._last_ts_loop_start)
        self.rate_extrema.update(curr_rate)
        self.curr_rate_history.append(curr_rate)
        if self._exec_time_s > 0:
            self.exec_rate_history.append(1 / self._exec_time_s)

        self._last_ts_loop_start = self._ts_loop_start

        # Calculate sleep time to achieve desired loop rate
        self._sleep_time_s = (1 / self.target_frequency) - self._exec_time_s
        if (
            self._sleep_time_s < 0.0 and time.perf_counter() - self._ts_0 > 5.0
        ):  # Allow 5s for timing to stabilize on on_startup
            self.missed_loops += 1
            if self.missed_loops == 1:
                logger.warning(
                    f"Missed target loop rate of {self.target_frequency:.2f} Hz for {self.name}. Currently {self.curr_rate_hz:.2f} Hz"
                )

    def end(self):
        """End the loop timing."""

        if self._ts_loop_start is None:
            return
        self._ts_loop_end = time.perf_counter()
        self._exec_time_s = self._ts_loop_end - self._ts_loop_start

    def end_with_sleep(self):
        """Call end() and sleep() in one go."""
        self.end()
        self.sleep()

    def sleep(self, min_time_s=0.0005):
        if self._ts_loop_start is None:
            time.sleep(0.01)
            return

        while time.perf_counter() - self._ts_loop_start < 1 / self.target_frequency:
            time.sleep(min_time_s)

    def monitor(self):
        """decorator to monitor loop timing"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.start()
                func(*args, **kwargs)
                self.end()
                self.sleep()

            return wrapper

        return decorator

    def debug_print(self, every_n_loops=50):
        if self.num_loops % every_n_loops == 0:
            logger.debug(f"------------ LoopManager {self.name} {self.num_loops} --------------")
            logger.debug(f"Current rate: {self.curr_rate_hz:.2f} Hz")
            logger.debug(f"Average rate: {self.avg_rate_hz:.2f} Hz")
            logger.debug(f"Std rate: {self.std_rate_hz:.2f} Hz")
            logger.debug(f"Min rate: {self.rate_extrema.min:.2f} Hz")
            logger.debug(f"Max rate: {self.rate_extrema.max:.2f} Hz")
            logger.debug(f"Execution rate: {self.avg_exec_rate_hz:.2f} Hz")
            logger.debug(f"Std execution rate: {self.std_exec_rate_hz:.2f} Hz")
            logger.debug(f"Missed loops: {self.missed_loops} / {self.num_loops}")
            logger.debug(f"Sleep time: {self._sleep_time_s:.6f} s")

    @property
    def exec_time_s(self):
        return self._exec_time_s

    @property
    def curr_rate_hz(self):
        return self.curr_rate_history[-1] if self.curr_rate_history else None

    @property
    def avg_rate_hz(self):
        return np.mean(self.curr_rate_history)

    @property
    def std_rate_hz(self):
        return np.std(self.curr_rate_history)

    @property
    def avg_exec_rate_hz(self):
        return np.mean(self.exec_rate_history)

    @property
    def std_exec_rate_hz(self):
        return np.std(self.exec_rate_history)


class ThreadedTask(threading.Thread, ABC):
    def __init__(self, name: str, target_frequency: float, daemon=False):
        """Base class for creating a threaded task.
        Source: https://vmois.dev/python-flask-background-thread/

        Args:
            name (str): name of the task
            target_frequency (float): target frequency of the task
            daemon (bool, optional): whether the thread is a daemon. Defaults to False.
        """
        threading.Thread.__init__(self, name=name, daemon=daemon)
        self.loop = LoopManager(name, target_frequency=target_frequency)
        self._stop_event = threading.Event()
        self.running = False

    def stop(self) -> None:
        self._stop_event.set()

    # def unstop(self) -> None:
    #     self._stop_event.clear()

    @property
    def stopped(self) -> bool:
        return self._stop_event.is_set()

    @abstractmethod
    def on_startup(self) -> None:
        """
        Method that is called before the thread starts.
        Initialize all necessary resources here.
        """
        raise NotImplementedError()

    @abstractmethod
    def on_shutdown(self) -> None:
        """
        Method that is called shortly after stop() method was called.
        Use it to clean up all resources before thread stops.
        """
        raise NotImplementedError()

    @abstractmethod
    def handle(self) -> None:
        """
        Method that should contain business logic of the thread.
        Will be executed in the loop until stop() method is called.
        Must not block for a long time.
        """
        raise NotImplementedError()

    def run(self) -> None:
        """
        This method will be executed in a separate thread
        when start() method is called.
        """
        self.running = True
        self._stop_event.clear()  # Ensure the thread is not stopped before starting
        logger.trace(f"Starting thread: {self.name}")
        self.on_startup()
        while not self.stopped:
            self.loop.start()
            self.handle()
            self.loop.end()
            self.loop.sleep()  # TODO: allow configurable sleep time
        logger.trace(f"Stopping thread: {self.name}")
        self.running = False
        self.on_shutdown()
