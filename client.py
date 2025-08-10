import socket
import threading
from utils import parse_packet, build_packet, CMD_DATA, CMD_BYE, CMD_GREET

HOST = '127.0.0.1'
PORT = 65432

def handle_receive(sock):
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
        chunk = sock.recv(1024)
        if not chunk:
            print("[Client] Connection closed by server.")
            break
        buffer.extend(chunk)
        for pkt in process_buffer():
            parse_packet(pkt)

def handle_send(sock):
    # Send greeting first
    sock.sendall(build_packet(CMD_GREET, "Hello from client!"))
    while True:
        msg = input("Client: ")
        if msg.lower() in ("bye", "exit", "quit"):
            sock.sendall(build_packet(CMD_BYE, "Client says bye!"))
            break
        else:
            sock.sendall(build_packet(CMD_DATA, msg))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[Client] Connected to server.")

    recv_thread = threading.Thread(target=handle_receive, args=(s,), daemon=True)
    send_thread = threading.Thread(target=handle_send, args=(s,), daemon=False)

    recv_thread.start()
    send_thread.start()
