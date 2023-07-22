# client.py
import socket
import threading
import tkinter as tk
from tkinter import simpledialog, filedialog
from PIL import Image, ImageTk

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("[Image]"):
                image_name = message.split()[1]
                image_data = client_socket.recv(1024)
                with open(f"received_{image_name}", 'wb') as image_file:
                    image_file.write(image_data)
                display_image(f"received_{image_name}")
            else:
                text_area.config(state=tk.NORMAL)  # Enable text_area for editing
                text_area.insert('end', message + '\n')  # Display the received message
                text_area.see('end')
                text_area.config(state=tk.DISABLED)  # Disable text_area again
        except OSError:
            break
    client_socket.close()
    root.quit()

def display_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((100, 100))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    label.image = photo
    text_area.window_create('end', window=label)
    text_area.insert('end', '\n')
    text_area.see('end')

def send(event=None):
    message = my_msg.get()
    my_msg.set("")
    print(f"Sending message: {message}")  # Add this line
    client_socket.send(message.encode('utf-8'))
    if message == "/sendimage":
        file_path = filedialog.askopenfilename()
        if file_path:
            client_socket.send(f"/sendimage {file_path}".encode('utf-8'))

def on_closing(event=None):
    my_msg.set("/exit")
    send()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    nickname = simpledialog.askstring("Nickname", "Enter your nickname:")
    client_socket.send(nickname.encode('utf-8'))

    root = tk.Tk()
    root.title("Chat")
    text_area = tk.Text(root, wrap='word', width=500, height=400)
    text_area.pack(expand='yes', fill='both')
    text_area.config(state=tk.DISABLED)
    scrollbar = tk.Scrollbar(text_area)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    my_msg = tk.StringVar()
    entry_field = tk.Entry(root, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.bind("<KP_Enter>", send)  # For Enter key on numeric keypad
    entry_field.pack(fill='both')

    root.protocol("WM_DELETE_WINDOW", on_closing)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    root.geometry("500x500")
    root.mainloop()