import json
import time
from multiprocessing import Process

import zenoh
from fourier_core.config.fi_config import gl_config
from fourier_core.logger.fi_logger import Logger
from fourier_core.predefine.fi_function_result import FunctionResult
from fourier_grx.control_system.fi_control_system_gr import ControlSystemGR as ControlSystem
from fourier_grx.zenoh.fi_zenoh_predefine import *
from ischedule import run_loop, schedule

# zenoh session and pub/sub
zenoh_session = None
zenoh_pub_robot_state = None
zenoh_sub_robot_control = None


def process_control_init():
    Logger().print_trace("process_control start...")

    p = Process(target=process_control)
    p.start()

    # sleep some time to allow process started
    time.sleep(2)


def process_control():
    # 控制子线程
    schedule_control_init()

    # ischedule run loop
    run_loop()


def schedule_control_init():
    global zenoh_session, zenoh_pub_robot_state, zenoh_sub_robot_control

    Logger().print_trace("thread_robot_control start...")

    # zenoh preparation
    zenoh_session = zenoh.open()
    zenoh_pub_robot_state = zenoh_session.declare_publisher(RCSGRZenohKey.KEY_ROBOT_STATE)
    zenoh_sub_robot_control = zenoh_session.declare_subscriber(
        RCSGRZenohKey.KEY_ROBOT_CONTROL, callback_sub_robot_control
    )

    # start schedule
    period_control = gl_config.parameters["robot"].get("control_period", 0.0025)  # 机器人控制周期 400Hz
    period_pub_robot_state = gl_config.parameters["robot"].get("control_period", 0.0025)  # 机器人控制周期 400Hz

    # set debug mode
    result = ControlSystem().debug_mode(control_period=period_control)

    if result != FunctionResult.SUCCESS:
        Logger().print_trace_error("main_zenoh.py thread_robot_control ControlSystem().debug_mode failed!!!")
        return FunctionResult.FAIL

    # start control loop
    schedule(schedule_control, interval=period_control)
    schedule(schedule_pub_robot_state, interval=period_pub_robot_state)


def schedule_control():
    ControlSystem().robot_control_loop_run_noalgortihm()


def schedule_pub_robot_state():
    global zenoh_pub_robot_state

    state_dict = ControlSystem().robot_control_loop_get_state()
    state_data = json.dumps(state_dict)

    # publish robot state data
    zenoh_pub_robot_state.put(state_data)


def callback_sub_robot_control(data):
    control_dict = json.loads(data.payload)
    ControlSystem().robot_control_loop_set_control(control_dict)
