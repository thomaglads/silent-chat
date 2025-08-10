from datetime import datetime

def parse_packet(packet: bytes) -> bool:
    """
    Parse a packet and print info.
    Returns True if CMD_BYE was received (to trigger close).
    """
    if len(packet) < 4:
        print("[WARN] Packet too short")
        return False

    start, cmd, length = packet[0], packet[1], packet[2]
    payload = packet[3:3+length]
    checksum = packet[3+length]

    if start != 0xAA:
        print("[WARN] Invalid start byte")
        return False

    if (sum(packet[:3+length]) & 0xFF) != checksum:
        print("[WARN] Invalid checksum")
        return False

    text = payload.decode('utf-8', errors='replace')
    timestamp = datetime.now().strftime("%H:%M")

    if cmd == CMD_GREET:
        print(f"[{timestamp}] * {text} joined the chat *")
    elif cmd == CMD_DATA:
        if ": " in text:
            username, msg = text.split(": ", 1)
            print(f"[{timestamp}] {username}: {msg}")
        else:
            print(f"[{timestamp}] {text}")
    elif cmd == CMD_BYE:
        print(f"[{timestamp}] * {text} left the chat *")
        return True
    else:
        print(f"[{timestamp}] [UNKNOWN CMD {cmd}] {text}")

    return False

