import socket
import threading
from queue import Queue

# Target info
target = input("Enter target IP or hostname: ")
port_range = input("Enter port range (e.g., 1-1024): ")

start_port, end_port = map(int, port_range.split('-'))

# Threading setup
thread_count = 100
q = Queue()

# To store results
open_ports = []
closed_ports = []

def tcp_scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((target, port))
        print(f"[+] TCP Port {port} is OPEN")
        open_ports.append(port)
        s.close()
    except:
        closed_ports.append(port)

def udp_scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.sendto(b"ScannerTest", (target, port))
        s.recvfrom(1024)
        print(f"[+] UDP Port {port} is OPEN or FILTERED")
        open_ports.append(port)
    except:
        closed_ports.append(port)

def worker():
    while not q.empty():
        port = q.get()
        tcp_scan(port)
        udp_scan(port)
        q.task_done()

def run_scanner():
    print(f"\n[*] Scanning {target} from port {start_port} to {end_port}")
    for port in range(start_port, end_port + 1):
        q.put(port)

    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()

    print("\nScan complete.")
    print(f"\nOpen Ports: {open_ports}")
    print(f"Closed Ports: {len(closed_ports)} skipped for brevity.")

if __name__ == "__main__":
    run_scanner()
