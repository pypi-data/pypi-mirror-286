import threading
import time
from copy import copy
from dataclasses import dataclass

from inputs import InputEvent, get_gamepad


def remap(value, old_min, old_max, new_min, new_max):
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min


@dataclass
class Stick:
    x: float = 0
    y: float = 0
    value_range = (0, 255)  # (-32768, 32767)

    def update_x(self, value):
        # map (0, 255) to (-1, 1)
        lower, upper = self.value_range
        if value < lower or value > upper:
            self.value_range = (-32768, 32767)
        self.x = remap(value, lower, upper, -1, 1)

    def update_y(self, value):
        lower, upper = self.value_range
        if value < lower or value > upper:
            self.value_range = (-32768, 32767)
        self.y = remap(value, lower, upper, -1, 1)

    def reset(self):
        self.x = 0
        self.y = 0


class Button:
    def __init__(self):
        self.pressed = False

    def is_pressed(self):
        print(f"IS_PRESSED {self.pressed}")
        return self.pressed

    def update(self, value):
        if value == 1:
            self.pressed = True
        elif value == 0:
            self.pressed = False
        else:
            raise ValueError("Button value must be 0 or 1")
        # print(f"UPDATE {self.pressed} {value}")

    def reset(self):
        self.pressed = False


@dataclass(slots=True)
class Trigger:
    value: float

    def update(self, value):
        self.value = value

    def reset(self):
        self.value = 0

    def as_button(self, threshold=15):
        return self.value > 15


class GamePad(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self._lock = threading.Lock()
        self._shutdown_flag = threading.Event()

        self.sticks = {f"{name}": Stick() for name in ["left", "right"]}

        self.buttons = {
            f"{name}": Button()
            for name in ["south", "north", "west", "east", "logo", "select", "start", "mode", "l1", "l2", "r1", "r2"]
        }

        self.pad_buttons = {f"{name}": Button() for name in ["top", "right", "bottom", "left"]}

        self.triggers = {f"{name}": Trigger(0) for name in ["z", "rz"]}

    def stop(self):
        with self._lock:
            self.running = False
        self._shutdown_flag.set()

    def run(self):
        while self.running:
            events = get_gamepad()
            # with self._lock:
            for event in events:
                match event:
                    case InputEvent(ev_type="Absolute", code="ABS_X", state=state):
                        self.sticks["left"].update_x(state)
                    case InputEvent(ev_type="Absolute", code="ABS_Y", state=state):
                        self.sticks["left"].update_y(state)
                    case InputEvent(ev_type="Absolute", code="ABS_RX", state=state):
                        self.sticks["right"].update_x(state)
                    case InputEvent(ev_type="Absolute", code="ABS_RY", state=state):
                        self.sticks["right"].update_y(state)

                    case InputEvent(ev_type="Key", code="BTN_SOUTH", state=state):
                        self.buttons["south"].update(state)
                    case InputEvent(ev_type="Key", code="BTN_NORTH", state=state):
                        self.buttons["north"].update(state)
                    case InputEvent(ev_type="Key", code="BTN_EAST", state=state):
                        self.buttons["east"].update(state)
                    case InputEvent(ev_type="Key", code="BTN_WEST", state=state):
                        self.buttons["west"].update(state)
                    case InputEvent(ev_type="Key", code="BTN_MODE", state=state):
                        self.buttons["logo"].update(state)
                        self.buttons["mode"].update(state)
                    case InputEvent(ev_type="Key", code="BTN_SELECT", state=state):
                        self.buttons["select"].update(state)
                    case InputEvent(ev_type="Key", code="BTN_START", state=state):
                        self.buttons["start"].update(state)
                    case InputEvent(ev_type="Key", code="BTN_MODE", state=state):
                        self.buttons["mode"].update(state)
                        self.buttons["logo"].update(state)
                    # l1
                    case InputEvent(ev_type="Key", code="BTN_TL", state=state):
                        self.buttons["l1"].update(state)
                    # r1
                    case InputEvent(ev_type="Key", code="BTN_TR", state=state):
                        self.buttons["r1"].update(state)
                    # l2
                    case InputEvent(ev_type="Key", code="BTN_TL2", state=state):
                        self.buttons["l2"].update(state)
                    # r2
                    case InputEvent(ev_type="Key", code="BTN_TR2", state=state):
                        self.buttons["r2"].update(state)
                    # button_axis_left
                    case InputEvent(ev_type="Key", code="BTN_THUMBL", state=state):
                        self.buttons["axis_left"].update(state)
                    # button_axis_right
                    case InputEvent(ev_type="Key", code="BTN_THUMBR", state=state):
                        self.buttons["axis_right"].update(state)
                    # hat
                    case InputEvent(ev_type="Absolute", code="ABS_HAT0X", state=state):  # -1 is left, 1 is right
                        if state == 0:
                            self.pad_buttons["left"].update(0)
                            self.pad_buttons["right"].update(0)
                        elif state == -1:
                            self.pad_buttons["left"].update(1)
                            self.pad_buttons["right"].update(0)
                        elif state == 1:
                            self.pad_buttons["left"].update(0)
                            self.pad_buttons["right"].update(1)

                    case InputEvent(ev_type="Absolute", code="ABS_HAT0Y", state=state):  # -1 is up, 1 is down
                        if state == 0:
                            self.pad_buttons["top"].update(0)
                            self.pad_buttons["bottom"].update(0)
                        elif state == -1:
                            self.pad_buttons["top"].update(1)
                            self.pad_buttons["bottom"].update(0)
                        elif state == 1:
                            self.pad_buttons["top"].update(0)
                            self.pad_buttons["bottom"].update(1)

                    case InputEvent(ev_type="Absolute", code="ABS_Z", state=state):
                        self.triggers["z"].update(state)
                    case InputEvent(ev_type="Absolute", code="ABS_RZ", state=state):
                        self.triggers["rz"].update(state)

                    # case _:
                    # print(event.ev_type, event.code, event.state)
                # print(event.ev_type, event.code, event.state)
                # print(id(self.buttons["l1"]), self.buttons["l1"].pressed)

            if self._shutdown_flag.is_set():
                break

    def read(self):
        with self._lock:
            res = {}
            res.update({f"{name}_stick_x": stick.x for name, stick in self.sticks.items()})
            res.update({f"{name}_stick_y": stick.y for name, stick in self.sticks.items()})
            res.update({f"button_{name}": button.pressed for name, button in self.buttons.items()})
            res.update({f"pad_button_{name}": button.pressed for name, button in self.pad_buttons.items()})
            res.update({f"trigger_{name}": trigger.value for name, trigger in self.triggers.items()})
            return res


def main():
    gamepad = GamePad()
    gamepad.start()
    try:
        while True:
            res = gamepad.read()
            # print("ZZZZZ", res["button_l1"], copy(gamepad.buttons["l1"].pressed))
            print(res)
            time.sleep(0.01)
    except KeyboardInterrupt:
        gamepad.stop()


if __name__ == "__main__":
    main()
