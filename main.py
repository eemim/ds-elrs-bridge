import hid
from dataclasses import dataclass
import argparse

from crsf import channels_to_packet
from utils import (
    apply_deadzone,
    display_controller_state,
    normalize_axis,
    normalize_trigger
)
from serial_sender import send_crsf_packet, open_serial_port
from channel_map import state_to_channels

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
            # print(device)
            return device

    return None

def parse_args():
    parser = argparse.ArgumentParser(description="DS Controller to CRSF Bridge")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without serial port communication, print channel values instead.",
    )
    parser.add_argument(
        "--port",
        default="/dev/ttyUSB0",
        help="Serial port for ELRS TX module (default: /dev/ttyUSB0)",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    ds_device = find_ds()
    if not ds_device:
        print("No DS controller found.")
        return

    try:
        # print(f"Found DS controller at path: {ds_device['path']}")
        gamepad = hid.Device(path=ds_device["path"])
        print("DS controller opened successfully.")
    except Exception as e:
        print(f"Failed to open DS controller: {e}")
        return

    if not args.dry_run:
        try:
            serial_port = open_serial_port("/dev/ttyUSB0") #adjust the serial port as needed
        except Exception as e:
            print(f"Failed to open serial port: {e}")
            gamepad.close()
            return

    try:
        while True:
            report = gamepad.read(64)
            state = ControllerState.from_report(report)
            channels = state_to_channels(state)
            packet = channels_to_packet(channels)
            if not args.dry_run:
                send_crsf_packet(serial_port, packet)
            display_controller_state(state)
            # print(' '.join(f'{i}:{report[i]:3d}' for i in range(8, 12)))
            # state = ControllerState.from_report(report)
            # print(state)
            # Display the current state of the controller
            # display_controller_state(ControllerState.from_report(report))

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        gamepad.close()
        if not args.dry_run:
            serial_port.close()


if __name__ == "__main__":
    main()
