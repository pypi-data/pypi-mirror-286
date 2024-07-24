from threading import Thread

from fourier_core.predefine.fi_flag_state import FlagState
from fourier_core.predefine.fi_function_result import FunctionResult
from fourier_core.robot.fi_robot_base import RobotBaseTask
from fourier_grx.robot.fi_robot_interface import RobotInterface
from ischedule import run_loop, schedule


def other_mode_init(mode_name) -> int:
    # TODO: right now 400Hz is stable, need to change to use value in config.yaml later
    RobotInterface().instance.control_period = 1 / 400  # unit : s

    # change task command to RobotBaseTask.TASK_SERVO_ON
    RobotInterface().instance.task_command = RobotBaseTask.TASK_SERVO_ON
    RobotInterface().instance.flag_task_command_update = FlagState.SET

    # create thread
    thread_handle = Thread(target=thread_other_mode_handle, args=(mode_name,))
    thread_handle.start()

    return FunctionResult.SUCCESS


def thread_other_mode_handle(args):
    print("======================================================================================")
    mode_name = args[0]

    loop_period_in_s = RobotInterface().instance.control_period
    print("thread_", mode_name, "_mode_control_loop period: ", loop_period_in_s, "s")

    schedule(schedule_other_mode_handle, interval=loop_period_in_s)
    print("thread_other_mode_control_loop enter loop")

    run_loop()


def schedule_other_mode_handle():
    # update state
    RobotInterface().instance.control_loop_intf_update_state()

    # algorithm (user customized...)
    # time cost : 0.02ms
    RobotInterface().instance.control_loop_intf_algorithm()

    # output control
    RobotInterface().instance.control_loop_intf_output_control()
