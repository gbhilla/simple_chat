# server.py
import socket
import threading
import time

clients = {}
addresses = {}

def handle_client(client_socket, addr):
    nickname = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = nickname
    addresses[client_socket] = addr
    print(f"[{time.strftime('%H:%M', time.localtime())}] {nickname} connected from {addr}")
    broadcast_message_to_all(f"[{time.strftime('%H:%M', time.localtime())}] {nickname} connected")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Received from {nickname}: {message}")  # Add this line
            if message.startswith('/sendimage'):
                send_image(client_socket, message.split()[1])
            else:
                broadcast_message_to_all(f"[{time.strftime('%H:%M', time.localtime())}] {nickname}: {message}")
        except:
            remove_client(client_socket)
            break

def remove_client(client_socket):
    nickname=clients[client_socket]
    del clients[client_socket]
    del addresses[client_socket]
    client_socket.close()
    broadcast_message_to_all(f"[{time.strftime('%H:%M', time.localtime())}] {nickname} exited")
def broadcast_message_to_all(message):
    for client_socket in clients:
        client_socket.send(message.encode('utf-8'))
def send_image(client_socket, image_name):
    try:
        with open(image_name, 'rb') as image_file:
            image_data = image_file.read()
            for client_socket in clients:
                client_socket.send(f"[Image] {image_name}".encode('utf-8'))
                client_socket.send(image_data)
    except FileNotFoundError:
        client_socket.send("[Error] Image not found".encode('utf-8'))

def start_server():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on {}:{}".format(host, port))

    while True:
        client_socket, addr = server_socket.accept()
        client_socket.send("Enter your nickname:".encode('utf-8'))
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
