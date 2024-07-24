import time

from fourier_core.control_system.fi_control_system import ControlSystem
from fourier_core.logger.fi_logger import Logger
from fourier_core.predefine.fi_deploy_mode import DeployMode
from fourier_core.predefine.fi_function_result import FunctionResult
from fourier_grx.control_system.fi_control_system_other_mode import other_mode_init
from fourier_grx.robot.fi_robot_interface import RobotInterface


class ControlSystemGR(ControlSystem):
    def agv_mode(self) -> int:
        # robot model check
        if RobotInterface().instance is None:
            Logger().print_trace_error(
                "fi_control_system_gr.py robot_control_loop_init " "The robot model has not been initialized!!!"
            )
            return FunctionResult.FAIL

        # change deploy mode to AGV_MODE
        RobotInterface().instance.deploy_mode = DeployMode.AGV_MODE

        # init, comm, prepare robot
        self.robot_control_loop_before()

        # mode init
        other_mode_init(mode_name="agv")

        # sleep some time to allow data updated
        time.sleep(2)

        return FunctionResult.SUCCESS
