import socket
import threading
from utils import build_packet, parse_packet, CMD_GREET, CMD_DATA, CMD_BYE

username = input("Enter your username: ")

def handle_receive(conn):
    buffer = bytearray()

    def process_buffer():
        nonlocal buffer
        packets = []
        while True:
            if len(buffer) < 4:
                break
            if buffer[0] != 0xAA:
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
        try:
            chunk = conn.recv(1024)
            if not chunk:
                print("[INFO] Connection closed by peer.")
                break
            buffer.extend(chunk)
            for pkt in process_buffer():
                if parse_packet(pkt):
                    conn.close()
                    return
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            break

def handle_send(conn):
    while True:
        msg = input()
        if msg.lower() in ("bye", "exit", "quit"):
            conn.sendall(build_packet(CMD_BYE, username))
            conn.close()
            break
        else:
            conn.sendall(build_packet(CMD_DATA, f"{username}: {msg}"))

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 65432))
    server.listen(1)
    print("[Server] Listening on 127.0.0.1:65432...")

    conn, addr = server.accept()
    print(f"[Server] Connected by {addr}")

    conn.sendall(build_packet(CMD_GREET, username))

    threading.Thread(target=handle_receive, args=(conn,), daemon=True).start()
    handle_send(conn)
