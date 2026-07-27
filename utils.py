
# Apply deadzone for the analog sticks (drifting)
def apply_deadzone(value: int, center: int = 128,  deadzone: int = 8) -> int:
    if abs(value - center) < deadzone:
        return center
    return value

# Normalize the analog stick value to a range of -1.0 to 1.0
def normalize_axis(value: int, center: int = 128, max_value: int = 255) -> float:
    if value < center:
        return (value - center) / center
    else:
        return (value - center) / (max_value - center)

# Normalize the trigger value to a range of 0.0 to 1.0
def normalize_trigger(value: int, max_value: int = 255) -> float:
    return value / max_value

# Display the current state of the controller in one-line format
def display_controller_state(state: "ControllerState"):
    output = (
        f"LS:({state.left_stick_x:+.2f},{state.left_stick_y:+.2f}) "
        f"RS:({state.right_stick_x:+.2f},{state.right_stick_y:+.2f}) "
        f"L2:{state.l2:.2f} R2:{state.r2:.2f} "
        f"[{'□' if state.square else ' '}]"
        f"[{'×' if state.cross else ' '}]"
        f"[{'○' if state.circle else ' '}]"
        f"[{'△' if state.triangle else ' '}]"
        f" L1:[{'x' if state.l1 else ' '}]"
        f" R1:[{'x' if state.r1 else ' '}]"
    )
    print(output, end="\r", flush=True)
    
