# utils/networktools.py

import subprocess
import socket
import json
import os

# JSON'dan port açıklamaları yükleniyor
PORT_DESCRIPTIONS_PATH = os.path.join(os.path.dirname(__file__), "port_descriptions.json")
try:
    with open(PORT_DESCRIPTIONS_PATH, "r") as f:
        PORT_DESCRIPTIONS = json.load(f)
except Exception:
    PORT_DESCRIPTIONS = {}

def ping_device(ip, count=4):
    import platform
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(["ping", param, str(count), ip], stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Ping başarısız:\n{e.output}"


def scan_open_ports(ip, ports=range(20, 1025)):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            if result == 0:
                description = PORT_DESCRIPTIONS.get(str(port), "Bilinmiyor")
                open_ports.append((port, description))
    return open_ports
