import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    print(f"[+] New connection from {client_address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
    except:
        pass
    finally:
        print(f"[-] Connection closed from {client_address}")
        clients.remove(client_socket)
        client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def chat_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[+] Chat server started on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    HOST = "0.0.0.0"  
    PORT = 12345      
    chat_server(HOST, PORT)
