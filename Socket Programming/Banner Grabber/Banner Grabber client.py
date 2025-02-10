import socket

def grab_banner(target_ip, target_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)  
            client_socket.connect((target_ip, target_port))  

            banner = client_socket.recv(1024).decode('utf-8')  
            print(f"[+] Banner received from {target_ip}:{target_port}: {banner}")
    except socket.timeout:
        print(f"[!] Connection to {target_ip}:{target_port} timed out.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    target_ip = input("Enter the server IP address: ").strip()
    target_port = int(input("Enter the server port: "))
    
    grab_banner(target_ip, target_port)
