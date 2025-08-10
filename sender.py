import socket
from utils import build_packet, CMD_GREET, CMD_DATA, CMD_BYE

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[Client] Connected to server.")

    # Initial greeting
    s.sendall(build_packet(CMD_GREET, "Hello from client!"))

    while True:
        msg = input("You: ")
        if msg.lower() in ("bye", "exit", "quit"):
            s.sendall(build_packet(CMD_BYE, "Goodbye!"))
            break
        else:
            s.sendall(build_packet(CMD_DATA, msg))
