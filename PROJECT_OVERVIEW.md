# 🤖 Telegram Auto Order Bot - Project Overview

## 🎯 What is this?

A complete, production-ready Telegram bot for running an automated online store selling digital products. Built with Python, Pyrogram, and MongoDB.

## ✨ Key Features at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    🏠 MAIN MENU                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Halo, User! Selamat datang di Arukaey Bot 👋🏻            │
│                                                              │
│  ╭  ◦ Total Pengguna Bot: 585 Orang                         │
│  ╰  ◦ Total Transaksi Berhasil: 6202x                       │
│                                                              │
│  [🏆 Produk Teratas] [👥 Pembeli Teratas]                  │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┬──────────────────┐                       │
│  │  🏠 Start    │  💬 Private Msg  │                       │
│  ├──────────────┼──────────────────┤                       │
│  │  📦 Katalog  │  📊 Stok         │                       │
│  ├──────────────┼──────────────────┤                       │
│  │  👤 Akun     │  💰 Deposit      │                       │
│  └──────────────┴──────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📊 User Journey

```
Start Bot
    │
    ├─> View Catalog
    │       │
    │       ├─> Select Product (1-10)
    │       │       │
    │       │       ├─> View Details
    │       │       │       │
    │       │       │       ├─> Buy Now
    │       │       │       │       │
    │       │       │       │       ├─> Check Balance ✓
    │       │       │       │       │
    │       │       │       │       ├─> Check Stock ✓
    │       │       │       │       │
    │       │       │       │       ├─> Process Transaction
    │       │       │       │       │
    │       │       │       │       └─> Deliver Product ✅
    │       │       │       │
    │       │       │       └─> Cancel ❌
    │       │       │
    │       │       └─> More Pages (if >10 products)
    │       │
    │       └─> Back to Menu
    │
    ├─> Check Account Info
    │       └─> View Balance & History
    │
    ├─> Check Stock
    │       └─> View All Available Products
    │
    └─> Contact Admin
            └─> Private Message
```

## 🔧 Admin Flow

```
Admin Commands
    │
    ├─> /addproduct
    │       └─> product_id|name|price|description
    │
    ├─> /addstock
    │       └─> product_id
    │           data_line1
    │           data_line2
    │
    ├─> /deposit user_id amount
    │       └─> Add balance to user
    │
    ├─> /listproducts
    │       └─> View all products & stock
    │
    ├─> /listusers
    │       └─> View recent users
    │
    ├─> /stats
    │       └─> Bot statistics
    │
    └─> /broadcast
            └─> Reply to message to broadcast
```

## 🗄️ Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                     MONGODB DATABASE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📁 users                                                    │
│     ├─ user_id (unique)                                      │
│     ├─ username                                              │
│     ├─ full_name                                             │
│     ├─ balance                                               │
│     ├─ total_transactions                                    │
│     ├─ created_at                                            │
│     └─ last_active                                           │
│                                                              │
│  📁 products                                                 │
│     ├─ product_id (unique)                                   │
│     ├─ name                                                  │
│     ├─ description                                           │
│     ├─ price                                                 │
│     ├─ category                                              │
│     ├─ total_sold                                            │
│     ├─ is_active                                             │
│     └─ created_at                                            │
│                                                              │
│  📁 stocks                                                   │
│     ├─ product_id                                            │
│     ├─ data                                                  │
│     ├─ is_used                                               │
│     ├─ added_at                                              │
│     ├─ used_at                                               │
│     └─ used_by                                               │
│                                                              │
│  📁 transactions                                             │
│     ├─ transaction_id (unique)                               │
│     ├─ user_id                                               │
│     ├─ product_id                                            │
│     ├─ amount                                                │
│     ├─ quantity                                              │
│     ├─ status                                                │
│     └─ created_at                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TELEGRAM BOT                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌────────┐   ┌─────────┐   ┌─────────┐
   │ Users  │   │  Admin  │   │ Handlers│
   │ Layer  │   │  Panel  │   │ Layer   │
   └────┬───┘   └────┬────┘   └────┬────┘
        │            │             │
        └────────────┼─────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   Database      │
            │   Operations    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │    MongoDB      │
            │   Collections   │
            └─────────────────┘
