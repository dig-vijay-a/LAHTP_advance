import socket

def start_banner_server(host, port, banner_message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5) 
            print(f"[+] Server started on {host}:{port}")
            
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"[+] Connection from {client_address}")
                
                client_socket.sendall(banner_message.encode('utf-8'))
                print(f"[+] Banner sent to {client_address}")
                
                client_socket.close()
                
    except Exception as e:
        print(f"[!] Server error: {e}")

if __name__ == "__main__":
    HOST = "0.0.0.0"  
    PORT = 12345    
    BANNER = "Welcome to the Banner Grabber Server!\n"
    
    start_banner_server(HOST, PORT, BANNER)
