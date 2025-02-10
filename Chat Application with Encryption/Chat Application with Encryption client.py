import socket
import threading
from tkinter import *
from cryptography.fernet import Fernet

# Encryption key (must match the server's key)
encryption_key = b"Syz04xLYG7RvNjuTqvLXVDg-xPSfJbUB_hvCB_QT5Vw="
cipher = Fernet(encryption_key)

# Client setup
HOST = '127.0.0.1'
PORT = 12345
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# Send username to server
username = input("Enter your username: ")
client.send(cipher.encrypt(username.encode('utf-8')))

# GUI Class
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Chat App")
        
        self.chat_area = Text(self.root, bg="lightgrey", state=DISABLED)
        self.chat_area.pack(padx=10, pady=5)
        
        self.msg_entry = Entry(self.root, width=50)
        self.msg_entry.pack(padx=10, pady=5)
        
        self.send_button = Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)
        
        # Start receiving thread
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        message = self.msg_entry.get()
        self.msg_entry.delete(0, END)
        encrypted_msg = cipher.encrypt(message.encode('utf-8'))
        client.send(encrypted_msg)
        self.display_message(f"You: {message}")

    def display_message(self, message):
        self.chat_area.config(state=NORMAL)
        self.chat_area.insert(END, f"{message}\n")
        self.chat_area.config(state=DISABLED)

    def receive_messages(self):
        while True:
            try:
                encrypted_msg = client.recv(1024)
                message = cipher.decrypt(encrypted_msg).decode('utf-8')
                self.display_message(message)
            except:
                break

# Run the app
root = Tk()
app = ChatApp(root)
root.mainloop()
