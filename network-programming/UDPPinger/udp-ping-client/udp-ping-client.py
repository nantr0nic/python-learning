import argparse
import socket
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description='This is a UDP Ping Client that sends a "PING" message to a server.'
    )

    parser.add_argument(
        "hostname",
        help="The target hostname or IP address (e.g. google.com or 8.8.8.8)",
    )
    parser.add_argument(
        "port", type=int, help="The port number to use (default: 12000)"
    )
    parser.add_argument(
        "pings", type=int, help="The number of pings to send (default: 10)"
    )

    args = parser.parse_args()

    run(args.hostname, args.port)


def run(hostname, port=12000, pings=10):
    serverName = hostname
    serverPort: int = port
    serverAddress = (serverName, serverPort)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.sendto("PING".encode(), serverAddress)

    for i in range(pings):
        pingStartTime = datetime.now()
        clientSocket.sendto("PING".encode(), serverAddress)
        message, serverAddress = clientSocket.recvfrom(1024)
        pingEndTime = datetime.now()
        elapsedMS = (pingEndTime - pingStartTime).total_seconds() * 1000
        print(f"{message.decode()} - RTT: {elapsedMS}ms")

    clientSocket.close()


if __name__ == "__main__":
    main()
