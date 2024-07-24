import time
from multiprocessing import Process

import zenoh
from fourier_core.config.fi_config import gl_config
from fourier_core.logger.fi_logger import Logger
from fourier_grx.zenoh.fi_zenoh_predefine import *
from ischedule import run_loop, schedule

# zenoh session and pub/sub
zenoh_session = None
zenoh_pub_joystick = None


def process_communication_init():
    Logger().print_trace("process_communication start...")

    p = Process(target=process_communication)
    p.start()

    # sleep some time to allow process started
    time.sleep(2)


def process_communication():
    # 通信子线程
    schedule_communication_init()

    # ischedule run loop
    run_loop()


def schedule_communication_init():
    global zenoh_session, zenoh_pub_joystick

    Logger().print_trace("thread_robot_communication start...")

    # zenoh preparation
    zenoh_session = zenoh.open()
    zenoh_pub_joystick = zenoh_session.declare_publisher(RCSGRZenohKey.KEY_JOYSTICK)

    # start schedule
    target_comm_period_in_s = gl_config.parameters["robot"].get("communication_period", 0.02)  # 机器人通信周期 50Hz

    schedule(schedule_communication, interval=target_comm_period_in_s)


def schedule_communication():
    global zenoh_pub_joystick

    # ControlSystem().robot_control_loop_communication()

    # publish joystick data
    # joystick_data = {
    #
    # }
    # zenoh_pub_joystick.put(joystick_data)
