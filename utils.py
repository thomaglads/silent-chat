# utils.py
"""
Utility functions for Silent Chat protocol.
"""

START_BYTE = 0xAA
END_BYTE = 0xFF

# Command codes
CMD_GREET = 0x01
CMD_DATA = 0x02
CMD_BYE = 0x03

def build_packet(command: int, data: str) -> bytes:
    """
    Build a binary packet from command and data string.
    """
    encoded_data = data.encode('utf-8')
    length = len(encoded_data)
    if length > 255:
        raise ValueError("Data too long (max 255 bytes)")
    
    return bytes([START_BYTE, command, length]) + encoded_data + bytes([END_BYTE])

def parse_packet(packet: bytes) -> tuple[int, str]:
    """
    Parse a binary packet into (command, data) tuple.
    Raises ValueError if packet is invalid.
    """
    if len(packet) < 5:  # at least start, command, length, 1 data byte, end
        raise ValueError("Packet too short")
    if packet[0] != START_BYTE or packet[-1] != END_BYTE:
        raise ValueError("Invalid start/end byte")

    command = packet[1]
    length = packet[2]
    data_bytes = packet[3:3+length]
    
    if len(data_bytes) != length:
        raise ValueError("Data length mismatch")

    return command, data_bytes.decode('utf-8')
