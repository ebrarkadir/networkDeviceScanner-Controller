# 🕷️ DarkMesh - Ağ Cihazları Tarayıcı & Erişim Kontrol Paneli

**DarkMesh**, Linux üzerinde çalışan grafik arayüzlü bir ağ izleme ve kontrol uygulamasıdır.  
Raspberry Pi cihazına yüklenen **OpenWRT** ile birlikte çalışarak ağdaki cihazları tespit eder, internet erişimlerini kontrol etmenizi sağlar ve zamanlanmış kurallar ile belirli cihazların erişimini otomatik olarak engelleyebilir.

---

## 🎯 Amaç

Kullanıcının yerel ağında bulunan cihazları tespit etmesini, analiz etmesini ve güvenlik açısından risk taşıyan cihazlara müdahale edebilmesini sağlamaktır.  
Özellikle kablosuz ağlara izinsiz erişim gibi durumların önüne geçmeyi hedefler.

---

## 🚀 Özellikler

- 📡 **Ağ Taraması:** IP, MAC adresi ve üretici bilgisi
- 🧠 **Cihaz Tanımlama:** İsim ve cihaz türü girilebilir
- 🌐 **Ping Atma:** Cihazın ağa yanıt verip vermediğini ölçer
- 🔐 **Port Taraması:** Sık kullanılan TCP portları üzerinden açık servislere bakar
- ❌ **İnterneti Kesme:** Cihazın internet erişimini iptables ile engeller
- 🔄 **İnterneti Açma:** Engellenen cihazın erişimi tekrar sağlanabilir
- ⏱️ **Zamanlama Özelliği:** Belirli saatlerde otomatik internet engelleme
- 💻 **GUI Arayüz:** Kullanımı kolay, tamamen grafiksel arayüz (Tkinter)
- 📁 **Linux Uygulaması:** `.desktop` desteğiyle menüden başlatılabilir

---

## 🧰 Kullanılan Teknolojiler

- Python 3
- Tkinter (GUI)
- Flask (API sunucusu - OpenWRT'de çalışır)
- `iptables` (internet engelleme için)
- threading (asenkron işlemler)
- `nmap` (port tarama için - OpenWRT tarafında)
- Raspberry Pi + OpenWRT (router olarak)

---

## 🖼️ Ekran Görüntüleri

Ekran görüntüleri `ss/` klasöründe yer almaktadır.

| Ana Sayfa | Detaylar | Ping | Port Taraması | Zamanlayıcı |
|-----------|----------|------|----------------|-------------|
| ![Ana Sayfa](ss/anasayfa.png) | ![Detaylar](ss/detaylar.png) | ![Ping](ss/ping.png) | ![Port](ss/port.png) | ![Zaman](ss/zaman.png) |

---

## ⚙️ Kurulum

### 🖥️ 1. Ana Bilgisayar (Linux) Üzerinde

#### Gerekli Bağımlılıklar

```bash
sudo apt install python3 python3-pip nmap -y
pip3 install requests
```
#### Fedora veya RPM tabanlı sistemler:
```bash
sudo dnf install python3 python3-tkinter nmap -y
pip3 install requests
```
#### Debain için:
```bash
sudo apt install python3 python3-tkinter nmap -y
pip3 install requests
```
#### Depoyu Klonla:
```bash
git clone https://github.com/kullanici-adi/darkmesh.git
cd darkmesh
```
#### Uygulamayı başlat:
```bash
python3 main.py
```

#### 2.Raspberry Pi Cihazına OpenWRT Kurulumu
-Raspberry Pi cihazına OpenWRT kurulmalı

-Raspberry Pi modeme WAN portu üzerinden bağlanmalı

-Ana bilgisayar (uygulamanın çalıştığı sistem) Raspberry üzerinden internete çıkmalı

-Böylece Raspberry Pi tüm ağ trafiğini denetleyen router olur

### 3.Raspberry Pi Üzerinde Flask API Kurulumu
#### Gerekli Paketleri Yükle (OpenWRT)
```bash
opkg update
opkg install python3 python3-pip
pip3 install flask flask-cors
```
#### **server.py** Dosyasını Raspberry Pi’ye Kopyala
```bash
scp server.py root@192.168.8.1:/root/
ssh root@192.168.8.1
python3 /root/server.py
(Raspberry IP'si farklıysa 192.168.8.1 yerine onu yaz.)
```
#### Flask Portunu Aç (5000)
```bash
uci add firewall rule
uci set firewall.@rule[-1].name='Allow-Flask'
uci set firewall.@rule[-1].src='lan'
uci set firewall.@rule[-1].dest_port='5000'
uci set firewall.@rule[-1].target='ACCEPT'
uci set firewall.@rule[-1].proto='tcp'
uci commit firewall
/etc/init.d/firewall restart
```
### 4. Ana Bilgisayarda IP Ayarlarını Yap
#### main.py içinde Flask sunucusunun IP’sini doğru şekilde ayarlamalısın:
```bash
RASPBERRY_IP = "192.168.8.1"  # veya senin Pi'nin IP'si ne ise
```

Artık uygulama arayüzü üzerinden port tarama, ping atma, internet engelleme işlemleri doğrudan Raspberry'deki OpenWRT API’ye gönderilir.
