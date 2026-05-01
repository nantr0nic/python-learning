import os
import socket
import sys


def main():
    if len(sys.argv) <= 1:
        print("Usage: python web-proxy-server.py <server_port>")
        sys.exit(2)

    # Make the cache dir if it doesn't exist already
    os.makedirs("./cache", exist_ok=True)

    proxy_port: int = int(sys.argv[1])

    # This is the proxy's socket to connect to the client/browser
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(("0.0.0.0", proxy_port))
    proxy_socket.listen(5)
    print(f"Proxy server listening on port {proxy_port}...")

    while True:
        client_socket, client_addr = proxy_socket.accept()
        print(f"Accepted connection from: {client_addr}")
        handle_client(client_socket)
        client_socket.close()


def handle_client(client_socket):
    # Receive the HTTP request from the client
    request_data = client_socket.recv(4096).decode()
    # Guard against empty requests
    if not request_data:
        return

    print(f"Request:\n{request_data}")

    # Extract the requested URL from the first line: "GET /path HTTP/1.1"
    request_line = request_data.split("\r\n")[0]
    parts = request_line.split()
    # protect against malformed requests (though rare?)
    if len(parts) < 2:
        return

    # parts[0] = "GET", parts[1] = "/path" or "http://...", etc.
    url = parts[1]

    # If its a full URL like "http://example.com/page", extract just "/page"
    # Because a browser knows if its using a proxy it'll use the absolute url
    # instead of just the page (like a normal HTTP request)
    if url.startswith("http://"):
        url_parts = url.split("/")
        path = "/" + "/".join(url_parts[3:])
    # If its just a path like "/page", use it directly
    else:
        path = url

    print(f"Requested path: {path}")

    # Extract the hostname from the Host header
    request_hostname = None
    for header_line in request_data.split("\r\n"):
        if header_line.lower().startswith("host:"):
            request_hostname = header_line.split()[1]
            break

    # Guard against missing Host header
    if not request_hostname:
        print("Request missing Host header, ignoring.")
        return

    # Build cache path
    cache_path = f"./cache/{request_hostname}/{path.lstrip('/')}"

    # Try to serve from cache first
    try:
        with open(cache_path, "r") as cache_file:
            cached_content = cache_file.read()
            client_socket.send(cached_content.encode())
        print("Served from cache.")

    except FileNotFoundError:
        # Not in cache — fetch from the remote server
        webHostAddr = (request_hostname, 80)
        web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        web_socket.connect(webHostAddr)
        # need to re-write the first line of the HTTP request...
        # cuz browser uses absolute URL when it knows its using a proxy
        rewritten_line = f"{parts[0]} {path} {parts[2]}"
        rest_of_request = request_data.split("\r\n", 1)[1]
        rewritten_request = f"{rewritten_line}\r\n{rest_of_request}"
        try:
            print("Fetching from remote server...")
            web_socket.send(rewritten_request.encode())
            response_data = b""
            while True:
                chunk = web_socket.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            status_line = response_data.split(b"\r\n")[0].decode()
            status_code = int(status_line.split()[1])
            if status_code == 200:
                client_socket.send(response_data)
                # save to cache...(full response, headers + body)
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                with open(cache_path, "w") as file:
                    file.write(response_data.decode())
                print("Saved data to cache")
            else:
                # forward all other codes but don't cache them
                client_socket.send(response_data)
        except Exception as e:
            print(f"Error fetching from remote server: {e}")
            client_socket.send(
                b"HTTP/1.0 502 Bad Gateway\r\n"
                b"\r\n"
                b"<html><body><h1>502 Bad Gateway</h1></body></html>"
            )
        finally:
            web_socket.close()


if __name__ == "__main__":
    main()
