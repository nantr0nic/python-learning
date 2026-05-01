import argparse
import socket
import sys


def main():
    parser = argparse.ArgumentParser(description="A simple chat client.")
    parser.add_argument(
        "--host", type=str, help="Host to connect to (e.g. google.com or 8.8.8.8)"
    )
    parser.add_argument("--port", type=int, default=31173, help="Port to connect to")
    args = parser.parse_args()

    run(args.host, args.port)


def run(host, port):
    print("Welcome to the chat client! Please enter your name:")

    name: str = input()
    for char in name:
        if not char.isalnum() and char != "_":
            print(
                "Invalid name. Please use alphanumeric characters or underscores only."
            )
            return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(name.encode())
    name_response = client_socket.recv(1024).decode()

    if name_response == "name_rejected":
        print("Name taken! Restart and choose another one.")
        client_socket.close()
        sys.exit()
    elif name_response == "name_accepted":
        print(f"You've successfully connected! Welcome, {name}!")
    else:
        print("Undefined server response. Exiting!")
        client_socket.close()
        sys.exit()
        
    while True:
        message: str = input()
        client_socket.send(message.encode())
        


if __name__ == "__main__":
    main()
