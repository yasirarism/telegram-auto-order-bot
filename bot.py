"""Main Telegram bot implementation."""
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
import config
from database import Database

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()

# Conversation states
AWAITING_USER_ID, AWAITING_AMOUNT = range(2)

# Custom keyboard
def get_main_keyboard():
    """Get main keyboard layout."""
    keyboard = [
        ['🏠 Start', '💬 Private Message'],
        ['📦 Catalog', '📊 Stock'],
        ['👤 Account Info', '💰 Deposit'],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    
    # Add user to database
    db.add_user(user.id, user.username, user.first_name)
    
    # Get statistics
    total_users = db.get_total_users()
    total_transactions = db.get_total_transactions()
    
    # Create inline keyboard for Top Products and Top Buyers
    keyboard = [
        [
            InlineKeyboardButton("🏆 Top Products", callback_data='top_products'),
            InlineKeyboardButton("👥 Top Buyers", callback_data='top_buyers')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send welcome message
    welcome_text = config.WELCOME_MESSAGE.format(
        total_users=total_users,
        total_transactions=total_transactions
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )
    
    # Send main keyboard
    await update.message.reply_text(
        "Please select an option:",
        reply_markup=get_main_keyboard()
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu button presses."""
    text = update.message.text
    user = update.effective_user
    
    if text == '🏠 Start':
        await start(update, context)
    
    elif text == '💬 Private Message':
        await update.message.reply_text(
            f"Click here to message the admin: @admin\n\n"
            f"Or use this link to start a chat with admin ID: {config.ADMIN_ID}"
        )
    
    elif text == '📦 Catalog':
        await show_catalog(update, context)
    
    elif text == '📊 Stock':
        await show_stock(update, context)
    
    elif text == '👤 Account Info':
        await show_account_info(update, context)
    
    elif text == '💰 Deposit':
        await show_deposit_info(update, context)

async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product catalog."""
    products = db.get_all_products()
    
    if not products:
        await update.message.reply_text(
            "📦 No products available at the moment.\n"
            "Please check back later!"
        )
        return
    
    message = "📦 *Product Catalog*\n\n"
    
    # Create inline keyboard with product buttons
    keyboard = []
    for product in products:
        message += f"*{product['product_id']}. {product['name']}*\n"
        message += f"   💰 Price: Rp {product['price']:,.0f}\n"
        message += f"   📦 Stock: {product['stock']} available\n\n"
        
        keyboard.append([
            InlineKeyboardButton(
                f"{product['product_id']}. {product['name']}",
                callback_data=f"product_{product['product_id']}"
            )
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product stock."""
    products = db.get_all_products()
    
    if not products:
        await update.message.reply_text("📊 No products available.")
        return
    
    message = "📊 *Product Stock*\n\n"
    for product in products:
        status = "✅ Available" if product['stock'] > 0 else "❌ Out of Stock"
        message += f"*{product['name']}*\n"
        message += f"   Stock: {product['stock']} {status}\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def show_account_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user account information."""
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("❌ User not found.")
        return
    
    transactions = db.get_user_transactions(user.id)
    
    message = f"👤 *Account Information*\n\n"
    message += f"Name: {user_data['first_name']}\n"
    message += f"Username: @{user_data['username'] or 'N/A'}\n"
    message += f"User ID: {user_data['user_id']}\n"
    message += f"💰 Balance: Rp {user_data['balance']:,.0f}\n"
    message += f"📊 Total Transactions: {len(transactions)}\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def show_deposit_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show deposit information."""
    message = (
        "💰 *Deposit Information*\n\n"
        "To add balance to your account, please contact the admin.\n\n"
        "Admin will manually process your deposit request.\n\n"
        "ℹ️ This is a manual balance system."
    )
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'top_products':
        await show_top_products(query, context)
    
    elif query.data == 'top_buyers':
        await show_top_buyers(query, context)
    
    elif query.data.startswith('product_'):
        product_id = int(query.data.split('_')[1])
        await show_product_detail(query, context, product_id)
    
    elif query.data.startswith('buy_'):
        product_id = int(query.data.split('_')[1])
        await process_purchase(query, context, product_id)

async def show_top_products(query, context: ContextTypes.DEFAULT_TYPE):
    """Show top products."""
    top_products = db.get_top_products(10)
    
    if not top_products:
        await query.edit_message_text("🏆 No product data available yet.")
        return
    
    message = "🏆 *Top Products*\n\n"
    for idx, (name, count) in enumerate(top_products, 1):
        message += f"{idx}. {name} - {count} purchases\n"
    
    await query.edit_message_text(message, parse_mode='Markdown')

async def show_top_buyers(query, context: ContextTypes.DEFAULT_TYPE):
    """Show top buyers."""
    top_buyers = db.get_top_buyers(10)
    
    if not top_buyers:
        await query.edit_message_text("👥 No buyer data available yet.")
        return
    
    message = "👥 *Top Buyers*\n\n"
    for idx, (user_id, name, count) in enumerate(top_buyers, 1):
        message += f"{idx}. {name} - {count} purchases\n"
    
    await query.edit_message_text(message, parse_mode='Markdown')

async def show_product_detail(query, context: ContextTypes.DEFAULT_TYPE, product_id: int):
    """Show detailed product information."""
    product = db.get_product(product_id)
    
    if not product:
        await query.edit_message_text("❌ Product not found.")
        return
    
    message = f"*{product['name']}*\n\n"
    message += f"📝 {product['description']}\n\n"
    message += f"💰 Price: Rp {product['price']:,.0f}\n"
    message += f"📦 Stock: {product['stock']} available\n"
    
    keyboard = []
    if product['stock'] > 0:
        keyboard.append([
            InlineKeyboardButton("🛒 Buy Now", callback_data=f"buy_{product_id}")
        ])
    keyboard.append([
        InlineKeyboardButton("« Back to Catalog", callback_data="back_catalog")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def process_purchase(query, context: ContextTypes.DEFAULT_TYPE, product_id: int):
    """Process product purchase."""
    user = query.from_user
    product = db.get_product(product_id)
    
    if not product:
        await query.edit_message_text("❌ Product not found.")
        return
    
    if product['stock'] <= 0:
        await query.edit_message_text("❌ Product is out of stock.")
        return
    
    user_balance = db.get_user_balance(user.id)
    
    if user_balance < product['price']:
        await query.edit_message_text(
            f"❌ Insufficient balance!\n\n"
            f"Product price: Rp {product['price']:,.0f}\n"
            f"Your balance: Rp {user_balance:,.0f}\n\n"
            f"Please deposit more funds."
        )
        return
    
    # Process purchase
    db.update_balance(user.id, -product['price'])
    db.update_product_stock(product_id, 1)
    db.create_transaction(user.id, product_id, product['price'])
    
    new_balance = db.get_user_balance(user.id)
    
    await query.edit_message_text(
        f"✅ *Purchase Successful!*\n\n"
        f"Product: {product['name']}\n"
        f"Price: Rp {product['price']:,.0f}\n"
        f"New Balance: Rp {new_balance:,.0f}\n\n"
        f"Thank you for your purchase!",
        parse_mode='Markdown'
    )

# Admin commands
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel (admin only)."""
    user = update.effective_user
    
    if user.id != config.ADMIN_ID:
        await update.message.reply_text("❌ You don't have admin access.")
        return
    
    keyboard = [
        [InlineKeyboardButton("👥 View Users", callback_data='admin_users')],
        [InlineKeyboardButton("💰 Add Balance", callback_data='admin_add_balance')],
        [InlineKeyboardButton("📦 Add Product", callback_data='admin_add_product')],
        [InlineKeyboardButton("📊 Statistics", callback_data='admin_stats')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔧 *Admin Panel*\n\nSelect an option:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin callbacks."""
    query = update.callback_query
    
    # Check admin permission
    if query.from_user.id != config.ADMIN_ID:
        await query.answer("❌ Admin access required", show_alert=True)
        return
    
    await query.answer()
    
    if query.data == 'admin_users':
        await show_users_list(query, context)
    elif query.data == 'admin_add_balance':
        await query.edit_message_text(
            "💰 *Add Balance to User*\n\n"
            "Please use the command:\n"
            "`/addbalance <user_id> <amount>`\n\n"
            "Example: `/addbalance 123456789 50000`",
            parse_mode='Markdown'
        )
    elif query.data == 'admin_stats':
        await show_admin_stats(query, context)

async def show_users_list(query, context: ContextTypes.DEFAULT_TYPE):
    """Show list of users (admin only)."""
    users = db.get_all_users()
    
    if not users:
        await query.edit_message_text("No users found.")
        return
    
    message = "👥 *User List*\n\n"
    for user in users[:20]:  # Show first 20 users
        message += f"• {user['first_name']} (ID: {user['user_id']})\n"
        message += f"  Balance: Rp {user['balance']:,.0f}\n\n"
    
    if len(users) > 20:
        message += f"\n... and {len(users) - 20} more users"
    
    await query.edit_message_text(message, parse_mode='Markdown')

async def show_admin_stats(query, context: ContextTypes.DEFAULT_TYPE):
    """Show admin statistics."""
    total_users = db.get_total_users()
    total_transactions = db.get_total_transactions()
    products = db.get_all_products()
    
    message = f"📊 *Bot Statistics*\n\n"
    message += f"👥 Total Users: {total_users}\n"
    message += f"📦 Total Products: {len(products)}\n"
    message += f"✅ Completed Transactions: {total_transactions}\n"
    
    await query.edit_message_text(message, parse_mode='Markdown')

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add balance to user (admin only)."""
    user = update.effective_user
    
    if user.id != config.ADMIN_ID:
        await update.message.reply_text("❌ You don't have admin access.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /addbalance <user_id> <amount>\n"
            "Example: /addbalance 123456789 50000"
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        amount = float(context.args[1])
        
        if amount <= 0:
            await update.message.reply_text("❌ Amount must be positive.")
            return
        
        # Check if user exists
        target_user = db.get_user(target_user_id)
        if not target_user:
            await update.message.reply_text("❌ User not found.")
            return
        
        # Add balance
        db.update_balance(target_user_id, amount, admin_id=user.id)
        new_balance = db.get_user_balance(target_user_id)
        
        await update.message.reply_text(
            f"✅ *Balance Added Successfully*\n\n"
            f"User: {target_user['first_name']} (ID: {target_user_id})\n"
            f"Amount Added: Rp {amount:,.0f}\n"
            f"New Balance: Rp {new_balance:,.0f}",
            parse_mode='Markdown'
        )
        
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID or amount.")

async def add_product_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add product (admin only)."""
    user = update.effective_user
    
    if user.id != config.ADMIN_ID:
        await update.message.reply_text("❌ You don't have admin access.")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /addproduct <name> <price> <stock> [description]\n"
            'Example: /addproduct "Premium Package" 50000 10 "Premium features"'
        )
        return
    
    try:
        name = context.args[0]
        price = float(context.args[1])
        stock = int(context.args[2])
        description = ' '.join(context.args[3:]) if len(context.args) > 3 else "No description"
        
        db.add_product(name, description, price, stock)
        
        await update.message.reply_text(
            f"✅ *Product Added Successfully*\n\n"
            f"Name: {name}\n"
            f"Price: Rp {price:,.0f}\n"
            f"Stock: {stock}\n"
            f"Description: {description}",
            parse_mode='Markdown'
        )
        
    except ValueError:
        await update.message.reply_text("❌ Invalid price or stock value.")

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("addbalance", add_balance))
    application.add_handler(CommandHandler("addproduct", add_product_command))
    
    # Message handlers
    application.add_handler(MessageHandler(
        filters.Regex('^(🏠 Start|💬 Private Message|📦 Catalog|📊 Stock|👤 Account Info|💰 Deposit)$'),
        handle_menu
    ))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
