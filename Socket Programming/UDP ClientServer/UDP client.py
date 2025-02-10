import socket

def udp_client(server_ip, server_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            print(f"[+] Connected to UDP server at {server_ip}:{server_port}")
            
            while True:
                message = input("Enter message to send (or type 'exit' to quit): ").strip()
                if message.lower() == 'exit':
                    print("[+] Exiting...")
                    break
                
                client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))
                
                data, server_address = client_socket.recvfrom(1024)
                print(f"[+] Server echoed: {data.decode('utf-8')}")
    except Exception as e:
        print(f"[!] Client error: {e}")

if __name__ == "__main__":
    SERVER_IP = input("Enter the server IP address: ").strip()
    SERVER_PORT = int(input("Enter the server port: "))
    
    udp_client(SERVER_IP, SERVER_PORT)
