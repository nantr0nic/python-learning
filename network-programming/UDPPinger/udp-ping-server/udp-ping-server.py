import random
import socket


def main():
    print("Starting UDP Pinger Server...")

    serverPort: int = 12000
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddress = ("0.0.0.0", serverPort)
    serverSocket.bind(serverAddress)
    print(f"Server is ready to receive pings on port {serverPort}")

    while True:
        message, clientAddress = serverSocket.recvfrom(1024)
        messageData = message.decode()
        messageSeq = int(messageData.split()[-1])
        print(f"Received {messageData} from {clientAddress}")
        if messageSeq == 0:
            packetToDrop = random.randint(1, 9)
        if messageSeq == packetToDrop:
            print(f"(Simulation) Dropping packet #({messageSeq})")
            continue
        else:
            serverSocket.sendto(f"PONG {messageSeq}".encode(), clientAddress)
            print("Pong returned!")


if __name__ == "__main__":
    main()
