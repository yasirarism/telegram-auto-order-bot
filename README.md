# Telegram Auto Order Bot

Bot Telegram berbasis Pyrogram untuk toko online otomatis dengan sistem manajemen produk, stok, dan transaksi menggunakan MongoDB.

## 🌟 Fitur

### 1. Menu Start (/start)
- Menampilkan informasi total pengguna bot dan total transaksi berhasil
- Tombol inline "Produk Teratas" dan "Pembeli Teratas"
- Contoh tampilan:
  ```
  Halo, Yasir Store! Selamat datang di Arukaey Bot 👋🏻
  
  ╭  ◦ Total Pengguna Bot: 585 Orang
  ╰  ◦ Total Transaksi Berhasil: 6202x
  ```

### 2. Menu Custom Keyboard
- **🏠 Start:** Kembali ke menu utama
- **💬 Private Message:** Membuka chat privat dengan admin
- **📦 Katalog:** Menampilkan daftar produk dengan stok tersedia
- **📊 Stok:** Menampilkan stok semua produk
- **👤 Informasi Akun:** Detail akun pengguna dan saldo
- **💰 Deposit:** Admin dapat menambah saldo pengguna

### 3. Pengelolaan Produk
- Tombol angka (1-10) untuk memilih produk
- Pagination otomatis untuk lebih dari 10 produk
- Detail produk dengan tombol checkout
- Stok otomatis berkurang saat transaksi berhasil

### 4. Panel Admin
- Tambah produk baru
- Tambah stok (single atau bulk)
- Top-up saldo pengguna manual
- Lihat statistik bot
- Broadcast pesan ke semua pengguna
- Lihat daftar produk dan pengguna

### 5. Database MongoDB
- **Users:** Data pengguna, saldo, dan riwayat transaksi
- **Products:** Informasi produk dan harga
- **Stocks:** Manajemen stok produk
- **Transactions:** Riwayat transaksi

### 6. Docker Support
- Deployment mudah dengan Docker dan Docker Compose
- MongoDB container included

## 🚀 Instalasi

### Prasyarat
- Python 3.11+
- MongoDB (atau gunakan Docker)
- API credentials dari [my.telegram.org](https://my.telegram.org)
- Bot token dari [@BotFather](https://t.me/BotFather)

### Instalasi Manual

1. Clone repository:
```bash
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Salin file konfigurasi:
```bash
cp .env.example .env
```

4. Edit file `.env` dengan kredensial Anda:
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MONGO_URI=mongodb://localhost:27017
DB_NAME=telegram_shop_bot
ADMIN_IDS=123456789,987654321
OWNER_NAME=Yasir Store
BOT_NAME=Arukaey Bot
```

5. Buat folder logs:
```bash
mkdir -p logs
```

6. Jalankan bot:
```bash
python main.py
```

### Instalasi dengan Docker

1. Clone repository:
```bash
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot
```

2. Salin dan edit konfigurasi:
```bash
cp .env.example .env
# Edit .env dengan kredensial Anda
```

3. Update MONGO_URI di `.env` untuk Docker:
```env
MONGO_URI=mongodb://admin:admin123@mongodb:27017
```

4. Jalankan dengan Docker Compose:
```bash
docker-compose up -d
```

5. Lihat logs:
```bash
docker-compose logs -f bot
```

## 📖 Penggunaan

### Untuk Pengguna

1. Start bot dengan `/start`
2. Pilih **📦 Katalog** untuk melihat produk
3. Klik nomor produk untuk melihat detail
4. Klik **✅ Beli Sekarang** untuk checkout
5. Produk akan dikirim otomatis setelah pembayaran berhasil

### Untuk Admin

#### Menambah Produk Baru

1. Kirim perintah `/addproduct`
2. Reply dengan format:
```
product_id|nama|harga|deskripsi
```

Contoh:
```
netflix_premium|Netflix Premium|50000|Akun Netflix Premium 1 Bulan
```

#### Menambah Stok

1. Kirim perintah `/addstock`
2. Reply dengan format:
```
product_id
data_stok
```

Contoh untuk 1 stok:
```
netflix_premium
email: test@example.com
password: password123
```

Contoh untuk multiple stok:
```
netflix_premium
email: user1@example.com
password: pass123

email: user2@example.com
password: pass456

email: user3@example.com
password: pass789
```

#### Top-Up Saldo Pengguna

```bash
/deposit <user_id> <amount>
```

Contoh:
```
/deposit 123456789 50000
```

#### Perintah Admin Lainnya

- `/listproducts` - Lihat semua produk
- `/listusers` - Lihat 20 pengguna terbaru
- `/stats` - Lihat statistik bot
- `/broadcast` - Reply ke pesan yang ingin di-broadcast

## 🗂️ Struktur Kode

```
telegram-auto-order-bot/
├── main.py              # Entry point bot
├── config.py            # Konfigurasi dan environment variables
├── database.py          # Database operations dan models
├── handlers.py          # Handler untuk user commands
├── admin.py             # Handler untuk admin commands
├── keyboards.py         # Keyboard markup utilities
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── .env.example         # Example environment file
├── .gitignore          # Git ignore file
└── logs/               # Log files directory
```

## 🔧 Konfigurasi

### Environment Variables

| Variable | Deskripsi | Required |
|----------|-----------|----------|
| `API_ID` | Telegram API ID dari my.telegram.org | Ya |
| `API_HASH` | Telegram API Hash dari my.telegram.org | Ya |
| `BOT_TOKEN` | Bot token dari @BotFather | Ya |
| `MONGO_URI` | MongoDB connection URI | Ya |
| `DB_NAME` | Nama database MongoDB | Ya |
| `ADMIN_IDS` | User IDs admin (pisahkan dengan koma) | Ya |
| `OWNER_NAME` | Nama pemilik toko | Opsional |
| `BOT_NAME` | Nama bot | Opsional |

## 🔐 Keamanan

- Jangan commit file `.env` ke repository
- Pastikan `ADMIN_IDS` hanya berisi user ID yang terpercaya
- Gunakan password yang kuat untuk MongoDB di production
- Backup database secara berkala

## 🐛 Troubleshooting

### Bot tidak merespon
- Pastikan bot token benar
- Cek logs di folder `logs/bot.log`
- Pastikan MongoDB berjalan

### Error koneksi MongoDB
- Pastikan MongoDB service berjalan
- Cek `MONGO_URI` di file `.env`
- Untuk Docker, pastikan container MongoDB up

### Stok tidak bertambah
- Pastikan format pesan sesuai
- Pastikan product_id sudah ada di database
- Cek logs untuk error message

## 📝 Lisensi

MIT License - silakan gunakan dan modifikasi sesuai kebutuhan.

## 🤝 Kontribusi

Pull requests are welcome! Untuk perubahan besar, silakan buka issue terlebih dahulu untuk diskusi.

## 👨‍💻 Developer

Developed by [Yasir](https://github.com/yasirarism)

## 📞 Support

Jika ada pertanyaan atau masalah, silakan buka issue di GitHub atau hubungi admin.
