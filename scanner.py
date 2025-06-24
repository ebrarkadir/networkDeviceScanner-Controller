import subprocess
import re
import socket
from netaddr import EUI

def get_own_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def get_own_mac(interface="enp4s0"):
    try:
        with open(f"/sys/class/net/{interface}/address") as f:
            return f.read().strip()
    except:
        return None

def lookup_vendor(mac):
    try:
        return EUI(mac).oui.registration().org
    except:
        return "Unknown Vendor"

def scan_network(interface="enp4s0"):
    try:
        result = subprocess.run(
            ["sudo", "arp-scan", "--interface", interface, "--localnet"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Hata oluştu:", e)
        return []

    own_ip = get_own_ip()
    own_mac = get_own_mac(interface)
    own_vendor = lookup_vendor(own_mac) if own_mac else None

    devices = []
    pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:]{17})\s+(.+)"
    for line in result.stdout.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            ip, mac, vendor = match.groups()
            devices.append({
                "ip": ip,
                "mac": mac,
                "vendor": lookup_vendor(mac),
                "self": ip == own_ip
            })

    if own_ip and own_mac and all(d["ip"] != own_ip for d in devices):
        devices.append({
            "ip": own_ip,
            "mac": own_mac,
            "vendor": own_vendor,
            "self": True
        })

    return devices

if __name__ == "__main__":
    cihazlar = scan_network()
    for c in cihazlar:
        label = " <-- BU CİHAZ" if c["self"] else ""
        print(f"{c['ip']} - {c['mac']} - {c['vendor']}{label}")
