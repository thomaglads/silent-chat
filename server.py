import socket
import threading
from utils import parse_packet, build_packet, CMD_DATA, CMD_BYE

HOST = '127.0.0.1'
PORT = 65432

def handle_receive(conn):
    buffer = bytearray()

    def process_buffer():
        nonlocal buffer
        packets = []
        while True:
            if len(buffer) < 4:
                break
            if buffer[0] != 0xAA:
                print("[WARN] Invalid start byte, discarding...")
                buffer.pop(0)
                continue
            length = buffer[2]
            total_len = 4 + length
            if len(buffer) < total_len:
                break
            packet = buffer[:total_len]
            buffer = buffer[total_len:]
            packets.append(packet)
        return packets

    while True:
        chunk = conn.recv(1024)
        if not chunk:
            print("[Server] Connection closed by client.")
            break
        buffer.extend(chunk)
        for pkt in process_buffer():
            parse_packet(pkt)

def handle_send(conn):
    while True:
        msg = input("Server: ")
        if msg.lower() in ("bye", "exit", "quit"):
            conn.sendall(build_packet(CMD_BYE, "Server says bye!"))
            break
        else:
            conn.sendall(build_packet(CMD_DATA, msg))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Server] Listening on {HOST}:{PORT}...")

    conn, addr = s.accept()
    print(f"[Server] Connected by {addr}")

    recv_thread = threading.Thread(target=handle_receive, args=(conn,), daemon=True)
    send_thread = threading.Thread(target=handle_send, args=(conn,), daemon=False)

    recv_thread.start()
    send_thread.start()
