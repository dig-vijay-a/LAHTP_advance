import socket

def udp_server(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((host, port))
            print(f"[+] UDP Server started on {host}:{port}")
            
            while True:
                data, client_address = server_socket.recvfrom(1024) 
                print(f"[+] Received from {client_address}: {data.decode('utf-8')}")
                
                server_socket.sendto(data, client_address)
                print(f"[+] Echoed back to {client_address}")
    except Exception as e:
        print(f"[!] Server error: {e}")

if __name__ == "__main__":
    HOST = "0.0.0.0"  
    PORT = 12345      
    
    udp_server(HOST, PORT)
