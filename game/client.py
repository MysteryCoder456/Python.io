import socket
import threading
import pickle
from typing import Optional, Any


class ClientInterface:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.incoming_msg_queue = []
        self.conn_closed = False
        self.id = ""

        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()

    def queue_empty(self) -> bool:
        return self.incoming_msg_queue == []

    def pop_first_msg(self) -> Optional[Any]:
        try:
            return self.incoming_msg_queue.pop(0)
        except IndexError:
            pass

    def listen(self):
        buffer_size = 4096
        while not self.conn_closed:
            try:
                incoming_msg = self.socket.recv(buffer_size)

                if incoming_msg:
                    decoded = pickle.loads(incoming_msg)
                    self.incoming_msg_queue.append(decoded)
                else:
                    self.conn_closed = True

            except ConnectionResetError:
                self.conn_closed = True

        self.socket.close()

    def send(self, event):
        if not self.conn_closed:
            encoded = pickle.dumps(event)
            self.socket.sendall(encoded)
        else:
            raise OSError("Attempting to send data to a closed connection.")
