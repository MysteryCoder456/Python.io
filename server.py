import threading
import uuid
import socket
import pickle

from game.network_events import *

ADDR, PORT = "0.0.0.0", 6969
BUFFER_SIZE = 4096
SERVER_ACTIVE = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

snakes: dict[str, Snake] = {}
clients: dict[str, socket.socket] = {}


def send(client: socket.socket, event):
    if client in list(clients.values()):
        encoded = pickle.dumps(event)
        client.sendall(encoded)
    else:
        print("[CLIENT ERROR] Attempting to send data to an unregistered client.")


def send_raw(client: socket.socket, encoded: bytes):
    if client in list(clients.values()):
        client.sendall(encoded)
    else:
        print("[CLIENT ERROR] Attempting to send data to an unregistered client.")


def send_all(event, ignore_client_uid: str = None):
    encoded = pickle.dumps(event)
    for uid in clients:
        if uid != ignore_client_uid:
            send_raw(clients[uid], encoded)


def listen(uid: str, client_socket: socket.socket):
    while SERVER_ACTIVE:
        try:
            incoming_msg = client_socket.recv(BUFFER_SIZE)

            if incoming_msg:
                decoded = pickle.loads(incoming_msg)

                if isinstance(decoded, RegisterWithServerEvent):
                    # Add snake to internal roster
                    snakes[uid] = decoded.snake

                    # Assign an ID to the client
                    msg_assign_id = AssignIDEvent(uid)
                    send(client_socket, msg_assign_id)
                    print(f"[CLIENT {uid}] Registered!")

                    # Notify all players about new player
                    msg_add_snake = AddSnakeEvent(uid, decoded.snake)
                    send_all(msg_add_snake)

                elif isinstance(decoded, SnakeUpdateEvent):
                    snakes[uid] = decoded.snake
                    msg_snake_update = SnakeUpdateEvent(uid, decoded.snake)
                    send_all(msg_snake_update, uid)
            else:
                break

        except ConnectionResetError:
            break

    # Client has disconnected
    client_socket.close()
    del clients[uid]
    print(f"[CLIENT {uid}] Disconnected!")


def new_connection():
    new_client, addr = s.accept()

    # Assign an ID to new client
    new_id = uuid.uuid4().hex
    clients[new_id] = new_client

    # Start listen thread
    client_listen_thread = threading.Thread(
        target=listen, args=[new_id, new_client], daemon=True
    )
    client_listen_thread.start()

    # Notify client that their connection has been accepted
    msg_conn_accept = ConnectionAcceptEvent()
    send(new_client, msg_conn_accept)

    print(f"New client connected from {addr}")


def main():
    global SERVER_ACTIVE

    s.bind((ADDR, PORT))
    s.listen()
    print("[SERVER] Started!")
    SERVER_ACTIVE = True

    while True:
        new_connection()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        print("[SERVER] Closing...")
        SERVER_ACTIVE = False
