import sys
import time
from pathlib import Path

import numpy as np
import zenoh
from fourier_core.robot.fi_robot_base_task import RobotBaseTask
from ischedule import run_loop, schedule
from loguru import logger
from omegaconf import OmegaConf
from rich.console import Console
from rich.progress import track

from fourier_grx.sdk.constants import BASE_LINK
from fourier_grx.sdk.exceptions import FourierBaseException
from fourier_grx.sdk.robot import Robot
from fourier_grx.sdk.utils import ControlGroup, ControlMode, Serde, ServiceStatus
from fourier_grx.sdk.zenoh import ZenohSession

import threading

# Logger().state = Logger().STATE_OFF
np.set_printoptions(precision=3, suppress=True)


def flatten(matrix):
    return [item for row in matrix for item in row]


console = Console()

print = console.print
zenoh.init_logger()


class RobotServer(ZenohSession):
    def __init__(
        self,
        config: Path | str,
        urdf_path="urdf",
        freq: int = 400,
        prefix: str = "gr",
        visualize: bool = False,
        start: bool = True,
    ):
        """Robot server.

        Args:
            config (Path | str): Path to the fourier config file. Defaults to "config.yaml".
            urdf_path (str, optional): Path to the urdf folder. Defaults to "./urdf".
            freq (int, optional): Robot update frequency. Defaults to 400.
            prefix (str, optional): Namespace prefix. Defaults to "gr".
            visualize (bool, optional): Whether to enable visualization. Defaults to False.
            start (bool, optional): Whether to start the robot on initialization. Defaults to True.

        Raises:
            FourierBaseException: If failed to initialize control system.
        """
        zenoh_config = zenoh.Config()
        # zenoh_config.insert_json5("transport/unicast/lowlatency", "true")
        # zenoh_config.insert_json5("transport/unicast/qos/enabled", "false")
        super().__init__(prefix, config=zenoh_config)

        self._ctrl_sys_init = False
        self.freq = freq
        self._stop_event = threading.Event()

        try:
            self.fourier_config = Path(config)
            self.config = OmegaConf.load(self.fourier_config)
            self.robot_name = self.config.robot.name + self.config.robot.mechanism
            self.joint_names = self.config.actuator.names
        except Exception as ex:
            raise FourierBaseException("Failed to load robot config.") from ex

        try:
            urdf_path = Path(urdf_path)
            self.robot = Robot(
                self.robot_name,
                str(urdf_path / Path(self.robot_name + "/urdf/robot.urdf")),
                visualize=visualize,
            )
        except Exception as ex:
            raise FourierBaseException("Failed to initialize robot. Please check the urdf path.") from ex



        # fmt: off
        self.commands = {
            # control mode:
            # - 4: position control
            # - 5: PD control
            #
            # kp, kd:
            # - in position control mode: kp is position kp, kd is velocity kp
            # - in PD control mode: kp is position kp, kd is velocity kd
            "control_mode": [
                ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD,  # left leg
                ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD,  # right leg
                ControlMode.PD, ControlMode.PD, ControlMode.PD,  # waist
                ControlMode.PD, ControlMode.PD, ControlMode.PD,  # head
                ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD,  # left arm
                ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD,  # right arm
            ],
            "kp": [
                251.625, 362.52, 200, 200, 10.98, 10.98,  # left leg
                251.625, 362.52, 200, 200, 10.98, 10.98,  # right leg
                251.625, 251.625, 251.625,  # waist
                25.54, 25.54, 25.54,  # head
                92.85, 92.85, 112.06, 112.06, 112.06, 35.76, 35.76,  # left arm
                92.85, 92.85, 112.06, 112.06, 112.06, 35.76, 35.76,  # right arm
            ],
            "kd": [
                14.72, 10.0833, 11, 11, 0.6, 0.6,  # left leg
                14.72, 10.0833, 11, 11, 0.6, 0.6,  # right leg
                14.72, 14.72, 14.72,  # waist
                2.84, 2.84, 2.84,  # head
                2.575, 2.575, 3.1, 3.1, 3.1, 2.84, 2.84,  # left arm
                2.575, 2.575, 3.1, 3.1, 3.1, 2.84, 2.84,  # right arm
            ],
            # position (in urdf):
            # - unit: deg
            "position": [0.0] * 32,
        }
        # fmt: on

        # dev mode
        try:
            control_system = self.control_system
            logger.info(f"Control system initialized {control_system}")
            # print version info
            info_dict = control_system.get_info()
            logger.info(info_dict)
        except Exception as ex:
            raise FourierBaseException("Failed to initialize control system.") from ex

        time.sleep(0.1)
        self.control_system.sdk_mode(control_frequency=freq)

        self._subscribers = {
            "control": self.session.declare_subscriber(f"{self.prefix}/control/joints/*", self.ctrl_callback)
        }

        self._services = {
            "info": self.session.declare_queryable(
                f"{self.prefix}/robot/info",
                lambda query: query.reply(
                    zenoh.Sample(
                        str(query.key_expr),
                        Serde.pack(self.control_system.get_info()),
                    )
                ),
            ),
            "enable": self.session.declare_queryable(f"{self.prefix}/control/enable", self.service_enable_callback),
            "set_home": self.session.declare_queryable(f"{self.prefix}/control/set_home", self.service_motor_callback),
            "reboot": self.session.declare_queryable(f"{self.prefix}/control/reboot", self.service_motor_callback),
            "gains": self.session.declare_queryable(f"{self.prefix}/control/gains", self.service_gains_callback),
            "tf": self.session.declare_queryable(f"{self.prefix}/tf/**", self.service_tf_callback),
        }

        logger.info("RobotServer initialized.")

        if start:
            self.start()

    @property
    def control_system(self):
        # hack
        if not self._ctrl_sys_init:
            old_sys_argv = sys.argv
            sys.argv = [old_sys_argv[0], "--config", str(self.fourier_config)]

            from fourier_grx.control_system import (
                ControlSystemGR as ControlSystem,
            )

            sys.argv = old_sys_argv
            time.sleep(0.1)
            self._ctrl_sys_init = True
        from fourier_grx.control_system import (
            ControlSystemGR as ControlSystem,
        )

        return ControlSystem()

    @property
    def hardware_interface(self):
        """Must be called after control_system is initialized."""
        from fourier_core.hardware.fi_hardware_interface import (  # type: ignore
            HardwareInterface,  # type: ignore
        )

        return HardwareInterface().instance

    @property
    def robot_interface(self):
        """Must be called after control_system is initialized."""
        from fourier_core.robot.fi_robot_interface import RobotInterface  # type: ignore

        return RobotInterface().instance

    def service_tf_callback(self, query: zenoh.Query):
        logger.info(
            f">> [Queryable] Received Query '{query.selector}'"
            + (f" with value: {query.value.payload}" if query.value is not None else "")
        )

        query_path = str(query.key_expr).split("/")
        tf_query = query_path[query_path.index("tf") + 1 :]

        # print(tf_query)
        if query.value is not None:
            q = Serde.unpack(query.value.payload)
            q_tmp = self.robot.q.copy()
            # self.robot.set_joints(self.joint_names, q)
            self.robot.compute_forward_kinematics(np.deg2rad(q))

        match tf_query:
            case ["list"]:
                query.reply(
                    zenoh.Sample(
                        str(query.key_expr),
                        Serde.pack(self.robot.frame_names),
                    )
                )
            case [frame]:
                transform = self.robot.get_transform(frame, BASE_LINK)
                query.reply(
                    zenoh.Sample(
                        str(query.key_expr),
                        Serde.pack(transform),
                    )
                )
            case [from_frame, to_frame]:
                transform = self.robot.get_transform(to_frame, from_frame)
                query.reply(
                    zenoh.Sample(
                        str(query.key_expr),
                        Serde.pack(transform),
                    )
                )
            case _:
                logger.error(f"Invalid tf query: {tf_query}")
                query.reply_err(f"INVALID QUERY: {tf_query}")
        if query.value is not None:
            self.robot.set_joints(self.joint_names, q_tmp)

    def service_gains_callback(self, query: zenoh.Query):
        """Callback for gains service, if query.value is None, return current gains, else set new gains."""

        def pack_gains():
            return Serde.pack(
                {
                    "control_mode": self.commands["control_mode"],
                    "kp": self.commands["kp"],
                    "kd": self.commands["kd"],
                }
            )

        if query.value is None:
            query.reply(
                zenoh.Sample(
                    str(query.key_expr),
                    pack_gains(),
                )
            )
            return
        payload = Serde.unpack(query.value.payload)
        logger.info(
            f">> [Queryable] Received Query '{query.selector}'"
            + (f" with value: {payload}" if query.value is not None else "")
        )

        assert len(payload["kp"]) == len(self.commands["kp"])
        assert len(payload["kd"]) == len(self.commands["kd"])
        self.commands["control_mode"] = payload["control_mode"]
        self.commands["kp"] = payload["kp"]
        self.commands["kd"] = payload["kd"]
        # TODO: Do we want it to take effect immediately?
        # self.control_system.robot_control_loop_set_control(self.commands)
        query.reply(zenoh.Sample(str(query.key_expr), pack_gains()))

    def service_motor_callback(self, query: zenoh.Query):
        logger.info(
            f">> [Queryable] Received Query '{query.selector}'"
            + (f" with value: {query.value.payload}" if query.value is not None else "")
        )

        motor_cmd = str(query.key_expr).split("/")[-1]
        logger.info(motor_cmd)

        match motor_cmd:
            case "set_home":
                self.control_system.robot_control_set_task_command(task_command=RobotBaseTask.TASK_SET_HOME)
                for i in track(range(100), description="Waiting for set home..."):
                    time.sleep(10 / 100)
            case "reboot":
                # self.control_system.robot_control_set_task_command(
                #     task_command=RobotBaseTask.TASK_SERVO_REBOOT
                # )
                self.hardware_interface.fi_fsa_set_servo_reboot_group(
                    ips=[actuator.ip for actuator in self.robot_interface.actuators]
                )
                for i in track(range(100), description="Waiting for set home..."):
                    time.sleep(10 / 100)
            case _:
                logger.info(f"Invalid motor command: {motor_cmd}")
                query.reply_err("INVALID")
                return

        query.reply(
            zenoh.Sample(
                str(query.key_expr),
                Serde.pack({"status": ServiceStatus.OK}),
            )
        )

    def service_enable_callback(self, query: zenoh.Query):
        logger.info(
            f">> [Queryable] Received Query '{query.selector}'"
            + (f" with value: {query.value.payload}" if query.value is not None else "")
        )

        # params = query.decode_parameters()
        # attachments = query.attachment

        if query.value is None:
            logger.error("[Service] enable: INVALID VALUE")
            query.reply_err("Invalid value.")
            return

        cmd = Serde.unpack(query.value.payload)
        match cmd:
            case "ON":
                state_dict = self.robot_interface.control_loop_get_state()
                self.commands["position"] = state_dict["joint_position"].copy()
                self.control_system.robot_control_loop_set_control(self.commands)
                time.sleep(0.1)
                self.control_system.robot_control_set_task_command(task_command=RobotBaseTask.TASK_SERVO_ON)
                time.sleep(0.1)
                self.update_states()

                # for i in track(range(10), description="Waiting for servo on..."):
                #     time.sleep(1 / 10)
                logger.info("Servo on")
            case "OFF":
                self.control_system.robot_control_set_task_command(task_command=RobotBaseTask.TASK_SERVO_OFF)
                # for i in track(range(10), description="Waiting for servo off..."):
                #     time.sleep(1 / 10)
                logger.info("Servo off")
            case _:
                logger.error(f"[Service] enable: INVALID VALUE {cmd}")
                query.reply_err(f"Invalid value {cmd}.")
                return

        query.reply(zenoh.Sample(str(query.key_expr), Serde.pack(ServiceStatus.OK)))

    def update_states(self):
        # update state
        self.robot_interface.control_loop_intf_update_state()
        state_dict = self.robot_interface.control_loop_get_state()

        def put_by_name(name):
            """Parse sensor type and name from name, and publish the value."""
            parts = name.split("_")
            sensor_type = parts[0]
            sensor_name = "_".join(parts[1:])
            # log(
            #     f"Publishing '{self.prefix}/{sensor_type}/{sensor_name}': '{state_dict[name]}'"
            # )
            key = f"{self.prefix}/{sensor_type}/{sensor_name}"
            if key not in self._publishers:
                self._publishers[key] = self.session.declare_publisher(
                    key,
                    priority=zenoh.Priority.REAL_TIME(),
                    congestion_control=zenoh.CongestionControl.DROP(),
                )
            # from icecream import ic

            # ic(name, state_dict[name])
            self._publish(key, state_dict[name])

        for name in state_dict:
            put_by_name(name)

        # algorithm (user customized...)
        # time cost : 0.02ms
        self.robot_interface.control_loop_intf_algorithm()

        # output control
        self.robot_interface.control_loop_intf_output_control()

        self.update_robot(q=state_dict["joint_position"].copy())

    def update_robot(self, q: np.ndarray, degrees: bool = True):
        if degrees:
            q = np.deg2rad(q)
        # update robot configuration
        self.robot.set_joints(self.joint_names, q)
        self.robot.update()

    def ctrl_callback(self, sample: zenoh.Sample):
        available_control_types = ["position", "velocity", "effort"]
        control_type = str(sample.key_expr).split("/")[-1]
        if control_type not in available_control_types:
            logger.error(f"Invalid control type: {control_type}")
            return

        payload = Serde.unpack(sample.payload).copy()
        logger.trace(f"Received '{sample.key_expr}': '{np.round(payload[18:], 1)}'")
        # jp = self.control_system.robot_control_loop_get_state()["joint_position"]
        # logger.info(f"{np.round(jp[18:], 1)}")
        logger.trace(f"{sample.kind} {sample.encoding} {sample.qos} {sample.value} {sample.timestamp}")
        assert len(payload) == 32

        if control_type == "position":
            # clip ankle
            # payload[4] = np.clip(payload[4], -25, 25)
            # payload[10] = np.clip(payload[10], -25, 25)
            # payload[5] = np.clip(payload[5], -60, 30)
            # payload[11] = np.clip(payload[11], -60, 30)

            # clip wrists
            payload[23] = np.clip(payload[23], -35, 35)  # pitch
            payload[24] = np.clip(payload[24], -50, 55)  # roll
            payload[30] = np.clip(payload[30], -35, 35)
            payload[31] = np.clip(payload[31], -50, 55)
            self.commands["position"] = list(payload)
            self.control_system.robot_control_loop_set_control(self.commands)
        else:
            raise NotImplementedError

    def _spin(self):
        if self._frequency_log:
            self._frequency_count += 1
            if time.time() - self._frequency_count_reset_time > 1:
                self._frequency_count_reset_time = time.time()
                print(f"server update freq: {self._frequency_count} hz")
                self._frequency_count = 0

        self.update_states()

    def start(self):
        # record frequency info
        self._frequency_log = False
        self._frequency_count = 0
        self._frequency_count_reset_time = time.time()

        # ischedule loop
        schedule(self._spin, interval=1 / self.freq)
        run_loop(self._stop_event)

    # def spin(self):
    #     while True:
    #         self.loop_manager.start()
    #         self._spin()
    #         self.loop_manager.debug_print()

    #         self.loop_manager.end()
    #         self.loop_manager.sleep()

    def __del__(self):
        self.close()

    def close(self):
        self.control_system.robot_control_set_task_command(task_command=RobotBaseTask.TASK_SERVO_OFF)
        logger.info("Closing...")
        self._stop_event.set()
        time.sleep(1)
        super().close()
