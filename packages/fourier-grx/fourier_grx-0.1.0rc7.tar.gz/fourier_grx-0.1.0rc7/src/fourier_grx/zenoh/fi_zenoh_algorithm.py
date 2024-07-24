import time
from multiprocessing import Process

import zenoh
from fourier_core.config.fi_config import gl_config
from fourier_core.logger.fi_logger import Logger
from fourier_grx.control_system.fi_control_system_gr import ControlSystemGR as ControlSystem
from fourier_grx.zenoh.fi_zenoh_predefine import *
from ischedule import run_loop, schedule

# zenoh session and pub/sub
zenoh_session = None
zenoh_sub_robot_state = None
zenoh_pub_robot_control = None


def process_algorithm_init():
    Logger().print_trace("process_algorithm start...")

    p = Process(target=process_algorithm)
    p.start()

    # sleep some time to allow process started
    time.sleep(2)


def process_algorithm():
    # 算法子线程
    schedule_algorithm_init()

    # ischedule run loop
    run_loop()


def schedule_algorithm_init():
    global zenoh_session, zenoh_sub_robot_state, zenoh_pub_robot_control

    Logger().print_trace("thread_robot_algorithm start...")

    # zenoh preparation
    zenoh_session = zenoh.open()
    zenoh_sub_robot_state = zenoh_session.declare_subscriber(RCSGRZenohKey.KEY_ROBOT_STATE, callback_sub_robot_state)
    zenoh_pub_robot_control = zenoh_session.declare_publisher(RCSGRZenohKey.KEY_ROBOT_CONTROL)

    # start schedule
    target_algorithm_period_in_s = gl_config.parameters["robot"].get("algorithm_period", 0.01)  # 算法周期 100Hz

    schedule(schedule_algorithm, interval=target_algorithm_period_in_s)


def schedule_algorithm():
    global zenoh_pub_robot_control

    # run algorithm
    ControlSystem().robot_control_loop_algorithm()

    # output

    # publish robot control data
    robot_control_data = {"position": [0, 0, 0]}
    zenoh_pub_robot_control.put(robot_control_data)


def callback_sub_robot_state(data):
    print("callback_sub_robot_state data: ", data.payload)
