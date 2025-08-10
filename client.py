import socket
import threading
from utils import build_packet, parse_packet, CMD_GREET, CMD_DATA, CMD_BYE

username = input("Enter your username: ")

def handle_receive(sock):
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
            chunk = sock.recv(1024)
            if not chunk:
                print("[INFO] Connection closed by peer.")
                break
            buffer.extend(chunk)
            for pkt in process_buffer():
                if parse_packet(pkt):
                    sock.close()
                    return
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            break

def handle_send(sock):
    while True:
        msg = input()
        if msg.lower() in ("bye", "exit", "quit"):
            try:
                sock.sendall(build_packet(CMD_BYE, username))
            except OSError:
                pass
            sock.close()
            return  # stop immediately after closing
        else:
            try:
                sock.sendall(build_packet(CMD_DATA, f"{username}: {msg}"))
            except OSError:
                break

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 65432))
    print("[Client] Connected to server.")

    sock.sendall(build_packet(CMD_GREET, username))

    threading.Thread(target=handle_receive, args=(sock,), daemon=True).start()
    handle_send(sock)

