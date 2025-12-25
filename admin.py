from pyrogram import Client, filters
from pyrogram.types import Message
from database import db
from config import Config
from keyboards import get_main_keyboard

@Client.on_message(filters.command("addproduct") & filters.private)
async def add_product_command(client: Client, message: Message):
    """Handle add product command (admin only)"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("❌ Anda tidak memiliki akses ke fitur ini.")
        return
    
    await message.reply_text(
        """📦 **Tambah Produk Baru**

Format:
```
/addproduct
product_id|nama|harga|deskripsi
```

Contoh:
```
/addproduct
netflix_premium|Netflix Premium|50000|Akun Netflix Premium 1 Bulan
```"""
    )

@Client.on_message(filters.command("addstock") & filters.private)
async def add_stock_command(client: Client, message: Message):
    """Handle add stock command (admin only)"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("❌ Anda tidak memiliki akses ke fitur ini.")
        return
    
    await message.reply_text(
        """📊 **Tambah Stok**

Format untuk 1 stok:
```
/addstock product_id
data_stok
```

Contoh:
```
/addstock netflix_premium
email: test@example.com
password: password123
```

Format untuk multiple stok (kirim beberapa pesan):
```
/addstock product_id
data_stok_1

data_stok_2

data_stok_3
```"""
    )

@Client.on_message(filters.command("listproducts") & filters.private)
async def list_products_command(client: Client, message: Message):
    """Handle list products command (admin only)"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("❌ Anda tidak memiliki akses ke fitur ini.")
        return
    
    products = db.get_all_products(is_active=None)
    
    if not products:
        await message.reply_text("❌ Tidak ada produk.")
        return
    
    text = "📦 **Daftar Produk**\n\n"
    for product in products:
        stock_count = db.get_available_stock_count(product["product_id"])
        status = "✅" if product["is_active"] else "❌"
        text += f"{status} **{product['name']}** (`{product['product_id']}`)\n"
        text += f"   💰 Rp {product['price']:,.0f}\n"
        text += f"   📊 Stok: {stock_count}\n"
        text += f"   📈 Terjual: {product['total_sold']}x\n\n"
    
    await message.reply_text(text)

@Client.on_message(filters.command("listusers") & filters.private)
async def list_users_command(client: Client, message: Message):
    """Handle list users command (admin only)"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("❌ Anda tidak memiliki akses ke fitur ini.")
        return
    
    users = list(db.users.find().sort("created_at", -1).limit(20))
    
    if not users:
        await message.reply_text("❌ Tidak ada user.")
        return
    
    text = "👥 **Daftar User (20 Terbaru)**\n\n"
    for user in users:
        text += f"🆔 {user['user_id']} - {user.get('full_name', 'N/A')}\n"
        text += f"   💰 Saldo: Rp {user['balance']:,.0f}\n"
        text += f"   📊 Transaksi: {user['total_transactions']}x\n\n"
    
    await message.reply_text(text)

@Client.on_message(filters.command("stats") & filters.private)
async def stats_command(client: Client, message: Message):
    """Handle stats command (admin only)"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("❌ Anda tidak memiliki akses ke fitur ini.")
        return
    
    total_users = db.get_total_users()
    total_transactions = db.get_total_successful_transactions()
    total_products = db.products.count_documents({})
    
    # Calculate total revenue
    transactions = list(db.transactions.find({"status": "completed"}))
    total_revenue = sum(t["amount"] for t in transactions)
    
    text = f"""📊 **Statistik Bot**

👥 Total Pengguna: {total_users}
📦 Total Produk: {total_products}
✅ Total Transaksi: {total_transactions}
💰 Total Pendapatan: Rp {total_revenue:,.0f}"""
    
    await message.reply_text(text)

@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_command(client: Client, message: Message):
    """Handle broadcast command (admin only)"""
    if message.from_user.id not in Config.ADMIN_IDS:
        await message.reply_text("❌ Anda tidak memiliki akses ke fitur ini.")
        return
    
    if not message.reply_to_message:
        await message.reply_text(
            "❌ Reply ke pesan yang ingin di-broadcast dengan /broadcast"
        )
        return
    
    users = list(db.users.find())
    success = 0
    failed = 0
    
    status_msg = await message.reply_text(f"📢 Broadcasting ke {len(users)} users...")
    
    for user in users:
        try:
            await message.reply_to_message.copy(user["user_id"])
            success += 1
        except:
            failed += 1
    
    await status_msg.edit_text(
        f"✅ Broadcast selesai!\n\n"
        f"✅ Berhasil: {success}\n"
        f"❌ Gagal: {failed}"
    )

# Handler for processing product addition from admin
@Client.on_message(filters.text & filters.private & filters.reply)
async def handle_product_addition(client: Client, message: Message):
    """Handle product addition via reply"""
    if message.from_user.id not in Config.ADMIN_IDS:
        return
    
    if not message.reply_to_message or not message.reply_to_message.text:
        return
    
    if "/addproduct" in message.reply_to_message.text:
        try:
            parts = message.text.strip().split("|")
            if len(parts) != 4:
                await message.reply_text("❌ Format salah. Harus ada 4 bagian yang dipisahkan dengan |")
                return
            
            product_id, name, price, description = parts
            price = float(price)
            
            if db.add_product(product_id.strip(), name.strip(), description.strip(), price):
                await message.reply_text(
                    f"✅ Produk berhasil ditambahkan!\n\n"
                    f"ID: `{product_id.strip()}`\n"
                    f"Nama: {name.strip()}\n"
                    f"Harga: Rp {price:,.0f}"
                )
            else:
                await message.reply_text("❌ Gagal menambahkan produk. Mungkin ID sudah ada.")
        except ValueError:
            await message.reply_text("❌ Format harga salah.")
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")
    
    elif "/addstock" in message.reply_to_message.text:
        try:
            lines = message.text.strip().split("\n")
            if len(lines) < 2:
                await message.reply_text("❌ Format salah. Minimal 2 baris (product_id dan data).")
                return
            
            product_id = lines[0].strip()
            
            # Check if product exists
            product = db.get_product(product_id)
            if not product:
                await message.reply_text(f"❌ Produk dengan ID `{product_id}` tidak ditemukan.")
                return
            
            # Split by empty lines for multiple stock items
            stock_data = "\n".join(lines[1:])
            stock_items = [s.strip() for s in stock_data.split("\n\n") if s.strip()]
            
            if not stock_items:
                stock_items = [stock_data]
            
            count = db.add_bulk_stock(product_id, stock_items)
            
            await message.reply_text(
                f"✅ Berhasil menambahkan {count} stok untuk produk `{product_id}`"
            )
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")
