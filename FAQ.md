# FAQ - Frequently Asked Questions

## General Questions

### Q: Apa itu bot ini?
A: Ini adalah bot Telegram untuk toko online otomatis yang dapat menjual produk digital dengan sistem manajemen stok dan transaksi otomatis.

### Q: Apakah bot ini gratis?
A: Ya, bot ini open source dan gratis untuk digunakan. Anda hanya perlu server/hosting untuk menjalankannya.

### Q: Produk apa yang bisa dijual?
A: Bot ini cocok untuk produk digital seperti:
- Akun streaming (Netflix, Spotify, Disney+)
- Akun premium software (Canva, Office 365)
- Game items/accounts
- E-books
- Kode voucher/kupon
- Dan produk digital lainnya

### Q: Apakah mendukung payment gateway?
A: Saat ini bot menggunakan sistem saldo manual (admin top-up). Ada placeholder untuk integrasi payment gateway di masa depan.

### Q: Berapa kapasitas maksimal bot?
A: Bot dapat menangani ribuan pengguna. Kapasitas tergantung pada spesifikasi server dan database.

## Setup & Installation

### Q: Apa saja yang dibutuhkan untuk menjalankan bot?
A: Anda membutuhkan:
- API ID & API Hash dari my.telegram.org
- Bot Token dari @BotFather
- Server dengan Python 3.11+ (bisa VPS, local, atau cloud)
- MongoDB database
- User ID Telegram Anda sebagai admin

### Q: Bagaimana cara mendapatkan API ID dan API Hash?
A: 
1. Kunjungi https://my.telegram.org
2. Login dengan nomor Telegram Anda
3. Klik "API development tools"
4. Buat aplikasi baru
5. Copy API ID dan API Hash

### Q: Bagaimana cara mendapatkan Bot Token?
A:
1. Cari @BotFather di Telegram
2. Kirim `/newbot`
3. Ikuti instruksi untuk memberi nama bot
4. Copy token yang diberikan

### Q: Bagaimana cara mendapatkan User ID saya?
A:
1. Cari @userinfobot di Telegram
2. Kirim pesan apa saja
3. Bot akan menampilkan User ID Anda

### Q: Apakah harus menggunakan Docker?
A: Tidak. Docker opsional untuk memudahkan deployment, tapi Anda bisa install manual dengan Python.

### Q: Bisa jalan di Windows?
A: Ya, bot bisa jalan di Windows, Linux, dan macOS.

### Q: Berapa spesifikasi server minimum?
A:
- RAM: 512 MB (1 GB recommended)
- CPU: 1 core
- Storage: 5 GB
- OS: Ubuntu 20.04+ / Debian 11+ / Windows Server

## Usage Questions

### Q: Bagaimana cara menambah produk?
A:
1. Kirim `/addproduct` ke bot
2. Reply dengan format: `product_id|nama|harga|deskripsi`
3. Contoh: `netflix|Netflix Premium|50000|Akun Netflix 1 Bulan`

### Q: Bagaimana cara menambah stok?
A:
1. Kirim `/addstock` ke bot
2. Reply dengan:
```
product_id
data_stok_baris1
data_stok_baris2
```

### Q: Bisa menambah stok sekaligus banyak?
A: Ya, pisahkan setiap item dengan 1 baris kosong:
```
product_id
data_item1

data_item2

data_item3
```

### Q: Bagaimana cara menambah admin baru?
A: Edit file `.env` dan tambahkan User ID ke `ADMIN_IDS` (pisahkan dengan koma):
```
ADMIN_IDS=123456789,987654321,555555555
```

### Q: Bagaimana format data produk yang dikirim?
A: Data produk bisa multi-line. Contoh:
```
Email: user@example.com
Password: pass123
PIN: 1234
Note: Jangan share ke orang lain
```

### Q: Bisa kirim gambar/file untuk produk?
A: Saat ini hanya text-based. Untuk fitur file attachment, perlu development tambahan.

## Troubleshooting

### Q: Bot tidak merespon saat di-start
A: Cek:
- Apakah bot sudah running? Lihat logs
- Apakah kredensial di .env sudah benar?
- Apakah MongoDB sudah running?
- Apakah ada error di logs?

### Q: Error "Module not found"
A: Install dependencies:
```bash
pip install -r requirements.txt
```

