import socket
import threading
import json
import queue

#TCP connection setup stuff
class Network:
    def __init__(self):
        self.client = None
        self.server = None
        self.messages = queue.Queue()
        self.send_lock = threading.Lock()
        self.connected = False
        self.running = False
#Host Game Functionality 
    def host(self, port=5555):
        print("HOST CALLED")
        self.running = True
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        self.server.bind(("0.0.0.0", port))
        print("BIND SUCCESS: ", self.server.getsockname())
        self.server.listen(1)
        print("LISTENING ON: ", port)

        print("SERVER OBJECT:", self.server)

        print("RUNNING:", self.running)

        threading.Thread(
            target=self._accept_connection,
            daemon=True
        ).start()
    def _accept_connection(self):
        print("WAITING FOR CONNECTION")
        try:
            client, address = self.server.accept()
            print("CLIENT CONNECTED: ", address)
            if not self.running:
                client.close()
                return
            self.client = client
            self.connected = True
            print("HOST CONNECTED FLAG SET")
            self.messages.put({"type": "connected", "address": address})
            self._receive_loop()
            print("CONNECTED MESSAGE QUEUED")
        #except OSError
        except Exception as error:
            print("ACCEPT ERROR:", repr(error))
            if self.running:
                self.messages.put({"type": "error", "message": "Unable to accept connection"})

# Join Game Functionality 
    def join(self, host_ip, port=5555):
        print("JOIN CALLED")
        self.running = True
        print("STARTING THREAD")
        threading.Thread(
            target=self._connect,
            args=(host_ip, port),
            daemon=True
        ).start()
    def _connect(self, host_ip, port):
        print("ENTERED CONNECT")
        try:
            print("ATTEMPTING CONNECTION: ", host_ip, port)
            client = socket.create_connection((host_ip, port), timeout=5)
            client.settimeout(None)
            if not self.running:
                client.close()
                return
            self.client = client
            self.connected = True
            print("CLIENT CONNECTED FLAG SET")
            self.messages.put({"type": "connected"})
            self._receive_loop()
        except OSError as error:
            print("CONNECT ERROR: ", repr(error))
            if self.running:
                self.messages.put({"type": "error", "message": str(error)})
# Sending Messages
    def send(self, data):
        if not self.connected or self.client is None:
            return False
        try:
            message = json.dumps(data) + "\n"
            with self.send_lock:
                self.client.sendall(message.encode("utf-8"))
            return True
        except OSError:
            self.messages.put({
                "type": "error",
                "message": "Failed to send message."
            })
            self.close()
            return False
# Receiving Messages
    def _receive_loop(self):
        buffer = ""
        try:
            while self.running:
                data = self.client.recv(4096)
                if not data:
                    break
                buffer += data.decode("utf-8")
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    if message:
                        self.messages.put({
                            "type": "message",
                            "data": json.loads(message)
                        })
        except (OSError, json.JSONDecodeError) as error:
            if self.running:
                self.messages.put({
                    "type": "error",
                    "message": str(error)
                })
        finally:
            self.connected = False
            if self.running:
                self.messages.put({
                    "type": "disconnected"
                })
# Sent Message Retrieval 
    def poll(self):
        received = []
        while not self.messages.empty():
            received.append(self.messages.get())
        return received
# Closing the Connection 
    def close(self):
        self.running = False
        self.connected = False
        if self.client:
            try:
                self.client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.client.close()
            self.client = None
        if self.server:
            self.server.close()
            self.server = None