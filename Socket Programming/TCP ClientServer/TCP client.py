import socket

def tcp_client(server_ip, server_port):
    """Connect to a TCP server and send messages."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))  
            print(f"[+] Connected to the server at {server_ip}:{server_port}")
            
            while True:
                message = input("Enter message to send (or type 'exit' to quit): ").strip()
                if message.lower() == 'exit':
                    print("[+] Exiting...")
                    break
                
                client_socket.sendall(message.encode('utf-8'))  
                data = client_socket.recv(1024) 
                print(f"[+] Server echoed: {data.decode('utf-8')}")
    except Exception as e:
        print(f"[!] Client error: {e}")

if __name__ == "__main__":
    SERVER_IP = input("Enter the server IP address: ").strip()
    SERVER_PORT = int(input("Enter the server port: "))
    
    tcp_client(SERVER_IP, SERVER_PORT)