### Q: Error "Connection refused" ke MongoDB
A: MongoDB belum running. Start dengan:
```bash
# Linux
sudo systemctl start mongodb

# Docker
docker-compose up -d mongodb
```

### Q: Stok tidak berkurang setelah transaksi
A: Cek logs untuk error. Kemungkinan:
- Database connection issue
- Product ID tidak match
- Stock ID tidak valid

### Q: User tidak menerima produk setelah beli
A: Cek:
- Apakah ada error di logs?
- Apakah user di-block bot? (bot tidak bisa kirim ke user yang block)
- Apakah stok benar-benar ada?

### Q: Bot crash/restart terus
A: Lihat error di logs:
```bash
# Manual
tail -f logs/bot.log

# Docker
docker-compose logs -f bot

# Systemd
sudo journalctl -u telegram-bot -f
```

## Database Questions

### Q: Database apa yang digunakan?
A: MongoDB

### Q: Apakah data pengguna aman?
A: Data tersimpan di database Anda sendiri. Pastikan:
- Gunakan password MongoDB yang kuat
- Backup database berkala
- Jangan expose MongoDB port ke internet

### Q: Bagaimana cara backup database?
A:
```bash
# Manual
mongodump --uri="mongodb://localhost:27017/telegram_shop_bot" --out=/backup

# Docker
docker-compose exec mongodb mongodump --out /tmp/backup
```

### Q: Bagaimana cara restore database?
A:
```bash
mongorestore --uri="mongodb://localhost:27017/telegram_shop_bot" /backup/path
```

### Q: Bisa pakai database lain selain MongoDB?
A: Saat ini hanya support MongoDB. Untuk database lain perlu modifikasi code.

## Payment Questions

### Q: Apakah support payment gateway otomatis?
A: Belum. Saat ini menggunakan sistem deposit manual oleh admin. Ada placeholder untuk integrasi payment gateway di masa depan.

### Q: Payment gateway apa yang bisa diintegrasikan?
A: Bisa diintegrasikan dengan:
- Midtrans
- Xendit
- PayPal
- Stripe
- Dan payment gateway lainnya (perlu development)

### Q: Bagaimana cara top-up saldo user?
A: Admin kirim command:
```
/deposit user_id amount
```
Contoh:
```
/deposit 123456789 50000
```

## Performance Questions

### Q: Berapa banyak user yang bisa dilayani?
A: Tergantung spesifikasi server. Dengan server 1GB RAM bisa handle ribuan user.

### Q: Apakah ada rate limiting?
A: Telegram API memiliki rate limit. Bot sudah handle dengan Pyrogram.

### Q: Bisa handle concurrent transactions?
A: Ya, MongoDB handle concurrent writes dengan baik.

## Development Questions

### Q: Apakah bisa dikustomisasi?
A: Ya, code modular dan bisa dimodifikasi sesuai kebutuhan.

### Q: Bagaimana cara menambah fitur baru?
A: Lihat CONTRIBUTING.md untuk panduan development.

### Q: Apakah support webhook mode?
A: Saat ini menggunakan polling. Webhook bisa ditambahkan dengan modifikasi.

### Q: Bahasa pemrograman apa?
A: Python dengan framework Pyrogram.

## Licensing

### Q: Apakah bisa digunakan untuk komersial?
A: Ya, bot ini berlisensi MIT yang memperbolehkan penggunaan komersial.

### Q: Apakah harus credit developer?
A: Tidak wajib, tapi dihargai jika Anda mencantumkan credit.

### Q: Bisa dijual kembali?
A: Ya, tapi dengan ketentuan MIT License.

## Support

### Q: Ada support berbayar?
A: Untuk support berbayar, hubungi developer melalui GitHub.

### Q: Bagaimana cara melaporkan bug?
A: Buka issue di GitHub dengan detail:
- Deskripsi bug
- Langkah reproduce
- Error message/logs
- Environment (OS, Python version)

### Q: Bagaimana cara request fitur?
A: Buka issue di GitHub dengan label "enhancement" dan jelaskan fitur yang diinginkan.

---

**Pertanyaan tidak terjawab?**
- Buka discussion di GitHub
- Buka issue baru
- Hubungi developer

**Update terakhir:** 2024
