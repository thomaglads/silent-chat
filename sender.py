import socket
from utils import build_packet, CMD_GREET, CMD_DATA, CMD_BYE

HOST = '127.0.0.1'  # Server address
PORT = 65432        # Server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[Client] Connected to server.")

    # Send a greeting
    s.sendall(build_packet(CMD_GREET, "Hello from client!"))

    # Send a data message
    s.sendall(build_packet(CMD_DATA, "This is a custom protocol test."))

    # Send a goodbye
    s.sendall(build_packet(CMD_BYE, "Closing connection now."))
