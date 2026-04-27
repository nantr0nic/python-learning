import socket


def main() -> None:
    host = "127.0.0.1"
    port = 31173

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"[SERVER] Listening on {host}:{port}...")

    try:
        conn, addr = server_socket.accept()
        print(f"[SERVER] Connection from {addr}")

        data = conn.recv(1024).decode()
        print(f"[SERVER] Received: {data}")

        response = data.upper()
        conn.sendall(response.encode())
        print(f"[SERVER] Sent: {response}")

        conn.close()
    finally:
        server_socket.close()
        print("[SERVER] Closed")


if __name__ == "__main__":
    main()
