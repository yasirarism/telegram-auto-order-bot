# Quick Start Guide

Panduan cepat untuk menjalankan bot pertama kali.

## 1. Persiapan

### A. Dapatkan API Credentials

1. Buka [my.telegram.org](https://my.telegram.org)
2. Login dengan nomor telepon Telegram Anda
3. Klik "API development tools"
4. Buat aplikasi baru, dapatkan `API_ID` dan `API_HASH`

### B. Buat Bot di Telegram

1. Cari [@BotFather](https://t.me/BotFather) di Telegram
2. Kirim `/newbot`
3. Ikuti instruksi untuk membuat bot
4. Simpan `BOT_TOKEN` yang diberikan

### C. Dapatkan User ID Admin

1. Cari [@userinfobot](https://t.me/userinfobot) di Telegram
2. Kirim pesan apa saja
3. Simpan `ID` yang ditampilkan

## 2. Setup Cepat dengan Docker (Recommended)

### Langkah 1: Clone Repository
```bash
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot
```

### Langkah 2: Konfigurasi
```bash
cp .env.example .env
nano .env
```

Edit file `.env`:
```env
API_ID=12345678
API_HASH=abc123def456
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
MONGO_URI=mongodb://admin:admin123@mongodb:27017
DB_NAME=telegram_shop_bot
ADMIN_IDS=987654321
OWNER_NAME=Toko Saya
BOT_NAME=MyShop Bot
```

### Langkah 3: Jalankan
```bash
docker-compose up -d
```

### Langkah 4: Cek Status
```bash
docker-compose logs -f bot
```

### Langkah 5: Setup Sample Data (Opsional)
```bash
docker-compose exec bot python setup_sample_data.py
```

## 3. Setup Manual (Tanpa Docker)

### Langkah 1: Clone Repository
```bash
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot
```

### Langkah 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Langkah 3: Install MongoDB

**Ubuntu/Debian:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Windows:**
Download dari [mongodb.com](https://www.mongodb.com/try/download/community)

### Langkah 4: Konfigurasi
```bash
cp .env.example .env
nano .env
```

Edit file `.env`:
```env
API_ID=12345678
API_HASH=abc123def456
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
MONGO_URI=mongodb://localhost:27017
DB_NAME=telegram_shop_bot
ADMIN_IDS=987654321
OWNER_NAME=Toko Saya
BOT_NAME=MyShop Bot
```

### Langkah 5: Buat Folder Logs
```bash
mkdir logs
```

### Langkah 6: Setup Sample Data (Opsional)
```bash
python setup_sample_data.py
```

### Langkah 7: Jalankan Bot
```bash
python main.py
```

## 4. Verifikasi Bot Berjalan

1. Buka Telegram dan cari bot Anda
2. Kirim `/start`
3. Bot harus merespon dengan menu utama

Jika bot tidak merespon, cek:
- Logs di `logs/bot.log`
- Kredensial di file `.env`
- Status MongoDB

## 5. Setup Produk Pertama

### Tambah Produk
1. Kirim `/addproduct` ke bot
2. Reply dengan:
```
test_product|Produk Test|10000|Ini adalah produk test
```

### Tambah Stok
1. Kirim `/addstock` ke bot
2. Reply dengan:
```
test_product
Data produk test 1

Data produk test 2
```

### Verifikasi
1. Kirim command `/listproducts`
2. Produk test harus muncul dengan stok 2

## 6. Test Transaksi

1. Top-up saldo ke akun Anda:
```
/deposit YOUR_USER_ID 50000
```

2. Klik **📦 Katalog**
3. Pilih produk dengan klik nomor
4. Klik **✅ Beli Sekarang**
5. Produk akan dikirim otomatis

## 7. Perintah Admin Penting

```bash
/addproduct      # Tambah produk baru
/addstock        # Tambah stok
/deposit         # Top-up saldo user
/listproducts    # Lihat semua produk
/listusers       # Lihat pengguna
/stats           # Lihat statistik
/broadcast       # Kirim pesan ke semua user
```

## Troubleshooting

### Bot tidak merespon
```bash
# Cek logs
tail -f logs/bot.log

# Atau dengan Docker
docker-compose logs -f bot
```

### MongoDB connection error
```bash
# Manual: Pastikan MongoDB running
sudo systemctl status mongodb

# Docker: Restart container
docker-compose restart mongodb
```

### Module not found
```bash
# Install ulang dependencies
pip install -r requirements.txt --force-reinstall
```

## Selanjutnya

- Baca [USAGE.md](USAGE.md) untuk panduan lengkap penggunaan
- Baca [README.md](README.md) untuk dokumentasi teknis
- Sesuaikan konfigurasi sesuai kebutuhan

## Support

Jika ada masalah:
1. Cek logs: `logs/bot.log`
2. Buka issue di GitHub
3. Hubungi developer

Selamat menggunakan! 🎉
