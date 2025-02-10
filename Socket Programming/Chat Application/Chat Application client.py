import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("[!] Connection closed by the server.")
            break

def chat_client(server_ip, server_port, username):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"[+] Connected to the chat server at {server_ip}:{server_port}")
    
    client_socket.send(username.encode('utf-8'))
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    try:
        while True:
            message = input()
            if message.lower() == "exit":
                print("[+] Exiting chat...")
                client_socket.close()
                break
            client_socket.send(f"{username}: {message}".encode('utf-8'))
    except:
        print("[!] Connection error.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    SERVER_IP = input("Enter the server IP address: ").strip()
    SERVER_PORT = int(input("Enter the server port: "))
    USERNAME = input("Enter your username: ").strip()

    chat_client(SERVER_IP, SERVER_PORT, USERNAME)
