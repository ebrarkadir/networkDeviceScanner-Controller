# utils/networktools.py

import subprocess
import socket

def ping_device(ip):
    try:
        output = subprocess.check_output(["ping", "-c", "4", ip], stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Ping başarısız: {e.output}"

def scan_open_ports(ip, ports=range(20, 1025)):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports
