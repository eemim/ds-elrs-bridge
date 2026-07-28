def state_to_channels(state: "ControllerState") -> list[int]:
    """
    Convert the controller state to a list of channel values in CRSF range.
    """
    channels = [
        axis_to_crsf(state.right_stick_x),   # Channel 1: Right Stick X
        axis_to_crsf(state.right_stick_y),   # Channel 2: Right Stick Y
        axis_to_crsf(state.left_stick_y),    # Channel 3: Left Stick Y
        axis_to_crsf(state.left_stick_x),    # Channel 4: Left Stick X
        1811 if state.cross else 172,        # Channel 5: Cross Button
        992,                                 # CH6: unused
        992,                                 # CH7: unused
        992,                                 # CH8: unused
        992,                                 # CH9: unused
        992,                                 # CH10: unused
        992,                                 # CH11: unused
        992,                                 # CH12: unused
        992,                                 # CH13: unused
        992,                                 # CH14: unused
        992,                                 # CH15: unused
        992,                                 # CH16: unused
    ]
    return channels
