# Simple TCP Chat Program - Server

## Usage:
```
pyton3 server.py (optional): <port> (default is 31173)
```

While running, the server reports server uptime and the number of connected clients. It will also remove channels that have been empty for 60 seconds. It does *not* handle/remove idle clients.

## The Server
The server code is in ```server.py```. 
It is instantiated in ```main()``` and runs the server loop that goes like:

- accepts connections and hand connections to ```handle_client()``` -> 

- on success, client connections become represented as a ```User``` object -> 

- announce the new user to all clients and put them in #general -> 

- start the chat loop by handing that user to ```handle_messages()``` -> 

- receive and handle messages from the client (including slash commands)... messages are broadcast to a channel through ```broadcast_to_channel()```.

---

Users are ultimately a set of asyncio streams (```asyncio.StreamReader```, ```asyncio.StreamWriter```), a unique username, and the channel they are in. 