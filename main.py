import tkinter as tk
from tkinter import ttk
from scanner import scan_network
import json
import os
import multiprocessing
import subprocess

def start_api():
    subprocess.Popen(["python3", "api/server.py"])  # Arka planda Flask API'yi başlat

class NetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ağ Cihazları Tarayıcı")
        self.root.geometry("900x550")
        self.root.configure(bg="#2e2e38")
        self.root.resizable(False, False)

        self.device_info_path = "device_info.json"
        self.device_info = self.load_device_info()

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#3a3a4a",
                        foreground="#ffffff",
                        rowheight=30,
                        fieldbackground="#3a3a4a",
                        font=("Segoe UI", 10))

        style.configure("Treeview.Heading",
                        background="#4a4a5a",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

        style.map("Treeview",
                  background=[("selected", "#5a6e9e")])

        self.table = ttk.Treeview(root, columns=("IP", "MAC", "VENDOR", "SELF", "NAME", "TYPE"), show="headings")
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=140)

        self.table.column("VENDOR", width=200, anchor="w")
        self.table.tag_configure("self-device", background="#446e6e")
        self.table.place(x=20, y=70, width=860, height=400)
        self.table.bind("<Double-1>", self.on_device_double_click)

        self.header = tk.Label(root, text="Ağ Cihazları", bg="#2e2e38", fg="white",
                               font=("Segoe UI", 20, "bold"))
        self.header.pack(pady=(20, 0))

        self.refresh_btn = tk.Button(root, text="Yeniden Tara", command=self.refresh_table,
                                     bg="#3a70f2", fg="white", font=("Segoe UI", 11, "bold"),
                                     relief="flat", padx=15, pady=8, activebackground="#2a60e0")
        self.refresh_btn.place(x=380, y=480)

        self.devices = []
        self.refresh_table()

    def load_device_info(self):
        if os.path.exists(self.device_info_path):
            try:
                with open(self.device_info_path, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_device_info(self):
        try:
            with open(self.device_info_path, "w") as f:
                json.dump(self.device_info, f, indent=2)
        except Exception as e:
            print("Cihaz bilgileri kaydedilemedi:", e)

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        self.devices = scan_network()
        for dev in self.devices:
            ip = dev["ip"]
            info = self.device_info.get(ip, {"name": "", "type": self.guess_device_type(dev["vendor"])})
            row = (ip, dev["mac"], dev["vendor"], "✅" if dev["self"] else "", info["name"], info["type"])
            tags = ("self-device",) if dev["self"] else ()
            self.table.insert("", "end", values=row, tags=tags)

    def on_device_double_click(self, event):
        selected_item = self.table.focus()
        if not selected_item:
            return

        values = self.table.item(selected_item, 'values')
        ip = values[0]
        device = next((d for d in self.devices if d["ip"] == ip), None)
        if device:
            self.show_device_details(device)

    def show_device_details(self, device):
        detail_win = tk.Toplevel(self.root)
        detail_win.title("Cihaz Detayları")
        detail_win.geometry("420x420")
        detail_win.configure(bg="#2e2e38")

        info = self.device_info.get(device["ip"], {"name": "", "type": self.guess_device_type(device["vendor"])})

        labels = [
            f"IP Adresi: {device['ip']}",
            f"MAC Adresi: {device['mac']}",
            f"Üretici: {device['vendor']}",
            f"Bu Cihaz: {'Evet' if device['self'] else 'Hayır'}"
        ]
        for text in labels:
            tk.Label(detail_win, text=text, bg="#2e2e38", fg="white",
                     font=("Segoe UI", 11)).pack(pady=3)

        entry_frame = tk.Frame(detail_win, bg="#2e2e38")
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Cihaz İsmi:", bg="#2e2e38", fg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        name_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), width=25, relief="flat")
        name_entry.insert(0, info["name"])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Cihaz Türü:", bg="#2e2e38", fg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        type_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), width=25, relief="flat")
        type_entry.insert(0, info["type"])
        type_entry.grid(row=1, column=1, padx=5, pady=5)

        def save_info():
            self.device_info[device["ip"]] = {
                "name": name_entry.get(),
                "type": type_entry.get()
            }
            self.save_device_info()
            self.refresh_table()
            detail_win.destroy()

        tk.Button(detail_win, text="Kaydet", command=save_info,
                  bg="#4caf50", fg="white", padx=15, pady=8,
                  font=("Segoe UI", 10, "bold"), relief="flat").pack(pady=15)

        btn_frame = tk.Frame(detail_win, bg="#2e2e38")
        btn_frame.pack(pady=5)

        for btn_text in ["İnterneti Kes", "Engelle", "Zamanla"]:
            tk.Button(btn_frame, text=btn_text, state="disabled",
                      bg="#5c5c70", fg="white", relief="flat",
                      font=("Segoe UI", 9, "bold"), padx=10, pady=5).pack(side="left", padx=5)

    def guess_device_type(self, vendor):
        vendor = vendor.lower()
        if any(keyword in vendor for keyword in ["apple", "samsung", "xiaomi", "huawei", "oppo", "vivo", "realme"]):
            return "Akıllı Telefon"
        elif any(keyword in vendor for keyword in ["espres", "sonoff", "tuya"]):
            return "IoT Cihazı"
        elif any(keyword in vendor for keyword in ["tplink", "asus", "netgear", "zyxel"]):
            return "Router"
        elif any(k in vendor for k in ["intel", "amd", "dell", "lenovo", "hp"]):
            return "Bilgisayar"
        return "Bilinmiyor"

if __name__ == "__main__":
    # API'yi başlat
    p = multiprocessing.Process(target=start_api)
    p.start()

    # GUI başlat
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()

    # GUI kapanınca API de kapatılsın
    p.terminate()