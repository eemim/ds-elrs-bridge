
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
