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

    run(args.hostname, args.port, args.pings)


def run(hostname, port=12000, pings=10):
    serverAddress = (hostname, port)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in range(pings):
        clientSocket.settimeout(1.0)
        pingStartTime = datetime.now()
        clientSocket.sendto(f"PING {i}".encode(), serverAddress)

        while True:
            try:
                message, _ = clientSocket.recvfrom(1024)
                messageSeq = int(message.decode().split()[-1])
                if messageSeq == i:
                    pingEndTime = datetime.now()
                    elapsedMS = (pingEndTime - pingStartTime).total_seconds() * 1000
                    print(f"({i}) {message.decode()} - RTT: {elapsedMS:.2f}ms")
                    break
            except socket.timeout:
                print(f"({i}) Request timed out.")
                break

    clientSocket.close()


if __name__ == "__main__":
    main()
