import subprocess
import os

def send_device_notification(device):
    ip = device.get("ip", "Bilinmiyor")
    mac = device.get("mac", "Bilinmiyor")
    message = f"Yeni cihaz bağlandı: {ip} ({mac})"
    
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"

    logo_path = os.path.abspath("darkmesh_logo.png")
    
    subprocess.Popen([
        "notify-send", "-i", logo_path,
        "DarkMesh - Yeni Cihaz Tespit Edildi", message
    ], env=env)
