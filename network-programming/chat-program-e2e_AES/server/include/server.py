import asyncio
import datetime
import sys
import os


class User:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, name: str
    ):
        self.user_reader: asyncio.StreamReader = reader
        self.user_writer: asyncio.StreamWriter = writer
        self.name: str = name
        self.channel: str = ""


class Server:
    def __init__(self, port: int):
        self.port: int = port
        self.server: asyncio.Server | None = None
        self.start_time = datetime.datetime.now()

        # Dictionary of clients (writers) {writer: User}
        self.connected_clients: dict[asyncio.StreamWriter, User] = {}

        # Always have a default channel named general, each channel
        # just has a list if its members in a set
        self.chat_channels = {"general": {"members": set(), "salt": os.urandom(16)}}

        # Server commands
        self.commands = {
            "list": self.handle_list_channels,
            "users": self.handle_list_users,
            "join": self.handle_join_channel,
            "quit": self.handle_quit,
        }

    async def run(self):
        """Run the main server"""
        self.server = await asyncio.start_server(
            self.handle_client, "0.0.0.0", self.port
        )
        async with self.server:
            if self.server.is_serving():
                print(f"Chat server started. Accepting connections on port {self.port}")
            else:
                print("An error occurred starting the server. Exiting.")
                return
            asyncio.create_task(self.report_information())
            asyncio.create_task(self.cleanup_channels())
            await self.server.serve_forever()

    async def report_information(self):
        """Reports server information to the console."""
        while True:
            count = len(self.connected_clients)
            uptime = datetime.datetime.now() - self.start_time
            print(f"\rServer uptime: {uptime} // Connected clients: {count}", end="")
            await asyncio.sleep(5)

    async def handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """Handles client connection, User creation, then passes to message handler."""
        setting_name: bool = True
        while setting_name:
            receive_data = await reader.read(1024)
            receive_client_username = receive_data.decode()
            if any(
                user.name.lower() == receive_client_username.lower()
                for user in self.connected_clients.values()
            ):
                writer.write("name_rejected".encode())
                await writer.drain()
                continue
            elif receive_client_username == "":
                writer.close()
                return
            else:
                user = User(reader, writer, receive_client_username)
                self.connected_clients.update({writer: user})
                writer.write("name_accepted".encode())
                await writer.drain()
                setting_name = False

        await self.broadcast_global_message(
            f"<<Server>> {user.name} has joined the server!".encode()
        )
        await self.handle_join_channel(user, "general")
        await self.handle_messages(user)

    async def handle_messages(self, user: User):
        """Handles incoming messages from the User."""
        while True:
            try:
                receive_data = await user.user_reader.read(1024)
                receive_message = receive_data.decode()
                # empty byte data signals a disconnection
                if receive_data == b"":
                    await self.remove_user(user)
                    break
                elif receive_message.startswith("/"):
                    parts = receive_message.strip().split(maxsplit=1)
                    command = parts[0][1:].lower()  # /join -> join
                    arg = parts[1] if len(parts) > 1 else ""

                    handler = self.commands.get(command)
                    if handler:
                        await handler(user, arg)
                        if command == "quit":
                            break
                    else:
                        user.user_writer.write(
                            f"<<Server>> Unknown command: {command}".encode()
                        )
                        await user.user_writer.drain()
                else:
                    formatted = f"<{user.name}> {receive_message}"
                    await self.broadcast_to_channel(formatted.encode(), user.channel)
            except (ConnectionError, asyncio.IncompleteReadError) as e:
                print(f"\nConnection error: {e}", file=sys.stderr)
                print()
                await self.remove_user(user)
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}", file=sys.stderr)
                print()
                await self.remove_user(user)
                break

    async def broadcast_global_message(self, message):
        """Broadcasts a message to all connected clients."""
        clients = list(self.connected_clients.keys())
        for client in clients:
            try:
                client.write(message)
                await client.drain()
            except:
                pass

    async def broadcast_to_channel(self, message, channel: str):
        """Broadcasts a message to users in a channel."""
        members = list(self.chat_channels[channel]["members"])
        for member in members:
            try:
                member.user_writer.write(message)
                await member.user_writer.drain()
            except:
                pass

    async def handle_list_channels(self, user: User, arg: str = ""):
        """Lists all channels."""
        channels = ", ".join(self.chat_channels.keys())
        user.user_writer.write(f"<<Server>> Channels: {channels}".encode())
        await user.user_writer.drain()

    async def handle_list_users(self, user: User, arg: str = ""):
        """Lists all users in the server."""
        users = ", ".join(
            [
                f"{client.name} (#{client.channel})"
                for client in self.connected_clients.values()
            ]
        )
        user.user_writer.write(f"<<Server>> Users: {users}".encode())
        await user.user_writer.drain()

    async def handle_join_channel(self, user: User, arg: str):
        """Handles a User joining a channel."""
        if not arg:
            user.user_writer.write(
                "<<Server>> Provide a channel name! Usage: /join #channel".encode()
            )
            await user.user_writer.drain()
            return

        channel = arg.lstrip("#").lower()
        if not channel:
            user.user_writer.write(
                "<<Server>> Provide a channel name! Usage: /join #channel".encode()
            )
            await user.user_writer.drain()
            return
        if not all(char.isalnum() or char == "_" for char in channel):
            user.user_writer.write(
                "<<Server>> Invalid name. Please use alphanumeric characters or underscores only.".encode()
            )
            await user.user_writer.drain()
            return

        # Check if channel exists, if it doesn't, make it. If it does, switch user to that.
        old_channel: str = user.channel

        if channel not in self.chat_channels:
            self.chat_channels[channel] = {"members": set()}
            user.user_writer.write(
                f"<<Server>> #{channel} doesn't exist. Creating it!\n".encode()
            )
        if old_channel:
            self.chat_channels[user.channel]["members"].discard(user)
            await self.broadcast_to_channel(
                f"<<Server>> {user.name} has left #{old_channel}!".encode(), old_channel
            )

        self.chat_channels[channel]["members"].add(user)
        user.channel = channel
        user.user_writer.write(
            f"<<Server>> You're now in #{channel}. Welcome!\n".encode()
        )
        await user.user_writer.drain()
        await self.broadcast_to_channel(
            f"<<Server>> {user.name} has joined #{channel}!".encode(), channel
        )

    async def handle_quit(self, user: User, arg: str = ""):
        """Handle a user leaving the server."""
        user.user_writer.write(b"<<Server>> You are leaving the server. Take it easy!")
        await user.user_writer.drain()
        await self.remove_user(user)

    async def remove_user(self, user: User):
        """Remove a user from the server gracefully."""
        del self.connected_clients[user.user_writer]
        self.chat_channels[user.channel]["members"].discard(user)
        user.user_writer.close()
        await self.broadcast_global_message(
            f"<<Server>> {user.name} has disconnected!".encode()
        )

    async def cleanup_channels(self):
        """Remove empty channels periodically."""
        while True:
            to_delete = []
            for channel_name, channel_data in self.chat_channels.items():
                if not channel_data["members"] and channel_name != "general":
                    to_delete.append(channel_name)
            for name in to_delete:
                del self.chat_channels[name]
            await asyncio.sleep(60)