```

## 📦 File Organization

```
telegram-auto-order-bot/
│
├── 🐍 Python Files (Core)
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration
│   ├── database.py          # DB operations
│   ├── handlers.py          # User handlers
│   ├── admin.py             # Admin handlers
│   └── keyboards.py         # UI keyboards
│
├── 🛠️ Utilities
│   ├── setup_sample_data.py # Sample data
│   └── test_structure.py    # Validation
│
├── 🐳 Deployment
│   ├── Dockerfile           # Container
│   ├── docker-compose.yml   # Orchestration
│   ├── requirements.txt     # Dependencies
│   ├── install.sh          # Linux installer
│   └── install.bat         # Windows installer
│
├── 📚 Documentation
│   ├── README.md            # Main docs
│   ├── QUICKSTART.md        # Quick setup
│   ├── USAGE.md             # Usage guide
│   ├── DEPLOYMENT.md        # Deploy guide
│   ├── FAQ.md               # Questions
│   ├── CONTRIBUTING.md      # Dev guide
│   └── IMPLEMENTATION_SUMMARY.md
│
└── ⚙️ Configuration
    ├── .env.example         # Template
    ├── .gitignore          # Git rules
    └── LICENSE             # MIT License
```

## 🚀 Quick Start Commands

### Installation
```bash
# Clone
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot

# Setup
cp .env.example .env
# Edit .env with your credentials

# Docker (Recommended)
docker-compose up -d

# OR Manual
pip install -r requirements.txt
python main.py
```

### Sample Data
```bash
# Docker
docker-compose exec bot python setup_sample_data.py

# Manual
python setup_sample_data.py
```

## 📈 Statistics

| Metric | Value |
|--------|-------|
| Total Files | 22 |
| Lines of Code | ~1,000 |
| Lines of Docs | ~1,900 |
| Dependencies | 4 |
| Admin Commands | 7+ |
| User Features | 6+ |
| Security Issues | 0 |
| License | MIT |

## 🎯 Use Cases

Perfect for selling:
- 🎬 Streaming accounts (Netflix, Disney+, Spotify)
- 💻 Software licenses (Canva Pro, Office 365)
- 🎮 Game accounts/items
- 📚 E-books and courses
- 🎟️ Digital vouchers
- 🔑 API keys and access codes
- 📱 App subscriptions

## 🌟 Highlights

✅ **Production Ready** - Fully functional and tested
✅ **Well Documented** - 7 comprehensive guides
✅ **Secure** - 0 vulnerabilities (CodeQL verified)
✅ **Scalable** - Handles thousands of users
✅ **Easy Deploy** - Docker + Multiple platforms
✅ **Open Source** - MIT License
✅ **Modular** - Easy to customize
✅ **Multi-language** - Ready for translation

## 🔗 Quick Links

- 📖 [Full Documentation](README.md)
- 🚀 [Quick Start Guide](QUICKSTART.md)
- 📝 [Usage Instructions](USAGE.md)
- 🐳 [Deployment Guide](DEPLOYMENT.md)
- ❓ [FAQ](FAQ.md)
- 🤝 [Contributing](CONTRIBUTING.md)

## 💡 Tips

1. Start with sample data to test the bot
2. Read QUICKSTART.md for fastest setup
3. Use Docker for easiest deployment
4. Check FAQ.md for common issues
5. Keep your .env file secure

## 🆘 Support

- 📋 [Open an Issue](https://github.com/yasirarism/telegram-auto-order-bot/issues)
- 💬 [Discussions](https://github.com/yasirarism/telegram-auto-order-bot/discussions)
- 📧 Contact via GitHub profile

---

**Ready to start?** → Read [QUICKSTART.md](QUICKSTART.md)

**Need help?** → Check [FAQ.md](FAQ.md)

**Want to deploy?** → See [DEPLOYMENT.md](DEPLOYMENT.md)

---

Made with ❤️ using Python & Pyrogram
