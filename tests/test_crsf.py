from crsf import channels_to_packet

def test_channels_to_packet():
    # All channels at center
    channels = [992] * 16
    packet = channels_to_packet(channels)

    assert len(packet) == 26
    assert packet[0] == 0xC8 
    assert packet[1] == 24
    assert packet[2] == 0x16 

def test_channel_packing_minimum():
    # all channels at minimum
    channels = [172] * 16
    packet = channels_to_packet(channels)
    payload = packet[3:25]
    buf = int.from_bytes(payload, byteorder='little')
    ch1 = buf & 0x07FF
    assert ch1 == 172, f"Expected 172, got {ch1}"

def test_channel_packing_maximum():
    # all channels at maximum
    channels = [1811] * 16
    packet = channels_to_packet(channels)
    payload = packet[3:25]
    buf = int.from_bytes(payload, byteorder='little')
    ch1 = buf & 0x07FF
    assert ch1 == 1811, f"Expected 1811, got {ch1}"

def test_channel_packing_center():
    # all channels at center
    channels = [992] * 16
    packet = channels_to_packet(channels)
    payload = packet[3:25]
    buf = int.from_bytes(payload, byteorder='little')
    ch1 = buf & 0x07FF
    assert ch1 == 992, f"Expected 992, got {ch1}"
