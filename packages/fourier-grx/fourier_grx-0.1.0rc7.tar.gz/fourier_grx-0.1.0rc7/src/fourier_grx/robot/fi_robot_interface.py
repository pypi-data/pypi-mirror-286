from fourier_core.config.fi_config import gl_config
from fourier_core.logger.fi_logger import Logger
from fourier_core.predefine.fi_robot_name import RobotName
from fourier_core.predefine.fi_robot_type import RobotType
from fourier_core.robot.fi_robot_interface import RobotInterface
from fourier_grx.robot.gr1.fi_robot_gr1_t1 import RobotGR1T1
from fourier_grx.robot.gr1.fi_robot_gr1_t1v2 import RobotGR1T1V2
from fourier_grx.robot.gr1.fi_robot_gr1_t1v3 import RobotGR1T1V3
from fourier_grx.robot.gr1.fi_robot_gr1_t2 import RobotGR1T2
from fourier_grx.robot.gr1.fi_robot_gr1_t3 import RobotGR1T3

# 根据配置文件中的机器人类型，初始化 RobotInterface
_robot_name = gl_config.parameters["robot"]["name"]
_robot_mechanism = gl_config.parameters["robot"]["mechanism"]

if _robot_name == RobotName.GR1 and _robot_mechanism == "T1":
    RobotInterface().type = RobotType.GR1
    RobotInterface().instance = RobotGR1T1()
    Logger().print_trace_highlight("RobotInterface().instance init RobotGR1T1")

if _robot_name == RobotName.GR1 and _robot_mechanism == "T1V2":
    RobotInterface().type = RobotType.GR1
    RobotInterface().instance = RobotGR1T1V2()
    Logger().print_trace_highlight("RobotInterface().instance init RobotGR1T1V2")

if _robot_name == RobotName.GR1 and _robot_mechanism == "T1V3":
    RobotInterface().type = RobotType.GR1
    RobotInterface().instance = RobotGR1T1V3()
    Logger().print_trace_highlight("RobotInterface().instance init RobotGR1T1V3")

if _robot_name == RobotName.GR1 and _robot_mechanism == "T2":
    RobotInterface().type = RobotType.GR1
    RobotInterface().instance = RobotGR1T2()
    Logger().print_trace_highlight("RobotInterface().instance init RobotGR1T2")

if _robot_name == RobotName.GR1 and _robot_mechanism == "T3":
    RobotInterface().type = RobotType.GR1
    RobotInterface().instance = RobotGR1T3()
    Logger().print_trace_highlight("RobotInterface().instance init RobotGR1T3")

# 如果 RobotInterface().instance 不为 None，则打印 RobotInterface().instance 的信息
if RobotInterface().instance is not None:
    RobotInterface().instance.log_info()
else:
    Logger().print_trace_error("fourier_grx.robot.fi_robot_interface.py RobotInterface().instance is None")
