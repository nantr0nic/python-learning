# Simple TCP Chat Program
This is a simple TCP chat program that allows multiple clients to connect to a server and chat with each other.
It is a learner project to practice network programming in Python. It relies on TCP sockets to establish connections and exchange data between clients.

The client makes use of threading to handle incoming/outgoing messages and also uses
prompt_toolkit for the interactive command line interface.

The server makes use of asyncio to handle concurrent connections.

There's nothing too fancy going on here, but some simple commands are available to the client similar to IRC clients:
- /join <channel>: join a channel
- /list: list all channels
- /users: list all users and what channels they are in
- /quit: quit the chat program
- /help: list all available commands

test-except is a script that sends an RST to the server and verifies that the server properly handles connection exceptions.