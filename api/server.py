import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Üst dizini modül yoluna ekle

from flask import Flask, jsonify, request
from scanner import scan_network
import json

app = Flask(__name__)

DEVICE_INFO_FILE = "device_info.json"

# Cihaz bilgilerini oku
def load_device_info():
    if os.path.exists(DEVICE_INFO_FILE):
        try:
            with open(DEVICE_INFO_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# Cihaz bilgilerini kaydet
def save_device_info(info):
    try:
        with open(DEVICE_INFO_FILE, "w") as f:
            json.dump(info, f, indent=2)
    except Exception as e:
        print("Cihaz bilgileri kaydedilemedi:", e)

# Ağ cihazlarını getir
@app.route("/devices", methods=["GET"])
def get_devices():
    raw_devices = scan_network()
    info_map = load_device_info()

    result = []
    for dev in raw_devices:
        ip = dev["ip"]
        extra = info_map.get(ip, {"name": "", "type": guess_device_type(dev["vendor"])})
        result.append({
            "ip": ip,
            "mac": dev["mac"],
            "vendor": dev["vendor"],
            "self": dev["self"],
            "name": extra["name"],
            "type": extra["type"]
        })

    return jsonify(result)

# Belirli bir cihaza isim ve tür etiketle
@app.route("/label", methods=["POST"])
def label_device():
    data = request.json
    ip = data.get("ip")
    name = data.get("name", "")
    dtype = data.get("type", "")

    if not ip:
        return jsonify({"error": "IP adresi gerekli"}), 400

    info = load_device_info()
    info[ip] = {
        "name": name,
        "type": dtype
    }
    save_device_info(info)
    return jsonify({"success": True})


# Otomatik tahmin fonksiyonu (mobilde de kullanılabilir)
def guess_device_type(vendor):
    vendor = vendor.lower()
    if any(keyword in vendor for keyword in ["apple", "samsung", "xiaomi", "huawei", "oppo", "vivo", "realme"]):
        return "Akıllı Telefon"
    elif "espres" in vendor or "sonoff" in vendor or "tuya" in vendor:
        return "IoT Cihazı"
    elif "tplink" in vendor or "asus" in vendor or "netgear" in vendor or "zyxel" in vendor:
        return "Router"
    elif any(k in vendor for k in ["intel", "amd", "dell", "lenovo", "hp"]):
        return "Bilgisayar"
    return "Bilinmiyor"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
