import socket

def tcp_server(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)  
            print(f"[+] TCP Server started on {host}:{port}")
            
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"[+] Connection from {client_address}")
                
                with client_socket:
                    while True:
                        data = client_socket.recv(1024) 
                        if not data:
                            break
                        
                        print(f"[+] Received from {client_address}: {data.decode('utf-8')}")
                        client_socket.sendall(data)
                        print(f"[+] Echoed back to {client_address}")
    except Exception as e:
        print(f"[!] Server error: {e}")

if __name__ == "__main__":
    HOST = "0.0.0.0"  
    PORT = 12345      
    
    tcp_server(HOST, PORT)
