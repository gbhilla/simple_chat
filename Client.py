from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

HOST = "127.0.0.1"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

chat_window = None
my_msg = None

def submit_name():
    name = name_entry.get()
    client_socket.send(bytes(name, "utf8"))
    if name.strip() != "":
        print("name exists")
        name_dialog.destroy()
        create_chat_window(name)

def create_chat_window(name):
    global chat_window, my_msg
    chat_window = tk.Tk()
    my_msg = tk.StringVar()
    scrollbar = tk.Scrollbar(chat_window)
    message_list = tk.Listbox(chat_window, width=50, height=10, yscrollcommand=scrollbar.set)
    chat_label = tk.Label(chat_window, text="\nWelcome, " + name + "!")
    chat_window.title("The chat of "+name)
    chat_label.pack()
    message_list.pack()
    message_entry = tk.Entry(chat_window, width=50, textvariable=my_msg)
    message_entry.pack()

    send_button = tk.Button(chat_window, text="Send", command=lambda: send_message(my_msg))
    send_button.pack()
    message_entry.bind("<Return>", lambda event: send_message(my_msg))
    receive_thread = Thread(target=receive, args=(message_list,))
    receive_thread.start()
    chat_window.mainloop()

def send_message(msg_var):
    global chat_window
    msg = msg_var.get()
    msg_var.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        chat_window.quit()

def receive(message_list):
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            # Split the received message into separate lines
            lines = msg.split("\n")
            for line in lines:
                if line.strip() != "":
                    message_list.insert(tk.END, line)
        except OSError:  # Possibly client has left the chat.
            break

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Create the dialog window
name_dialog = tk.Tk()
name_dialog.title("Enter Your Name")

name_label = tk.Label(name_dialog, text="Enter your name:")
name_label.pack()

name_entry = tk.Entry(name_dialog, width=50)
name_entry.pack()

submit_button = tk.Button(name_dialog, text="Submit", command=submit_name)
submit_button.pack()
name_entry.bind("<Return>", lambda event: submit_name())
name_dialog.mainloop()