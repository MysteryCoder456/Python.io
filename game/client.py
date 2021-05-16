import socket
import threading
import pickle


class ClientInterface:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.incoming_msg_queue = []
        self.conn_closed = True

        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()

    def pop_first_msg(self):
        return self.incoming_msg_queue.pop(0)

    def listen(self):
        buffer_size = 4096
        while not self.conn_closed:
            incoming_msg = self.socket.recv(buffer_size)

            if incoming_msg:
                decoded = pickle.loads(incoming_msg)
                self.incoming_msg_queue.append(decoded)
            else:
                self.conn_closed = True
                self.socket.close()

    def send(self, event):
        if not self.conn_closed:
            encoded = pickle.dumps(event)
            self.socket.sendall(encoded)
        else:
            raise OSError("Attempting to send data to a closed connection.")
