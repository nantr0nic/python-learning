import sys
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket

serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
# line below 'releases' the port immediately after script closes
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

try:
    serverSocket.bind(("0.0.0.0", serverPort))
    serverSocket.listen(1)
    print(f"Web server up and listening on port {serverPort}.")
    print("Press CTRL + C to shut down server.")

    while True:
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from: {addr}")

        try:
            message = connectionSocket.recv(1024).decode()
            # this guards against empty requests
            if not message:
                connectionSocket.close()
                continue

            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.readlines()

            # Send the HTTP Status Line (success in this case) and headers
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n".encode())
            # Send one blank line to signal the end of the headers
            connectionSocket.send("\r\n".encode())

            # Send the content of the requested file to the client
            for line in outputdata:
                connectionSocket.send(line.encode())

            # Final CRLF closes the message
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            print(f"Successfully served {filename}")

        except IOError:
            # Send response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send(
                "<html><body><h1>404 Not Found</h1></body></html>".encode()
            )
            connectionSocket.close()
            print(f"File {filename} not found.")

except KeyboardInterrupt:
    print("\nShutting down the server...")
    serverSocket.close()
    sys.exit()
