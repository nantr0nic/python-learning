import argparse
import socket
import sys
import threading
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="A simple chat client.")
    parser.add_argument(
        "host", type=str, help="Host to connect to (e.g. google.com or 8.8.8.8)"
    )
    parser.add_argument("--port", type=int, default=31173, help="Port to connect to")
    args = parser.parse_args()

    run(args.host, args.port)


def run(host, port):
    threads = []
    server_running = threading.Event()
    print(" >> Welcome to the chat client! << ")

    # Connect to server
    client_socket = connect_to_server(host, port, server_running)

    # Negotiate name with server
    name = set_name(client_socket, server_running)

    # Start message receive thread
    receive_thread = threading.Thread(
        target=receive_messages, args=(client_socket, server_running)
    )
    threads.append(receive_thread)
    receive_thread.start()

    # Start message send thread
    send_thread = threading.Thread(
        target=send_message, args=(client_socket, name, server_running)
    )
    threads.append(send_thread)
    send_thread.start()

    for thread in threads:
        thread.join()


def connect_to_server(host, port, server_running) -> socket.socket:
    print(f" >> Connecting to server: {host}:{port}")
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        server_running.set()
    except Exception as e:
        client_socket.close()
        print(
            f" >> Connection failed: {e}\nTry again or connect to a different server."
        )
        sys.exit()
    print(" >> Connected!\nHere are a list of available commands:")
    print(
        " >> /list - List all channels\n >> /users - List all users\n >> \
        /join <channel> - Join a channel\n >> /quit - Quit the server"
    )
    return client_socket


def set_name(client_socket, server_running) -> str:
    name: str = ""
    setting_name: bool = True
    while setting_name:
        print("\n >> Please enter your name:")
        name: str = input()
        if not all(char.isalnum() or char == "_" for char in name):
            print(
                "Invalid name. Please use alphanumeric characters or underscores only."
            )
            continue

        client_socket.send(name.encode())
        name_response = client_socket.recv(1024).decode()

        if name_response.split("|")[0] == "name_rejected":
            print(" >> Name taken!")
            continue
        elif name_response.split("|")[0] == "name_accepted":
            print(f" >> You've successfully connected! Welcome, {name}!")
            print(f" >> Current users: {name_response.split('|')[1:]}")
            setting_name = False
        else:
            print(" >> Undefined server response. Exiting!")
            client_socket.close()
            server_running.clear()
            sys.exit()
    return name


def receive_messages(client_socket, server_running):
    while server_running.is_set():
        try:
            recv_message = client_socket.recv(1024).decode()
            if recv_message == "":
                client_socket.close()
                print(" >> The server disconnected!")
                server_running.clear()
            else:
                print("(" + datetime.now().strftime("%H:%M:%S") + ") " + recv_message)
        except socket.error as e:
            client_socket.close()
            print(f" >> A connection error occurred: {e}")
            server_running.clear()


def send_message(client_socket, name, server_running):
    while server_running.is_set():
        message: str = input()
        if message == "/quit":
            client_socket.send(b"/quit")
            server_running.clear()
            print(" >> Leaving! << ")
            break
        out_message = f"<{name}> {message}"
        try:
            client_socket.send(out_message.encode())
        except Exception as e:
            print(f" >> An error occurred: {e}")
            continue


if __name__ == "__main__":
    main()
