import argparse
import socket
import sys
import threading
from datetime import datetime

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.styles import Style

server_running = threading.Event()

HELP_TEXT = (
    " >> /list - List all channels\n"
    " >> /users - List all users\n"
    " >> /join <channel> - Join a channel\n"
    " >> /quit - Quit the server\n"
    " >> /help - Show this help message"
)


def main():
    parser = argparse.ArgumentParser(description="A simple chat client.")
    parser.add_argument(
        "host", type=str, help="Host to connect to (e.g. google.com or 8.8.8.8)"
    )
    parser.add_argument("--port", type=int, default=31173, help="Port to connect to")
    args = parser.parse_args()
    run(args.host, args.port)


def connect_to_server(host, port):
    """Connect silently.  Prints an error and exits only on failure."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        server_running.set()
        return client_socket
    except Exception as e:
        print(
            f" >> Connection failed: {e}\nTry again or connect to a different server."
        )
        sys.exit()


def receive_messages(client_socket, output_buffer, app, buffer_lock):
    """Runs in a background thread.  Reads from the socket and pushes
    every message into the shared output buffer.  *buffer_lock* protects
    concurrent access from the UI thread (key-bindings)."""
    while server_running.is_set():
        try:
            data = client_socket.recv(1024)
            if data == b"":
                with buffer_lock:
                    output_buffer.insert_text(" >> The server disconnected!\n")
                    output_buffer.cursor_position = len(output_buffer.text)
                server_running.clear()
                app.invalidate()
                break

            message = data.decode()
            timestamp = datetime.now().strftime("%H:%M:%S")
            with buffer_lock:
                output_buffer.insert_text(f"({timestamp}) {message}\n")
                output_buffer.cursor_position = len(output_buffer.text)
            app.invalidate()
        except OSError as e:
            with buffer_lock:
                output_buffer.insert_text(
                    f" >> A connection error occurred: {e}\n"
                )
                output_buffer.cursor_position = len(output_buffer.text)
            server_running.clear()
            app.invalidate()
            break


def is_valid_name(name):
    return name and all(char.isalnum() or char == "_" for char in name)


def run(host, port):
    client_socket = connect_to_server(host, port)

    # --- Buffers ---
    output_buffer = Buffer(multiline=True)
    input_buffer = Buffer(multiline=False)
    buffer_lock = threading.Lock()

    def write_output(text):
        """Thread-safe helper: insert *text* into the output buffer."""
        with buffer_lock:
            output_buffer.insert_text(text)
            output_buffer.cursor_position = len(output_buffer.text)

    # --- Name-negotiation state (mutated by key handlers) ---
    naming = True
    name = ""

    # --- Key bindings ---
    kb = KeyBindings()

    @kb.add("enter")
    def send_handler(event):
        nonlocal naming, name
        text = input_buffer.text
        input_buffer.reset()
        if not text:
            return

        # ---- Phase 1: pick a name ----
        if naming:
            if not is_valid_name(text):
                write_output(
                    "Invalid name. Use alphanumeric characters or underscores only.\n"
                )
                write_output(" >> Please enter your name: \n")
                return

            try:
                client_socket.send(text.encode())
                client_socket.settimeout(5.0)
                response = client_socket.recv(1024).decode()
                client_socket.settimeout(None)
            except OSError as e:
                write_output(f" >> Connection error: {e}\n")
                server_running.clear()
                event.app.exit()
                return

            if response == "name_rejected":
                write_output(" >> Name taken!\n")
                write_output(" >> Please enter your name: \n")
                return
            elif response == "name_accepted":
                name = text
                naming = False
                write_output(f" >> Welcome, {name}!\n\n")

                # Handshake done -- start the receive thread now.
                recv_thread = threading.Thread(
                    target=receive_messages,
                    args=(client_socket, output_buffer, event.app, buffer_lock),
                    daemon=True,
                )
                recv_thread.start()
                return
            else:
                write_output(" >> Undefined server response. Exiting!\n")
                server_running.clear()
                event.app.exit()
                return

        # ---- Phase 2: normal chat ----
        if text == "/quit":
            try:
                client_socket.send(b"/quit")
            except OSError:
                pass
            write_output(" >> Leaving! << \n")
            server_running.clear()
            event.app.exit()
            return

        if text == "/help":
            write_output(HELP_TEXT + "\n")
            return

        try:
            client_socket.send(text.encode())
        except OSError as e:
            write_output(f" >> An error occurred: {e}\n")
            server_running.clear()
            event.app.exit()

    @kb.add("c-c")
    def quit_handler(event):
        try:
            client_socket.send(b"/quit")
        except OSError:
            pass
        write_output("\n >> Leaving! << \n")
        server_running.clear()
        event.app.exit()

    # --- Layout ---
    output_control = BufferControl(buffer=output_buffer, focusable=False)
    input_control = BufferControl(buffer=input_buffer)

    root_container = HSplit(
        [
            Window(content=output_control, wrap_lines=True, dont_extend_width=False),
            Window(height=1, char="\u2500", style="class:separator"),
            Window(
                height=1,
                content=input_control,
                style="class:input-field",
            ),
        ]
    )

    layout = Layout(root_container, focused_element=input_control)
    style = Style.from_dict(
        {
            "separator": "fg:#555555",
            "input-field": "bg:#1e1e1e",
        }
    )

    app = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        full_screen=True,
    )

    # Seed the output buffer *before* the UI starts its event loop.
    write_output(f" >> Connected to {host}:{port}!\n")
    write_output("Here are a list of available commands:\n")
    write_output(HELP_TEXT + "\n\n")
    write_output(" >> Please enter your name: \n")

    # Blocking call -- runs prompt_toolkit on the main thread.
    app.run()

    # --- Cleanup (after app exits) ---
    server_running.clear()
    try:
        client_socket.close()
    except OSError:
        pass
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
