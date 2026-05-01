import argparse
import socket

def main():
    parser = argparse.ArgumentParser(
        description="A simple but functional chat server."
    )
    parser.add_argument(
        "port",
        type=int,
        default=31173,
        help="The port to listen on (default: 31173)",
    )
    args = parser.parse_args()

    run(args.port)

def run(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(10) # max 10 queued connections
    print(f"Chat server is running. Accepting connections on port {server_port}")

    # Move these variables later
    # Do we want a dictionary of connection_socket and name?
    client_names = []

    while True:
        connection_socket, connection_address = server_socket.accept()
        first_message = connection_socket.recv(1024).decode()
        if first_message in client_names:
            connection_socket.send("name_rejected".encode())
            connection_socket.close()
            break
        else:
            client_names.append(first_message)
            connection_socket.send("name_accepted".encode())
        connection_socket.close()
        

if __name__ == "__main__":
    main()