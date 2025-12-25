# Panduan Penggunaan Bot

## Untuk Pengguna

### 1. Memulai Bot

1. Cari bot di Telegram
2. Klik tombol **Start** atau kirim `/start`
3. Bot akan menampilkan menu utama dengan statistik

### 2. Melihat Katalog Produk

1. Klik tombol **📦 Katalog**
2. Bot akan menampilkan daftar produk dengan nomor (1-10)
3. Klik nomor produk untuk melihat detail
4. Jika ada lebih dari 10 produk, gunakan tombol navigasi untuk pindah halaman

### 3. Membeli Produk

1. Setelah memilih produk, bot akan menampilkan detail produk
2. Klik tombol **✅ Beli Sekarang**
3. Bot akan mengecek saldo dan stok
4. Jika saldo cukup dan stok tersedia, transaksi akan diproses
5. Produk akan langsung dikirim ke chat Anda

### 4. Cek Saldo dan Informasi Akun

1. Klik tombol **👤 Informasi Akun**
2. Bot akan menampilkan:
   - User ID
   - Nama dan username
   - Saldo saat ini
   - Total transaksi

### 5. Top-Up Saldo

1. Klik tombol **💰 Deposit**
2. Hubungi admin melalui menu **💬 Private Message**
3. Admin akan menambahkan saldo secara manual

### 6. Melihat Stok Produk

1. Klik tombol **📊 Stok**
2. Bot akan menampilkan semua produk dan jumlah stok tersedia

## Untuk Admin

### 1. Menambah Produk Baru

**Langkah 1:** Kirim perintah `/addproduct`

**Langkah 2:** Reply dengan format:
```
product_id|nama|harga|deskripsi
```

**Contoh:**
```
/addproduct
```
Reply:
```
netflix_premium|Netflix Premium|50000|Akun Netflix Premium 1 Bulan dengan garansi
```

### 2. Menambah Stok Produk

**Langkah 1:** Kirim perintah `/addstock`

**Langkah 2:** Reply dengan format:

**Untuk 1 item stok:**
```
product_id
data_stok_baris1
data_stok_baris2
```

**Contoh:**
```
/addstock
```
Reply:
```
netflix_premium
Email: test@example.com
Password: password123
PIN: 1234
```

**Untuk multiple item stok:**
Pisahkan setiap item dengan 1 baris kosong
```
product_id
data_stok_1_baris1
data_stok_1_baris2

data_stok_2_baris1
data_stok_2_baris2

data_stok_3_baris1
data_stok_3_baris2
```

**Contoh:**
```
/addstock
```
Reply:
```
netflix_premium
Email: user1@example.com
Password: pass123

Email: user2@example.com
Password: pass456

Email: user3@example.com
Password: pass789
```

### 3. Top-Up Saldo Pengguna

**Format:**
```
/deposit <user_id> <amount>
```

**Contoh:**
```
/deposit 123456789 50000
```

**Cara mendapatkan User ID:**
1. Minta user mengirim pesan ke bot
2. Gunakan `/listusers` untuk melihat daftar user
3. Copy User ID yang ditampilkan

### 4. Melihat Daftar Produk

**Perintah:** `/listproducts`

Menampilkan:
- Status aktif/non-aktif
- Nama dan ID produk
- Harga
- Stok tersedia
- Total terjual

### 5. Melihat Daftar Pengguna

**Perintah:** `/listusers`

Menampilkan 20 pengguna terbaru dengan:
- User ID
- Nama
- Saldo
- Total transaksi

### 6. Melihat Statistik Bot

**Perintah:** `/stats`

Menampilkan:
- Total pengguna
- Total produk
- Total transaksi
- Total pendapatan

### 7. Broadcast Pesan

**Langkah 1:** Buat pesan yang ingin di-broadcast

**Langkah 2:** Reply pesan tersebut dengan `/broadcast`

Bot akan mengirim pesan ke semua pengguna yang terdaftar.

## Tips & Trik

### Untuk Pengguna
- Pastikan saldo cukup sebelum membeli
- Simpan data produk yang diterima dengan aman
- Gunakan menu **📊 Stok** untuk cek ketersediaan sebelum membeli

### Untuk Admin
- Selalu cek dengan `/listproducts` sebelum menambah produk baru
- Gunakan product_id yang mudah diingat (contoh: netflix_premium, spotify_family)
- Backup database secara berkala
- Monitor statistik dengan `/stats` secara rutin
- Pastikan data stok yang ditambahkan valid dan teruji

## Troubleshooting

### "Stok habis"
- Admin perlu menambah stok dengan `/addstock`

### "Saldo tidak cukup"
- User perlu top-up saldo melalui admin

### "Produk tidak ditemukan"
- Pastikan product_id sudah benar
- Gunakan `/listproducts` untuk cek product_id yang tersedia

### "Transaksi gagal"
- Cek log bot untuk detail error
- Pastikan database berjalan dengan baik
- Hubungi developer jika masalah berlanjut
