import subprocess
import re

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

    devices = []
    pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:]{17})\s+(.+)"
    for line in result.stdout.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            ip, mac, vendor = match.groups()
            devices.append({
                "ip": ip,
                "mac": mac,
                "vendor": vendor
            })

    return devices


# TEST amaçlı çalıştır
if __name__ == "__main__":
    cihazlar = scan_network()
    for c in cihazlar:
        print(f"{c['ip']} - {c['mac']} - {c['vendor']}")
