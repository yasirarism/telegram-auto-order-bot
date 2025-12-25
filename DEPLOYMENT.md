# Deployment Guide

Panduan deployment bot ke berbagai platform.

## 1. Deployment Lokal (Development)

### Prasyarat
- Python 3.11+
- MongoDB

### Langkah-langkah
```bash
# Clone repository
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot

# Install dependencies
pip install -r requirements.txt

# Setup konfigurasi
cp .env.example .env
nano .env  # Edit dengan kredensial Anda

# Setup sample data (opsional)
python setup_sample_data.py

# Jalankan bot
python main.py
```

## 2. Deployment dengan Docker

### Prasyarat
- Docker
- Docker Compose

### Langkah-langkah
```bash
# Clone repository
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot

# Setup konfigurasi
cp .env.example .env
nano .env  # Edit dengan kredensial Anda

# Pastikan MONGO_URI untuk Docker
# MONGO_URI=mongodb://admin:admin123@mongodb:27017

# Build dan jalankan
docker-compose up -d

# Cek logs
docker-compose logs -f bot

# Setup sample data (opsional)
docker-compose exec bot python setup_sample_data.py
```

### Maintenance
```bash
# Stop bot
docker-compose down

# Restart bot
docker-compose restart bot

# Lihat logs
docker-compose logs -f bot

# Backup database
docker-compose exec mongodb mongodump --out /tmp/backup

# Update bot (jika ada perubahan code)
git pull
docker-compose build
docker-compose up -d
```

## 3. Deployment ke VPS (Ubuntu/Debian)

### Prasyarat
- Ubuntu 20.04+ atau Debian 11+
- Akses SSH ke VPS
- Domain (opsional)

### Langkah-langkah

#### A. Setup Server
```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip git mongodb

# Install Docker (opsional, jika ingin pakai Docker)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### B. Clone dan Setup Bot
```bash
# Clone repository
cd ~
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot

# Install dependencies
pip3 install -r requirements.txt

# Setup konfigurasi
cp .env.example .env
nano .env  # Edit dengan kredensial Anda
```

#### C. Setup Systemd Service
```bash
# Buat service file
sudo nano /etc/systemd/system/telegram-bot.service
```

Isi dengan:
```ini
[Unit]
Description=Telegram Auto Order Bot
After=network.target mongodb.service

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/telegram-auto-order-bot
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/telegram-auto-order-bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ganti `YOUR_USERNAME` dengan username Linux Anda.

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable dan start service
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Cek status
sudo systemctl status telegram-bot

# Lihat logs
sudo journalctl -u telegram-bot -f
```

#### D. Setup dengan Docker di VPS
```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Setup konfigurasi
cp .env.example .env
nano .env

# Jalankan dengan Docker
docker-compose up -d

# Auto-restart on boot
sudo systemctl enable docker
```

## 4. Deployment ke Heroku

### Prasyarat
- Akun Heroku
- Heroku CLI

### Langkah-langkah

#### A. Persiapan
```bash
# Login ke Heroku
heroku login

# Buat aplikasi
heroku create nama-bot-anda

# Add MongoDB addon
heroku addons:create mongolab:sandbox
```

#### B. Setup Konfigurasi
```bash
# Set environment variables
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set ADMIN_IDS=your_user_id
heroku config:set OWNER_NAME="Your Store"
heroku config:set BOT_NAME="Your Bot"

# MongoDB URI akan otomatis dari addon mongolab
```

#### C. Deploy
```bash
# Tambah file Procfile
echo "worker: python main.py" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Scale worker
heroku ps:scale worker=1

