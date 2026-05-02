import socket
import threading
import datetime
import time


class Server:
    def __init__(self, port: int):
        self.port = port
        self.connected_clients = {}
        self.clients_dict_lock = threading.Lock()
        self.client_threads = []
        self.start_time = datetime.datetime.now()

    def run(self):
        """Main server loop"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(10)
        print(f"Chat server started. Accepting connections on port {self.port}")

        accept_thread = threading.Thread(target=self.accept_connections)
        self.client_threads.append(accept_thread)
        accept_thread.start()

        report_thread = threading.Thread(target=self.report_information)
        self.client_threads.append(report_thread)
        report_thread.start()

    def accept_connections(self):
        """Accepts incoming connections and handles them in separate threads."""
        while True:
            connection_socket, connection_address = self.server_socket.accept()
            
            handler_thread = threading.Thread(
                target=self.handle_client, args=(connection_socket, connection_address)
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

    def handle_client(self, connection_socket, connection_address):
        """Handles initial client connection (name setting) then message handling."""
        setting_name: bool = True
        while setting_name:
            receive_client_username = connection_socket.recv(1024).decode()
            with self.clients_dict_lock:
                if receive_client_username in self.connected_clients.values():
                    connection_socket.send("name_rejected".encode())
                    continue
                elif receive_client_username == "":
                    connection_socket.close()
                    return
                else:
                    self.connected_clients.update(
                        {connection_socket: receive_client_username}
                    )
                    response = f"name_accepted|{list(self.connected_clients.values())}"
                    connection_socket.send(response.encode())
                    setting_name = False
            self.broadcast_message(
                f"<<Server>> {receive_client_username} has joined the chat".encode()
            )

        self.handle_messages(connection_socket)

    def handle_messages(self, connection_socket):
        """Handles incoming messages from the client."""
        while True:
            try:
                receive_message = connection_socket.recv(1024)
                if receive_message == b"":
                    connection_socket.close()
                    with self.clients_dict_lock:
                        user = (
                            f"{self.connected_clients.get(connection_socket, 'A user')}"
                        )
                        del self.connected_clients[connection_socket]
                    self.broadcast_message(f"<<Server>> {user} has left!".encode())
                    break
                else:
                    self.broadcast_message(receive_message)
            except (ConnectionResetError, ConnectionAbortedError):
                connection_socket.close()
                with self.clients_dict_lock:
                    user = f"{self.connected_clients.get(connection_socket, 'A user')}"
                    del self.connected_clients[connection_socket]
                self.broadcast_message(f"<<Server>> {user} has left!".encode())
                break

    def broadcast_message(self, message):
        """Broadcasts a message to all connected clients."""
        clients_copy: list = []
        with self.clients_dict_lock:
            for client_socket in self.connected_clients.keys():
                clients_copy.append(client_socket)
        for client in clients_copy:
            try:
                client.send(message)
            except:
                pass
