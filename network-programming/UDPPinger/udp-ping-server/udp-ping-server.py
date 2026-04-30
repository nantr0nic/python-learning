import socket


def main():
    print("Starting UDP Pinger Server...")

    serverPort: int = 12000
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddress = ("localhost", serverPort)
    serverSocket.bind(serverAddress)
    print(f"Server is ready to receive pings on port {serverPort}")

    while True:
        message, clientAddress = serverSocket.recvfrom(1024)
        print(f"Received {message.decode()} from {clientAddress}")
        serverSocket.sendto("PONG".encode(), clientAddress)
        print("Pong returned!")


if __name__ == "__main__":
    main()