# Cek logs
heroku logs --tail
```

## 5. Deployment ke Railway

### Prasyarat
- Akun GitHub
- Akun Railway

### Langkah-langkah

1. Fork repository ini di GitHub
2. Buka [Railway.app](https://railway.app)
3. Login dengan GitHub
4. Klik "New Project"
5. Pilih "Deploy from GitHub repo"
6. Pilih repository yang di-fork
7. Tambahkan MongoDB:
   - Klik "New" -> "Database" -> "MongoDB"
8. Set environment variables:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `ADMIN_IDS`
   - `MONGO_URI` (copy dari MongoDB service)
9. Deploy akan otomatis

## 6. Deployment ke Render

### Prasyarat
- Akun GitHub
- Akun Render

### Langkah-langkah

1. Fork repository
2. Buka [Render.com](https://render.com)
3. Klik "New" -> "Background Worker"
4. Connect GitHub repository
5. Set konfigurasi:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
6. Add MongoDB:
   - Gunakan MongoDB Atlas atau add-on
7. Set environment variables
8. Deploy

## 7. Best Practices untuk Production

### Security
- Jangan commit file `.env` ke repository
- Gunakan password MongoDB yang kuat
- Batasi akses admin hanya ke user terpercaya
- Enable firewall di VPS
- Gunakan HTTPS untuk webhook (jika pakai webhook mode)

### Monitoring
- Setup log rotation untuk file logs
- Monitor disk space untuk database
- Setup alerting untuk downtime
- Backup database secara berkala

### Backup
```bash
# Backup MongoDB
mongodump --uri="mongodb://localhost:27017/telegram_shop_bot" --out=/backup/$(date +%Y%m%d)

# Dengan Docker
docker-compose exec mongodb mongodump --out /tmp/backup
docker cp telegram_bot_mongodb:/tmp/backup ./backup/$(date +%Y%m%d)

# Restore
mongorestore --uri="mongodb://localhost:27017/telegram_shop_bot" /backup/YYYYMMDD
```

### Auto Backup Script
```bash
#!/bin/bash
# save as backup.sh

BACKUP_DIR="/home/user/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup MongoDB
mongodump --uri="mongodb://localhost:27017/telegram_shop_bot" --out=$BACKUP_DIR/$DATE

# Keep only last 7 backups
cd $BACKUP_DIR
ls -t | tail -n +8 | xargs rm -rf

echo "Backup completed: $DATE"
```

Setup cron untuk auto backup:
```bash
# Edit crontab
crontab -e

# Add line (backup setiap hari jam 3 pagi)
0 3 * * * /home/user/backup.sh
```

## Troubleshooting

### Bot tidak jalan setelah restart server
```bash
# Cek status service
sudo systemctl status telegram-bot

# Restart service
sudo systemctl restart telegram-bot

# Cek logs
sudo journalctl -u telegram-bot -n 100
```

### MongoDB connection refused
```bash
# Cek MongoDB status
sudo systemctl status mongodb

# Start MongoDB
sudo systemctl start mongodb

# Cek connection
mongo --eval "db.serverStatus()"
```

### Out of memory
```bash
# Tambah swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Monitoring dan Maintenance

### Setup Monitoring dengan PM2
```bash
# Install PM2
npm install -g pm2

# Start bot dengan PM2
pm2 start main.py --name telegram-bot --interpreter python3

# Auto restart on crash
pm2 startup
pm2 save

# Monitor
pm2 monit

# Logs
pm2 logs telegram-bot
```

### Health Check Script
```python
# health_check.py
import requests
import sys

BOT_TOKEN = "YOUR_BOT_TOKEN"

try:
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
    if response.json()["ok"]:
        print("✅ Bot is running")
        sys.exit(0)
    else:
        print("❌ Bot is not responding")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
```

Setup cron untuk health check:
```bash
# Setiap 5 menit
*/5 * * * * /usr/bin/python3 /home/user/telegram-auto-order-bot/health_check.py
```

## Support

Untuk masalah deployment:
1. Cek logs terlebih dahulu
2. Pastikan semua environment variables sudah set
3. Verifikasi koneksi MongoDB
4. Buka issue di GitHub dengan detail error

---

Happy deploying! 🚀
