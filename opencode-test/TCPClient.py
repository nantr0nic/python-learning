import socket


def main() -> None:
    host = "127.0.0.1"
    port = 31173
    message = "hello from tcp client"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[CLIENT] Connected to {host}:{port}")

    client_socket.sendall(message.encode())
    print(f"[CLIENT] Sent: {message}")

    response = client_socket.recv(1024).decode()
    print(f"[CLIENT] Received: {response}")

    client_socket.close()
    print("[CLIENT] Closed")


if __name__ == "__main__":
    main()
