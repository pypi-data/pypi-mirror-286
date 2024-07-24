import typer
import time
from .client import RobotClient
from .server import RobotServer

app = typer.Typer()


@app.command()
def run(
    config: str = typer.Argument(help="Path to the config file"),
    urdf_path: str = typer.Option("./urdf", help="Path to the urdf file"),
    freq: int = typer.Option(400, help="Main loop frequency in hz. defaults to 400hz."),
    verbose: bool = typer.Option(True, help="Print internal debug info"),
    visualize: bool = typer.Option(False, help="Visualize the robot in rviz"),
):
    """Run the robot server."""
    if not verbose:
        from fourier_core.logger.fi_logger import Logger

        Logger().state = Logger().STATE_OFF

    robot = RobotServer(config, urdf_path=urdf_path, freq=freq, visualize=visualize)


@app.command()
def calibrate(output_path: str = typer.Argument(default="sensor_offsets.json", help="Path to the output file")):
    """Calibrate the robot sensors and save the offsets to a file"""
    client = RobotClient(400)
    client.set_home()
    client.close()


@app.command()
def generate_sensor_offset():
    """Generate sensor offset file from the control SDK installed on the host machine, usually located at ~/RoCS/bin/pythonscripts/absAngle.json"""
    from fourier_grx.tools.load_sensor_offset import load_sensor_offset

    load_sensor_offset()


@app.command()
def disable():
    """Disable all the motors."""
    client = RobotClient(400)
    time.sleep(0.1)
    client.set_enable(False)
    time.sleep(0.1)
    client.close()


@app.command()
def enable():
    """Enable all the motors."""
    client = RobotClient(400)
    time.sleep(0.1)
    client.set_enable(True)
    time.sleep(0.1)
    client.close()


@app.command()
def states():
    """Print the current robot states."""
    import time

    import numpy as np
    from rich.console import Console
    from rich.table import Table

    console = Console()
    print = console.print
    client = RobotClient(400)
    time.sleep(0.1)
    table = Table("Type", "Data", title="Current :robot: states")
    for sensor_type, sensor_data in client.states.items():
        for sensor_name, sensor_reading in sensor_data.items():
            # print(sensor_type + "/" + sensor_name, sensor_reading.tolist())
            table.add_row(
                sensor_type + "/" + sensor_name,
                str(np.round(sensor_reading, 3)),
            )
    print(table)

    client.close()


if __name__ == "__main__":
    app()
