# utils/logger.py

from datetime import datetime

LOG_FILE = "darkmesh.log"

def log_event(event_type, ip, detail=""):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time_str}] [{event_type}] {ip} - {detail}\n")
