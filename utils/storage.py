# utils/storage.py

import json

DEVICE_INFO_PATH = "device_info.json"

def remove_device(ip):
    try:
        with open(DEVICE_INFO_PATH, "r") as f:
            data = json.load(f)
        if ip in data:
            del data[ip]
            with open(DEVICE_INFO_PATH, "w") as f:
                json.dump(data, f, indent=2)
            return True
        else:
            return False
    except Exception as e:
        print("Kaldırma hatası:", e)
        return False
