import socket
from utils import parse_packet

HOST = '127.0.0.1'
PORT = 65432

def process_buffer(buffer):
    """Process any complete packets from the buffer."""
    packets = []
    while True:
        # Need at least 4 bytes for START, CMD, LENGTH, END
        if len(buffer) < 4:
            break
        
        if buffer[0] != 0xAA:
            print("[WARN] Invalid start byte, discarding...")
            buffer.pop(0)
            continue

        length = buffer[2]
        total_len = 4 + length  # START + CMD + LEN + DATA + END

        if len(buffer) < total_len:
            # Not enough data yet
            break

        packet = buffer[:total_len]
        buffer = buffer[total_len:]
        packets.append(packet)

    return packets, buffer

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Server] Listening on {HOST}:{PORT}...")

    conn, addr = s.accept()
    with conn:
        print(f"[Server] Connected by {addr}")
        buffer = bytearray()

        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break

            buffer.extend(chunk)
            packets, buffer = process_buffer(buffer)

            for pkt in packets:
                parse_packet(pkt)
