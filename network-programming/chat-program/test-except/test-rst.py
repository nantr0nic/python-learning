import argparse
import socket
import time


def main():
    parser = argparse.ArgumentParser(
        description="Force a TCP RST to test the chat server's exception handler."
    )
    parser.add_argument("host", type=str, help="Server hostname or IP")
    parser.add_argument("--port", type=int, default=31173, help="Server port")
    parser.add_argument("--name", type=str, default="TestBot", help="Name to register")
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, args.port))
    print(f"Connected. Sending name: {args.name}")
    s.send(args.name.encode())
    time.sleep(0.5)

    # Force RST on close instead of FIN
    s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, bytes([1, 0, 0, 0]))
    s.close()
    print("Socket closed with RST (abrupt disconnect)")


if __name__ == "__main__":
    main()
