import socket
import threading
from cryptography.fernet import Fernet

# Generate and store an encryption key (should be securely distributed to clients)
encryption_key = Fernet.generate_key()  # This will generate a valid key
print(f"Encryption Key: {encryption_key.decode()}")

cipher = Fernet(encryption_key)

# Server setup
HOST = '127.0.0.1'  # Localhost
PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

# Broadcast messages to all connected clients
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            encrypted_msg = cipher.encrypt(message)
            client.send(encrypted_msg)

# Handle individual client connections
def handle_client(client):
    while True:
        try:
            encrypted_message = client.recv(1024)
            if not encrypted_message:
                break
            message = cipher.decrypt(encrypted_message).decode('utf-8')
            broadcast(message.encode('utf-8'), sender=client)
        except:
            index = clients.index(client)
            clients.remove(client)
            username = usernames[index]
            usernames.remove(username)
            print(f"[INFO] {username} disconnected.")
            break

# Accept new client connections
def accept_connections():
    print("[SERVER] Server is running...")
    while True:
        client, addr = server.accept()
        print(f"[INFO] Connection established with {addr}")

        # Receive username
        username = cipher.decrypt(client.recv(1024)).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(f"[INFO] {username} joined the chat!")
        broadcast(f"{username} joined the chat!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

accept_connections()
