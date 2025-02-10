import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port (host,port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  
            result = s.connect_ex((host, port))
            if result == 0:
                print(f"[+] Port {port} is OPEN")
            else:
                pass
                
    except Exception as e:
        print(f"Error: {e}")

def port_scanner(host, start_port, end_port, threads):
    print(f"Scanning {host} from port {start_port} to {end_port}...\n")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, host, port)

host=input("Enter the IP address: ")
start_port=int(input("Enter the starting port: "))
end_port=int(input("Enter the ending port: "))
no_of_thread=int(input("Enter the no of thread: "))
port_scanner(host,start_port,end_port,threads=no_of_thread)
