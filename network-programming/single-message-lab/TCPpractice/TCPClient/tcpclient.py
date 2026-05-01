import argparse
from socket import AF_INET, SOCK_STREAM, socket


def main():
    parser = argparse.ArgumentParser(
        description="A simple TCP client that sends an ASCII message to a TCP server."
    )

    parser.add_argument("hostname", help="The target hostname or IP address (e.g. google.com or 8.8.8.8)")
    parser.add_argument("message", help="The text message to include")

    args = parser.parse_args()

    run(args.hostname, args.message)

def run(hostname, message):
    serverName = hostname
    serverPort = 31173
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(message.encode())
    modifiedSentence = clientSocket.recv(1024)
    print(f"From server: {modifiedSentence.decode()}")
    clientSocket.close()

if __name__ == "__main__":
    main()
