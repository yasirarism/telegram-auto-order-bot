import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "telegram_shop_bot")
    ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    
    # Bot settings
    OWNER_NAME = os.getenv("OWNER_NAME", "Yasir Store")
    BOT_NAME = os.getenv("BOT_NAME", "Arukaey Bot")
    MAX_PRODUCTS_PER_PAGE = 10
