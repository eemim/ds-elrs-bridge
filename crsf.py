def crsf_crc8(data: bytes) -> int:
    """
    Calculate the CRC8 checksum for the given data using the polynomial 0xD5.
    """
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0xD5
            else:
                crc <<= 1
            crc &= 0xFF  # Ensure CRC remains within 8 bits
    return crc

def pack_channels(channels: list[int]) -> bytes:
    buf = 0

    for i, ch in enumerate(channels):
        buf |= (ch & 0x07FF) << (i * 11)

    return buf.to_bytes(22, byteorder='little')

def build_crsf_packet(payload: bytes) -> bytes:

    sync_byte = 0xC8
    length = len(payload) + 2  # type + payload
    packet_type = 0x16  # CRSF frame type for RC channels
    packet = bytes([sync_byte, length, packet_type]) + payload
    crc = crsf_crc8(packet[1:])  # Calculate CRC8 for length + type + payload
    return packet + bytes([crc])

def channels_to_packet(channels: list[int]) -> bytes:
    payload = pack_channels(channels)
    return build_crsf_packet(payload)

