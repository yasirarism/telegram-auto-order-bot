"""Configuration module for the Telegram bot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# Database configuration
DATABASE_NAME = 'bot_database.db'

# Bot messages
WELCOME_MESSAGE = """Halo, Yasir Store! Selamat datang di Arukaey Bot 👋🏻

╭  ◦ Total Pengguna Bot: {total_users} Orang
╰  ◦ Total Transaksi Berhasil: {total_transactions}x"""

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set in .env file")
if ADMIN_ID == 0:
    raise ValueError("ADMIN_ID must be set in .env file")
