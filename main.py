from pyrogram import Client
from config import Config
import logging
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create bot instance
app = Client(
    "telegram_shop_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

def main():
    """Main function to run the bot"""
    logger.info("Starting Telegram Shop Bot...")
    
    # Import handlers to register them
    import handlers
    import admin
    
    logger.info("Bot handlers loaded successfully")
    
    # Run the bot
    app.run()

if __name__ == "__main__":
    main()
