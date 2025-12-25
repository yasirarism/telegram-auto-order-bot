# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Get Your Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` to create a new bot
3. Follow the instructions to choose a name and username
4. Copy the bot token (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Get Your Telegram User ID
1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Send any message to it
3. Copy your user ID (a number like: `123456789`)

### 3. Setup the Bot
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your favorite editor
nano .env  # or use: vim .env, code .env, etc.
```

Add your credentials to `.env`:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_user_id_here
```

### 4. Initialize with Sample Data (Optional)
```bash
python init_db.py
```

This will create 5 sample products in the database.

### 5. Run the Bot
```bash
python bot.py
```

You should see:
```
INFO - Starting bot...
```

### 6. Test the Bot
1. Open Telegram
2. Search for your bot by username
3. Send `/start`

## Your First Steps

### As a User:
1. Click "📦 Catalog" to browse products
2. Click on any product to see details
3. Check "👤 Account Info" to see your balance (starts at 0)

### As an Admin:
1. Send `/admin` to open admin panel
2. Add balance to yourself:
   ```
   /addbalance YOUR_USER_ID 100000
   ```
3. Now you can make test purchases!
4. Add more products:
   ```
   /addproduct "Test Product" 10000 5 "This is a test product"
   ```

## Testing the Purchase Flow

1. Add balance to your account (as admin):
   ```
   /addbalance YOUR_USER_ID 100000
   ```

2. Browse catalog and click on a product

3. Click "🛒 Buy Now"

4. Check your account info to see updated balance and transaction

## Troubleshooting

**Bot doesn't start?**
- Make sure you copied the bot token correctly
- Check if there are any error messages
- Verify `.env` file exists and has correct values

**Admin commands don't work?**
- Double-check your ADMIN_ID in `.env`
- Restart the bot after changing `.env`
- Make sure you're using YOUR user ID, not the bot's ID

**"Module not found" error?**
- Run `pip install -r requirements.txt`
- Make sure you're in the correct directory

## Need Help?

Check the main [README.md](README.md) for detailed documentation.
