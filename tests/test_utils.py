from utils import (
    apply_deadzone,
    normalize_axis,
    normalize_trigger,
)


def test_apply_deadzone():
    assert apply_deadzone(120) == 128  # just inside deadzone (128 - 8 = 120)
    assert apply_deadzone(119) == 119  # just outside deadzone
    assert apply_deadzone(136) == 128  # just inside deadzone (128 + 8 = 136)
    assert apply_deadzone(137) == 137  # just outside deadzone

def test_normalize_axis():
    assert normalize_axis(128) == 0.0
    assert normalize_axis(0) == -1.0
    assert normalize_axis(255) == 1.0
    assert normalize_axis(64) == -0.5
    assert normalize_axis(192) == (192 - 128) / 127

def test_normalize_trigger():
    assert normalize_trigger(0) == 0.0
    assert normalize_trigger(255) == 1.0
    assert normalize_trigger(128) == 128 / 255
