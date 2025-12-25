from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from database import db
from keyboards import (
    get_main_keyboard, 
    get_start_inline_keyboard,
    get_product_number_keyboard,
    get_checkout_keyboard,
    get_admin_deposit_keyboard
)
from config import Config
import uuid

# Store user session data
user_sessions = {}

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user = message.from_user
    
    # Add user to database if not exists
    existing_user = db.get_user(user.id)
    if not existing_user:
        db.add_user(user.id, user.username, user.first_name)
    else:
        db.update_user_activity(user.id)
    
    # Get statistics
    total_users = db.get_total_users()
    total_transactions = db.get_total_successful_transactions()
    
    welcome_text = f"""Halo, {Config.OWNER_NAME}! Selamat datang di {Config.BOT_NAME} 👋🏻

╭  ◦ Total Pengguna Bot: {total_users} Orang
╰  ◦ Total Transaksi Berhasil: {total_transactions}x"""
    
    await message.reply_text(
        welcome_text,
        reply_markup=get_start_inline_keyboard()
    )
    
    # Send main keyboard
    await message.reply_text(
        "Silakan pilih menu di bawah ini:",
        reply_markup=get_main_keyboard()
    )

@Client.on_message(filters.regex("^🏠 Start$") & filters.private)
async def menu_start(client: Client, message: Message):
    """Handle Start button"""
    await start_command(client, message)

