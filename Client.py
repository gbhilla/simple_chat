from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from datetime import datetime

class ChatClient:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.chat_window = None
        self.my_msg = None
        self.name_dialog = None  # Added name_dialog attribute
        self.name_entry = None  # Added name_entry attribute

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

    def submit_name(self):
        name = self.name_entry.get()
        self.client_socket.send(bytes(name, "utf8"))
        if name.strip() != "":
            self.name_dialog.destroy()
            self.create_chat_window(name)

    def create_chat_window(self, name):
        self.chat_window = tk.Tk()
        self.my_msg = tk.StringVar()
        scrollbar = tk.Scrollbar(self.chat_window)
        message_list = tk.Listbox(self.chat_window, width=50, height=10, yscrollcommand=scrollbar.set)
        chat_label = tk.Label(self.chat_window, text="\nWelcome, " + name + "!")
        self.chat_window.title("The chat of " + name)
        chat_label.pack()
        message_list.pack()
        message_entry = tk.Entry(self.chat_window, width=50, textvariable=self.my_msg)
        message_entry.pack()

        send_button = tk.Button(self.chat_window, text="Send", command=lambda: self.send_message(self.my_msg))
        send_button.pack()
        message_entry.bind("<Return>", lambda event: self.send_message(self.my_msg))
        self.chat_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        receive_thread = Thread(target=self.receive, args=(message_list,))
        receive_thread.start()
        self.chat_window.mainloop()

    def send_message(self, msg_var):
        msg = msg_var.get()
        msg_var.set("")  # Clears input field.
        if msg == "{quit}":
            try:
                self.client_socket.close()
                self.chat_window.quit()
            except OSError:
                print("The connection has already been closed.")
        try:
            self.client_socket.send(bytes(msg, "utf8"))
        except OSError:
            print("Failed to send the message.")




    def on_closing(self, event=None):
        print("on_closing")
        self.my_msg.set("{quit}")
        self.send_message(self.my_msg)
    def receive(self, message_list):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                lines = msg.split("\n")
                for line in lines:
                    if line.strip() != "":
                        message_list.insert(tk.END, line)
            except OSError:
                break

if __name__ == "__main__":
    client = ChatClient("127.0.0.1", 33000)

    client.name_dialog = tk.Tk()  # Updated variable name
    client.name_dialog.title("Enter Your Name")

    name_label = tk.Label(client.name_dialog, text="Enter your name:")
    name_label.pack()

    client.name_entry = tk.Entry(client.name_dialog, width=50)  # Updated variable name
    client.name_entry.pack()

    submit_button = tk.Button(client.name_dialog, text="Submit", command=client.submit_name)
    submit_button.pack()
    client.name_entry.bind("<Return>", lambda event: client.submit_name())
    client.name_dialog.mainloop()
