from socket import *


def main():
    print("Weclome to a simple TCP server!")

    serverPort = 31173
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1) # 1 is max number of queued connections
    print("The server is ready to receive.")

    while True:
        connectionSocket, addr = serverSocket.accept()
        if addr:
            print(f"Connection from: {addr}")
        sentence = connectionSocket.recv(1024).decode()
        print(f"Received: {sentence}")
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())
        print(f"Sent: {capitalizedSentence}")
        connectionSocket.close()

if __name__ == "__main__":
    main()
