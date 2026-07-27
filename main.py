import hid
import time
from dataclasses import dataclass
from utils import apply_deadzone, normalize_axis, normalize_trigger

DS_VENDOR_ID = 0x054C
DS_PRODUCT_ID = 0x0CE6


@dataclass
class ControllerState:
    left_stick_x: float
    left_stick_y: float
    right_stick_x: float
    right_stick_y: float
    l2: float
    r2: float
    square: bool
    cross: bool
    circle: bool
    triangle: bool
    l1: bool
    r1: bool

    @classmethod
    def from_report(cls, report: list[int]) -> "ControllerState":
        return cls(
            left_stick_x=normalize_axis(apply_deadzone(report[1])),
            left_stick_y=normalize_axis(apply_deadzone(report[2])),
            right_stick_x=normalize_axis(apply_deadzone(report[3])),
            right_stick_y=normalize_axis(apply_deadzone(report[4])),
            l2=normalize_trigger(report[5]),
            r2=normalize_trigger(report[6]),
            square=bool(report[8] & 0x10),
            cross=bool(report[8] & 0x20),
            circle=bool(report[8] & 0x40),
            triangle=bool(report[8] & 0x80),
            l1=bool(report[9] & 0x01),
            r1=bool(report[9] & 0x02),
        )

def find_ds():
    # Enumerate all connected HID devices
    for device in hid.enumerate():
        if (
            device["vendor_id"] == DS_VENDOR_ID
            and device["product_id"] == DS_PRODUCT_ID
        ):
            print(device)
            return device

    return None

def main():
    ds_device = find_ds()
    if not ds_device:
        print("No DS controller found.")
        return

    print(f"Found DS controller at path: {ds_device['path']}")

    gamepad = hid.Device(path=ds_device["path"])
    print("DS controller opened successfully.")

    while True:
        report = gamepad.read(64)

        # print(' '.join(f'{i}:{report[i]:3d}' for i in range(8, 12)))
        state = ControllerState.from_report(report)
        print(state)

    gamepad.close()


if __name__ == "__main__":
    main()
