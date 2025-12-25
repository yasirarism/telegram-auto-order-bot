# Telegram Auto-Order Bot

A comprehensive Telegram bot for automatic ordering with a manual balance system, product catalog, and admin panel.

## Features

### User Features
- **Welcome Screen**: Displays total users and successful transactions
- **Custom Keyboard Menu**: Easy navigation with buttons for:
  - 🏠 Start - Return to main menu
  - 💬 Private Message - Contact admin directly
  - 📦 Catalog - Browse available products
  - 📊 Stock - Check product availability
  - 👤 Account Info - View balance and transaction history
  - 💰 Deposit - Information about adding balance

- **Product Browsing**: Interactive catalog with inline buttons
- **Product Details**: Detailed product information with buy option
- **Order Processing**: Automatic balance deduction and stock management
- **Transaction History**: Track all purchases

### Admin Features
- **Admin Panel**: Comprehensive admin interface
- **Manual Balance Top-up**: Add balance to any user account
- **Product Management**: Add new products with stock and pricing
- **User Management**: View all users and their balances
- **Statistics Dashboard**: View bot usage statistics
- **Top Products & Top Buyers**: Rankings based on transactions

## Installation

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Your Telegram User ID (admin)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yasirarism/telegram-auto-order-bot.git
   cd telegram-auto-order-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   BOT_TOKEN=your_bot_token_from_botfather
   ADMIN_ID=your_telegram_user_id
   ```

   **How to get your Telegram User ID:**
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - It will reply with your user ID

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Usage

### For Users

1. **Start the bot**: Send `/start` to the bot
2. **Browse products**: Click "📦 Catalog" to see available products
3. **Check stock**: Click "📊 Stock" to see product availability
4. **View account**: Click "👤 Account Info" to see your balance
5. **Make a purchase**: 
   - Browse the catalog
   - Click on a product to see details
   - Click "🛒 Buy Now" to purchase (requires sufficient balance)

### For Admins

1. **Access admin panel**: Send `/admin` to the bot
2. **Add balance to user**:
   ```
   /addbalance <user_id> <amount>
   Example: /addbalance 123456789 50000
   ```

3. **Add a new product**:
   ```
   /addproduct <name> <price> <stock> [description]
   Example: /addproduct "Premium Package" 50000 10 "Premium features included"
   ```

4. **View statistics**: Use the admin panel buttons

## Project Structure

```
telegram-auto-order-bot/
├── bot.py              # Main bot implementation
├── database.py         # Database operations
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Database Schema

The bot uses SQLite with the following tables:

- **users**: User information and balances
- **products**: Product catalog with pricing and stock
- **transactions**: Purchase history
- **balance_history**: Balance change tracking

## Commands

### User Commands
- `/start` - Start the bot and show welcome screen

### Admin Commands
- `/admin` - Open admin panel
- `/addbalance <user_id> <amount>` - Add balance to user
- `/addproduct <name> <price> <stock> [description]` - Add new product

## Features in Detail

### Manual Balance System
- Admin manually tops up user balances
- All balance changes are tracked in history
- Users can view their current balance anytime

### Product Management
- Products have name, description, price, and stock
- Stock automatically decreases with purchases
- Out-of-stock products cannot be purchased

### Transaction Processing
- Automatic balance verification
- Stock availability check
- Instant transaction completion
- Transaction history tracking

### Statistics & Rankings
- Total users count
- Total successful transactions
- Top products by purchase count
- Top buyers by transaction count

## Security

- Admin commands are restricted to configured ADMIN_ID
- User authentication through Telegram
- Balance validation before purchases
- Stock validation before sales

## Future Enhancements

This bot is designed to be modular and scalable. Potential additions:

- Payment gateway integration (e.g., Stripe, PayPal)
- Automated deposit processing
- Multi-admin support
- Product categories
- Discount codes
- Referral system
- Order notifications
- Product images
- CSV export for reports

## Troubleshooting

### Bot doesn't respond
- Check if BOT_TOKEN is correct
- Ensure the bot is running (`python bot.py`)
- Check internet connection

### Admin commands don't work
- Verify ADMIN_ID in `.env` matches your Telegram user ID
- Restart the bot after changing `.env`

### Database errors
- Ensure write permissions in the bot directory
- Delete `bot_database.db` to reset (will lose all data)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Support

For support, please open an issue on GitHub or contact the repository owner.
