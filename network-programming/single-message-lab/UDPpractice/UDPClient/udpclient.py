import argparse
from socket import socket, AF_INET, SOCK_DGRAM


def main():
    parser = argparse.ArgumentParser(
        description="A simple UDP client that sends an ASCII message to a UDP server."
    )

    parser.add_argument(
        "hostname",
        help="The target hostname or IP address (e.g. google.com or 8.8.8.8)",
    )
    parser.add_argument("message", help="The text message to include")

    args = parser.parse_args()

    run(args.hostname, args.message)


def run(hostname, message):
    serverName = hostname
    serverPort = 31173
    serverAddress = (serverName, serverPort)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message.encode(), serverAddress)
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    clientSocket.close()


if __name__ == "__main__":
    main()
