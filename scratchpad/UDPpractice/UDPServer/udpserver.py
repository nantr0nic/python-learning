from socket import *

def main():
    print("Welcome to a simple UDP server!")

    serverPort = 31173
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Server is ready to receive messages...")

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        print(f"Received message from {clientAddress}: {message.decode()}. Sent back: {modifiedMessage}")

if __name__ == "__main__":
    main()
