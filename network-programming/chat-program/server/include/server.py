import datetime
import socket
import threading
import time


class User:
    def __init__(self, connection_socket, name):
        self.user_socket: socket.socket = connection_socket
        self.name: str = name
        self.channel: str = ""


class Server:
    def __init__(self, port: int):
        self.port: int = port
        self.client_threads: list = []
        self.start_time = datetime.datetime.now()

        # Dictionary of clients {client_socket: User}
        self.connected_clients = {}
        self.clients_dict_lock = threading.Lock()

        # Always have a default channel named general, each channel
        # just has a list if its members in a set
        self.chat_channels = {"general": {"members": set()}}
        self.channels_dict_lock = threading.Lock()

    def run(self):
        """Main server loop"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(10)
        print(f"Chat server started. Accepting connections on port {self.port}")

        # Start connecting-accepting thread
        accept_thread = threading.Thread(target=self.accept_connections)
        self.client_threads.append(accept_thread)
        accept_thread.start()

        # Start console-reporting thread
        report_thread = threading.Thread(target=self.report_information)
        self.client_threads.append(report_thread)
        report_thread.start()

    def accept_connections(self):
        """Accepts incoming connections and handles them in separate threads."""
        while True:
            connection_socket, connection_address = self.server_socket.accept()

            handler_thread = threading.Thread(
                target=self.handle_client, args=(connection_socket,)
            )
            self.client_threads.append(handler_thread)
            handler_thread.start()

    def report_information(self):
        """Reports server information to the console."""
        while True:
            time.sleep(5)
            with self.clients_dict_lock:
                count = len(self.connected_clients)
            uptime = datetime.datetime.now() - self.start_time
            print(f"\rServer uptime: {uptime} // Connected clients: {count}", end="")

    def handle_client(self, connection_socket):
        """Handles client connection, User creation, then passes to message handler."""
        setting_name: bool = True
        while setting_name:
            receive_client_username = connection_socket.recv(1024).decode()
            with self.clients_dict_lock:
                # if receive_client_username in [user.name for user in self.connected_clients.values()]:
                if any(
                    user.name == receive_client_username
                    for user in self.connected_clients.values()
                ):
                    connection_socket.send("name_rejected".encode())
                    continue
                elif receive_client_username == "":
                    connection_socket.close()
                    return
                else:
                    user = User(connection_socket, receive_client_username)
                    self.connected_clients.update({connection_socket: user})
                    response = f"name_accepted|{list(user.name for user in self.connected_clients.values())}"
                    connection_socket.send(response.encode())
                    setting_name = False

        self.add_user_to_channel(user, "general")

        self.broadcast_global_message(
            f"<<Server>> {user.name} has joined the server!".encode()
        )
        self.handle_messages(user)

    def handle_messages(self, user: User):
        """Handles incoming messages from the User."""
        while True:
            try:
                receive_message = user.user_socket.recv(1024)
                # empty byte data signals a disconnection
                if receive_message == b"":
                    self.remove_user(user)
                    break
                else:
                    self.broadcast_to_channel(receive_message, user.channel)
            except (ConnectionResetError, ConnectionAbortedError):
                self.remove_user(user)
                break

    def broadcast_global_message(self, message):
        """Broadcasts a message to all connected clients. Locks clients dict."""
        clients_copy: list = []
        with self.clients_dict_lock:
            for client_socket in self.connected_clients.keys():
                clients_copy.append(client_socket)
        for client in clients_copy:
            try:
                client.send(message)
            except:
                pass

    def broadcast_to_channel(self, message, channel: str):
        """Broadcasts a message to users in a channel. Locks channels dict."""
        channel_members: list = []
        with self.channels_dict_lock:
            for member in self.chat_channels[channel]["members"]:
                channel_members.append(member)
        for member in channel_members:
            try:
                member.user_socket.send(message)
            except:
                pass

    def add_user_to_channel(self, user: User, channel: str):
        """Add a User to a channel. Locks channels dict."""
        # Check if channel exists, if it doesn't, make it. If it does, switch user to that.
        old_channel: str = user.channel
        created_channel: bool = False
        with self.channels_dict_lock:
            if channel not in self.chat_channels:
                created_channel = True
                self.chat_channels[channel] = {"members": set()}
            if old_channel:
                self.chat_channels[user.channel]["members"].discard(user)
            self.chat_channels[channel]["members"].add(user)

        # This is messy but trying to minimize network I/O that happens inside the lock
        if created_channel:
            user.user_socket.send(
                f"<<Server>> #{channel} doesn't exist. Creating it!".encode()
            )
        if old_channel:
            self.broadcast_to_channel(
                f"<<Server>> {user.name} has left {old_channel}!".encode(), old_channel
            )
        user.channel = channel
        user.user_socket.send(f"<<Server>> You're now in #{channel}. Welcome!".encode())

    def remove_user(self, user: User):
        """Remove a user from the server gracefully. Locks clients and channels dicts."""
        with self.clients_dict_lock:
            del self.connected_clients[user.user_socket]
        with self.channels_dict_lock:
            self.chat_channels[user.channel]["members"].discard(user)
        user.user_socket.close()
        self.broadcast_global_message(
            f"<<Server>> {user.name} has disconnected!".encode()
        )
