import os
import psutil
import platform
import getpass
import subprocess

# --- User Privilege Analysis ---
def check_user_privileges():
    user = getpass.getuser()
    is_admin = os.getuid() == 0 if platform.system() != "Windows" else os.getenv("USERNAME") == "Administrator"
    print(f"[+] Current User: {user}")
    print(f"[+] Admin Privileges: {'Yes' if is_admin else 'No'}")

# --- File and Directory Permissions ---
def scan_file_permissions(directory="/etc" if platform.system() != "Windows" else "C:\\Windows\\System32"):
    print(f"\n[+] Scanning permissions in directory: {directory}")
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                if os.access(filepath, os.W_OK):
                    print(f"[!] Writable File Detected: {filepath}")
    except PermissionError:
        print(f"[!] Permission denied while accessing: {directory}")

# --- Process Analysis ---
def analyze_running_processes():
    print("\n[+] Analyzing running processes...")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            if proc.info['username'] == 'root' or 'Administrator' in proc.info['username']:
                print(f"[!] Process with elevated privileges detected: PID={proc.info['pid']}, Name={proc.info['name']}")
        except psutil.AccessDenied:
            print(f"[!] Access denied to process: PID={proc.info['pid']}")
        except psutil.NoSuchProcess:
            continue

# --- Registry Analysis (Windows Only) ---
def check_registry_entries():
    if platform.system() != "Windows":
        print("\n[-] Registry analysis is only supported on Windows.")
        return
    print("\n[+] Checking registry for suspicious entries...")
    try:
        output = subprocess.check_output("reg query HKLM /f 'admin' /s", shell=True, text=True)
        print("[!] Suspicious Registry Entries:\n", output)
    except subprocess.CalledProcessError:
        print("[!] No suspicious entries found in the registry.")

# --- Log Analysis ---
def analyze_logs(log_file="/var/log/auth.log" if platform.system() != "Windows" else "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx"):
    print(f"\n[+] Analyzing log file: {log_file}")
    try:
        with open(log_file, 'r') as file:
            logs = file.readlines()
            for line in logs:
                if "authentication failure" in line or "escalation" in line:
                    print(f"[!] Potential escalation attempt found: {line.strip()}")
    except FileNotFoundError:
        print(f"[!] Log file not found: {log_file}")
    except PermissionError:
        print(f"[!] Permission denied while accessing: {log_file}")

# --- Main Tool ---
def main():
    print("=== Local Privilege Escalation Detection Tool ===")
    choose=input("Choices: \n\t1) check_user_privileges\n\t2)scan_file_permissions\n\t3)analyze_running_processes\n\t4)check_registry_entries\n\t5)analyze_logs\n\t\n\tEnter your choice: ")
    try:
        choose=int(choose)
    except:
        print('Wrong Choice')
    if choose==1:
        check_user_privileges()
    elif choose==2:
        scan_file_permissions()
    elif choose==3:
        analyze_running_processes()
    elif choose==4:
        check_registry_entries()
    elif choose==5:
        analyze_logs()

if __name__ == "__main__":
    main()