@Client.on_message(filters.regex("^💬 Private Message$") & filters.private)
async def private_message(client: Client, message: Message):
    """Handle Private Message button"""
    if Config.ADMIN_IDS:
        admin_id = Config.ADMIN_IDS[0]
        admin_link = f"tg://user?id={admin_id}"
        await message.reply_text(
            f"💬 Untuk menghubungi admin, klik link berikut:\n{admin_link}",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.reply_text(
            "❌ Admin belum dikonfigurasi.",
            reply_markup=get_main_keyboard()
        )

@Client.on_message(filters.regex("^📦 Katalog$") & filters.private)
async def catalog_menu(client: Client, message: Message):
    """Handle Catalog button"""
    products = db.get_products_with_stock()
    
    if not products:
        await message.reply_text(
            "❌ Tidak ada produk yang tersedia saat ini.",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Show first page of products
    max_per_page = Config.MAX_PRODUCTS_PER_PAGE
    total_pages = (len(products) + max_per_page - 1) // max_per_page
    current_page = 0
    
    page_products = products[current_page * max_per_page:(current_page + 1) * max_per_page]
    
    # Store in session
    user_sessions[message.from_user.id] = {
        "products": products,
        "current_page": current_page
    }
    
    catalog_text = "📦 **Katalog Produk**\n\n"
    for i, product in enumerate(page_products, 1):
        catalog_text += f"{i}. **{product['name']}**\n"
        catalog_text += f"   💰 Harga: Rp {product['price']:,.0f}\n"
        catalog_text += f"   📊 Stok: {product['stock_count']}\n\n"
    
    catalog_text += "\n💡 Klik nomor produk untuk melihat detail dan membeli."
    
    await message.reply_text(
        catalog_text,
        reply_markup=get_product_number_keyboard(page_products, current_page, total_pages)
    )

@Client.on_message(filters.regex("^📊 Stok$") & filters.private)
async def stock_menu(client: Client, message: Message):
    """Handle Stock button"""
    products = db.get_all_products(is_active=True)
    
    if not products:
        await message.reply_text(
            "❌ Tidak ada produk yang tersedia saat ini.",
            reply_markup=get_main_keyboard()
        )
        return
    
    stock_text = "📊 **Stok Produk**\n\n"
    for product in products:
        stock_count = db.get_available_stock_count(product["product_id"])
        stock_text += f"▫️ **{product['name']}**\n"
        stock_text += f"   Stok: {stock_count} tersedia\n\n"
    
    await message.reply_text(
        stock_text,
        reply_markup=get_main_keyboard()
    )

@Client.on_message(filters.regex("^👤 Informasi Akun$") & filters.private)
async def account_info(client: Client, message: Message):
    """Handle Account Info button"""
    user = db.get_user(message.from_user.id)
    
    if not user:
        await message.reply_text(
            "❌ Akun tidak ditemukan. Silakan /start kembali.",
            reply_markup=get_main_keyboard()
        )
        return
    
    info_text = f"""👤 **Informasi Akun**

🆔 User ID: `{user['user_id']}`
👤 Nama: {user.get('full_name', 'N/A')}
📱 Username: @{user.get('username', 'N/A')}
💰 Saldo: Rp {user['balance']:,.0f}
📊 Total Transaksi: {user['total_transactions']}x"""
    
    await message.reply_text(
        info_text,
        reply_markup=get_main_keyboard()
    )

@Client.on_message(filters.regex("^💰 Deposit$") & filters.private)
async def deposit_menu(client: Client, message: Message):
    """Handle Deposit button"""
    if message.from_user.id in Config.ADMIN_IDS:
        await message.reply_text(
            "💰 **Panel Admin Deposit**\n\n"
            "Silakan kirim User ID untuk menambah saldo.\n"
            "Format: /deposit <user_id> <amount>\n\n"
            "Contoh: /deposit 123456789 50000",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.reply_text(
            "💰 **Deposit**\n\n"
            "Untuk menambah saldo, silakan hubungi admin melalui menu Private Message.",
            reply_markup=get_main_keyboard()
        )

@Client.on_message(filters.regex("^[0-9]+$") & filters.private)
async def product_number_handler(client: Client, message: Message):
    """Handle product number selection"""
    user_id = message.from_user.id
    
    if user_id not in user_sessions or "products" not in user_sessions[user_id]:
        await message.reply_text(
            "❌ Silakan buka katalog terlebih dahulu.",
            reply_markup=get_main_keyboard()
        )
        return
    
    try:
        number = int(message.text)
        session = user_sessions[user_id]
        current_page = session.get("current_page", 0)
        products = session["products"]
        max_per_page = Config.MAX_PRODUCTS_PER_PAGE
        
        page_products = products[current_page * max_per_page:(current_page + 1) * max_per_page]
        
        if number < 1 or number > len(page_products):
            await message.reply_text(
                "❌ Nomor produk tidak valid.",
                reply_markup=get_main_keyboard()
            )
            return
        
        product = page_products[number - 1]
        
        # Show product details
        product_text = f"""📦 **Detail Produk**

**{product['name']}**

{product['description']}

💰 Harga: Rp {product['price']:,.0f}
📊 Stok Tersedia: {product['stock_count']}

Klik "Beli Sekarang" untuk melakukan checkout."""
        
        await message.reply_text(
            product_text,
            reply_markup=get_checkout_keyboard(product["product_id"])
        )
        
    except ValueError:
        pass

@Client.on_message(filters.regex("^🔙 Kembali$") & filters.private)
async def back_button(client: Client, message: Message):
    """Handle back button"""
    await message.reply_text(
        "Menu Utama:",
        reply_markup=get_main_keyboard()
    )

@Client.on_callback_query(filters.regex("^top_products$"))
async def top_products_callback(client: Client, callback_query: CallbackQuery):
    """Handle top products callback"""
    products = db.get_top_products(10)
    
    if not products:
        await callback_query.answer("Belum ada data produk.", show_alert=True)
        return
    
    text = "🏆 **Top 10 Produk Terlaris**\n\n"
    for i, product in enumerate(products, 1):
        text += f"{i}. **{product['name']}**\n"
        text += f"   📊 Terjual: {product['total_sold']}x\n"
        text += f"   💰 Harga: Rp {product['price']:,.0f}\n\n"
    
    await callback_query.message.reply_text(text)
    await callback_query.answer()

@Client.on_callback_query(filters.regex("^top_buyers$"))
async def top_buyers_callback(client: Client, callback_query: CallbackQuery):
    """Handle top buyers callback"""
    buyers = db.get_top_buyers(10)
    
    if not buyers:
        await callback_query.answer("Belum ada data pembeli.", show_alert=True)
        return
    
    text = "👥 **Top 10 Pembeli**\n\n"
    for i, buyer in enumerate(buyers, 1):
        text += f"{i}. {buyer.get('full_name', 'N/A')}\n"
        text += f"   📊 Transaksi: {buyer['total_transactions']}x\n\n"
    
    await callback_query.message.reply_text(text)
    await callback_query.answer()

@Client.on_callback_query(filters.regex("^buy_(.+)$"))
async def buy_product_callback(client: Client, callback_query: CallbackQuery):
    """Handle buy product callback"""
    product_id = callback_query.data.split("_", 1)[1]
    user_id = callback_query.from_user.id
    
    product = db.get_product(product_id)
    user = db.get_user(user_id)
    
    if not product or not user:
        await callback_query.answer("❌ Data tidak ditemukan.", show_alert=True)
        return
    
    # Check stock
    available_stock = db.get_available_stock(product_id, 1)
    if not available_stock:
        await callback_query.answer("❌ Stok habis.", show_alert=True)
        return
    
    # Check balance
    if user["balance"] < product["price"]:
        await callback_query.answer(
            f"❌ Saldo tidak cukup. Saldo Anda: Rp {user['balance']:,.0f}",
            show_alert=True
        )
        return
    
    # Process purchase
    stock_item = available_stock[0]
    transaction_id = str(uuid.uuid4())
    
    # Deduct balance
    db.update_user_balance(user_id, -product["price"])
    
    # Mark stock as used
    db.mark_stock_used(stock_item["_id"], user_id)
    
    # Create transaction
    db.create_transaction(transaction_id, user_id, product_id, product["price"], 1)
    
    # Update product sales
    db.update_product_sales(product_id, 1)
    
    # Send product data to user
    success_text = f"""✅ **Pembelian Berhasil!**

📦 Produk: {product['name']}
💰 Harga: Rp {product['price']:,.0f}
🆔 ID Transaksi: `{transaction_id}`

**Data Produk:**
```
{stock_item['data']}
```

Terima kasih atas pembelian Anda! 🎉"""
    
    await callback_query.message.reply_text(success_text)
    await callback_query.answer("✅ Pembelian berhasil!", show_alert=True)

@Client.on_callback_query(filters.regex("^cancel_checkout$"))
async def cancel_checkout_callback(client: Client, callback_query: CallbackQuery):
    """Handle cancel checkout callback"""
    await callback_query.message.delete()
    await callback_query.answer("❌ Checkout dibatalkan.")

@Client.on_message(filters.command("deposit") & filters.private)
async def admin_deposit_command(client: Client, message: Message):
    """Handle admin deposit command"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("❌ Anda tidak memiliki akses ke fitur ini.")
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 3:
            await message.reply_text(
                "❌ Format salah.\nGunakan: /deposit <user_id> <amount>"
            )
            return
        
        target_user_id = int(parts[1])
        amount = float(parts[2])
        
        if amount <= 0:
            await message.reply_text("❌ Jumlah harus lebih dari 0.")
            return
        
        user = db.get_user(target_user_id)
        if not user:
            await message.reply_text("❌ User tidak ditemukan.")
            return
        
        db.update_user_balance(target_user_id, amount)
        
        await message.reply_text(
            f"✅ Berhasil menambah saldo Rp {amount:,.0f} ke user {target_user_id}"
        )
        
        # Notify user
        try:
            await client.send_message(
                target_user_id,
                f"💰 **Deposit Berhasil!**\n\nSaldo Anda telah ditambah sebesar Rp {amount:,.0f}"
            )
        except:
            pass
            
    except ValueError:
        await message.reply_text("❌ Format salah. User ID dan amount harus berupa angka.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
