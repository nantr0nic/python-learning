import argparse

from include.server import Server


def main():
    parser = argparse.ArgumentParser(description="A simple but functional chat server.")
    parser.add_argument(
        "--port",
        type=int,
        default=31173,
        help="The port to listen on (default: 31173)",
    )
    args = parser.parse_args()

    chat_server = Server(args.port)
    chat_server.run()

    for thread in chat_server.client_threads:
        thread.join()


if __name__ == "__main__":
    main()
