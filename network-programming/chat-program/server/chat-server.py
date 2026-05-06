import argparse
import asyncio

from include.server import Server


async def main():
    parser = argparse.ArgumentParser(description="A simple but functional chat server.")
    parser.add_argument(
        "--port",
        type=int,
        default=31173,
        help="The port to listen on (default: 31173)",
    )
    args = parser.parse_args()

    chat_server = Server(args.port)
    await chat_server.run()


if __name__ == "__main__":
    asyncio.run(main())
