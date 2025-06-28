import json
import time
import subprocess
from datetime import datetime

def run_scheduler():
    while True:
        try:
            now = datetime.now().strftime("%H:%M")

            # schedule.json dosyasını oku
            with open("schedule.json", "r") as f:
                schedules = json.load(f)

            for entry in schedules:
                ip = entry["ip"]
                start = entry["start"]
                end = entry["end"]

                if start <= now <= end:
                    # IP zaten bloklanmamışsa, blokla
                    subprocess.run(["sudo", "iptables", "-C", "OUTPUT", "-d", ip, "-j", "DROP"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    # Eğer kural yoksa ekle
                    if subprocess.call(["sudo", "iptables", "-C", "OUTPUT", "-d", ip, "-j", "DROP"],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-d", ip, "-j", "DROP"])

                else:
                    # Bu zaman aralığında değilse unblock et
                    subprocess.call(["sudo", "iptables", "-D", "OUTPUT", "-d", ip, "-j", "DROP"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        except Exception as e:
            print("Zamanlayıcı hatası:", e)

        time.sleep(5) 