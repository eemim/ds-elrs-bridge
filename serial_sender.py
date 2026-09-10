import serial

CRSF_BAUD_RATE = 420000

def open_serial_port(port: str) -> serial.Serial:
    """
    Open the specified serial port with the CRSF baud rate.
    """
    return serial.Serial(
        port=port,
        baudrate=CRSF_BAUD_RATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

def send_crsf_packet(serial_port: serial.Serial, packet: bytes) -> None:
    """
    Send a CRSF packet over the specified serial port.
    """
    serial_port.write(packet)
