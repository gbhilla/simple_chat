from socket import *
from threading import Thread

HOST = '0.0.0.0'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

def accept_incoming_connections(server_socket, addresses, clients):
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = server_socket.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,clients)).start()


def handle_client(client, clients):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(clients, bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(clients, msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(clients, bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(clients, msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


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