import tkinter as tk
from tkinter import ttk
from scanner import scan_network

class NetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ağ Cihazları Tarayıcı")
        self.root.geometry("900x550")
        self.root.configure(bg="#2e2e38")  # Daha açık koyu gri arka plan
        self.root.resizable(False, False)

        # Stil ayarları
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

        # Tablo
        self.table = ttk.Treeview(root, columns=("IP", "MAC", "VENDOR", "SELF"), show="headings")
        self.table.heading("IP", text="IP Adresi")
        self.table.heading("MAC", text="MAC Adresi")
        self.table.heading("VENDOR", text="Üretici")
        self.table.heading("SELF", text="Bu Cihaz")

        self.table.column("IP", width=180, anchor="center")
        self.table.column("MAC", width=230, anchor="center")
        self.table.column("VENDOR", width=360, anchor="w")
        self.table.column("SELF", width=100, anchor="center")

        self.table.tag_configure("self-device", background="#446e6e")  # kendi cihaz: açık yeşilimsi-gri ton

        self.table.place(x=20, y=70, width=860, height=400)

        # Başlık
        self.header = tk.Label(root, text="Ağ Cihazları", bg="#2e2e38", fg="white",
                               font=("Segoe UI", 20, "bold"))
        self.header.pack(pady=(20, 0))

        # Buton
        self.refresh_btn = tk.Button(root, text="Yeniden Tara", command=self.refresh_table,
                                     bg="#3a70f2", fg="white", font=("Segoe UI", 11, "bold"),
                                     relief="flat", padx=15, pady=8, activebackground="#2a60e0")
        self.refresh_btn.place(x=380, y=480)

        # Başlangıçta verileri getir
        self.refresh_table()

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        devices = scan_network()
        for dev in devices:
            row = (dev["ip"], dev["mac"], dev["vendor"], "✅" if dev["self"] else "")
            tags = ("self-device",) if dev["self"] else ()
            self.table.insert("", "end", values=row, tags=tags)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()
