import socket
from utils import parse_packet, CMD_GREET, CMD_DATA, CMD_BYE

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Server] Listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"[Server] Connected by {addr}")
        while True:
            packet = conn.recv(1024)
            if not packet:
                break
            try:
                command, data = parse_packet(packet)
                if command == CMD_GREET:
                    print(f"[GREET] {data}")
                elif command == CMD_DATA:
                    print(f"[DATA] {data}")
                elif command == CMD_BYE:
                    print(f"[BYE] {data}")
                else:
                    print(f"[UNKNOWN] {data}")
            except ValueError as e:
                print(f"[Error] {e}")
