from datetime import datetime
from socket import *
from threading import Thread

HOST = '0.0.0.0'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

import traceback


def accept_incoming_connections(server_socket, addresses, clients):
    """Sets up handling for incoming clients."""
    while not server_socket._closed:
        try:
            client, client_address = server_socket.accept()
            current_time = datetime.now().strftime("%H:%M")
            client.send(bytes("["+current_time+"] Greetings from the cave!\n", "utf8"))
            addresses[client] = client_address
            Thread(target=handle_client, args=(client, clients)).start()
        except OSError as e:
            if server_socket._closed:
                break
            else:
                print("Error accepting incoming connection:", e)
                traceback.print_exc()
                continue
    server_socket.close()



def handle_client(client, clients):
    """Handles a single client connection."""
    current_time = datetime.now().strftime("%H:%M")
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = f"Welcome {name}! If you ever want to quit, type {{quit}} to exit."
    client.send(bytes(welcome, "utf8"))
    msg = f"{name} has joined the chat!"
    broadcast(clients, bytes(msg, "utf8"))
    clients[client] = name
    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                raise ConnectionResetError("Client requested disconnect.")
            if not msg:
                raise ConnectionResetError("Client disconnected unexpectedly.")
            broadcast(clients, msg, name + ": ")
        except ConnectionResetError:
            del clients[client]
            client.close()
            msg = f"{name} has left the chat."
            broadcast(clients, bytes(msg, "utf8"))
            break



def broadcast(clients, msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    current_time = datetime.now().strftime("%H:%M")
    for sock in clients:
        #if bytes("{quit}", "utf8") in msg:
        #    sock.send(bytes(prefix, "utf8") + msg)
        #else:
        sock.send(bytes("["+current_time+"]"+prefix, "utf8") + msg)


def create_server_socket():
    """
    Thios function returns serevr socket
    :return: server_socket
    """
    try:
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(ADDR)
    except Exception as err:
        print(err)
        exit(999)
    return server_socket


def main():
    server_socket = create_server_socket()
    clients = {}
    addresses = {}
    server_socket.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections,args=(server_socket, addresses, clients))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server_socket.close()


if __name__ == "__main__":
    main()