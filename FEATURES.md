# Bot Features Documentation

## User Interface Flow

### 1. Welcome Screen (/start)
When a user starts the bot, they see:

```
Halo, Yasir Store! Selamat datang di Arukaey Bot 👋🏻

╭  ◦ Total Pengguna Bot: 585 Orang
╰  ◦ Total Transaksi Berhasil: 6202x
```

**Inline Buttons:**
- 🏆 Top Products
- 👥 Top Buyers

**Custom Keyboard Menu:**
```
┌─────────────┬────────────────────┐
│  🏠 Start  │ 💬 Private Message │
├─────────────┼────────────────────┤
│ 📦 Catalog │    📊 Stock        │
├─────────────┼────────────────────┤
│👤 Account Info│   💰 Deposit     │
└─────────────┴────────────────────┘
```

### 2. Catalog View (📦 Catalog)
```
📦 Product Catalog

1. Basic Package
   💰 Price: Rp 25,000
   📦 Stock: 50 available

2. Standard Package
   💰 Price: Rp 50,000
   📦 Stock: 30 available

3. Premium Package
   💰 Price: Rp 100,000
   📦 Stock: 20 available

[Button: 1. Basic Package]
[Button: 2. Standard Package]
[Button: 3. Premium Package]
...
```

### 3. Product Detail View
When clicking on a product:

```
Premium Package

📝 Premium package with all features unlocked. Best value for money.

💰 Price: Rp 100,000
📦 Stock: 20 available

[Button: 🛒 Buy Now]
[Button: « Back to Catalog]
```

### 4. Purchase Flow
After clicking "🛒 Buy Now":

**If sufficient balance:**
```
✅ Purchase Successful!

Product: Premium Package
Price: Rp 100,000
New Balance: Rp 50,000

Thank you for your purchase!
```

**If insufficient balance:**
```
❌ Insufficient balance!

Product price: Rp 100,000
Your balance: Rp 25,000

Please deposit more funds.
```

### 5. Account Info (👤 Account Info)
```
👤 Account Information

Name: John Doe
Username: @johndoe
User ID: 123456789
💰 Balance: Rp 150,000
📊 Total Transactions: 5
```

### 6. Stock View (📊 Stock)
```
📊 Product Stock

Basic Package
   Stock: 50 ✅ Available

Standard Package
   Stock: 30 ✅ Available

Premium Package
   Stock: 0 ❌ Out of Stock
```

### 7. Deposit Info (💰 Deposit)
```
💰 Deposit Information

To add balance to your account, please contact the admin.

Admin will manually process your deposit request.

ℹ️ This is a manual balance system.
```

### 8. Top Products View
```
🏆 Top Products

1. Premium Package - 45 purchases
2. Standard Package - 32 purchases
3. Basic Package - 28 purchases
4. VIP Package - 15 purchases
5. Enterprise Package - 8 purchases
```

### 9. Top Buyers View
```
👥 Top Buyers

1. John Doe - 12 purchases
2. Jane Smith - 9 purchases
3. Bob Wilson - 7 purchases
4. Alice Brown - 6 purchases
5. Charlie Davis - 5 purchases
```

## Admin Interface

### 1. Admin Panel (/admin)
```
🔧 Admin Panel

Select an option:

[Button: 👥 View Users]
[Button: 💰 Add Balance]
[Button: 📦 Add Product]
[Button: 📊 Statistics]
```

### 2. Add Balance Command
```
Command: /addbalance 123456789 50000

Response:
✅ Balance Added Successfully

User: John Doe (ID: 123456789)
Amount Added: Rp 50,000
New Balance: Rp 200,000
```

### 3. Add Product Command
```
Command: /addproduct "New Product" 75000 15 "Amazing new product"

Response:
✅ Product Added Successfully

Name: New Product
Price: Rp 75,000
Stock: 15
Description: Amazing new product
```

### 4. Users List View
```
👥 User List

• John Doe (ID: 123456789)
  Balance: Rp 150,000

• Jane Smith (ID: 987654321)
  Balance: Rp 75,000

• Bob Wilson (ID: 456789123)
  Balance: Rp 200,000

... and 582 more users
```

### 5. Admin Statistics
```
📊 Bot Statistics

👥 Total Users: 585
📦 Total Products: 5
✅ Completed Transactions: 6202
```

## Command Reference

### User Commands
- `/start` - Start the bot and display welcome screen

### Admin Commands
- `/admin` - Open admin panel (admin only)
- `/addbalance <user_id> <amount>` - Add balance to user (admin only)
- `/addproduct <name> <price> <stock> [description]` - Add product (admin only)

## Button Actions

### Main Menu Buttons
- **🏠 Start** - Return to welcome screen
- **💬 Private Message** - Get admin contact info
- **📦 Catalog** - Browse available products
- **📊 Stock** - Check product stock levels
- **👤 Account Info** - View account details and balance
- **💰 Deposit** - View deposit instructions

### Inline Buttons
- **🏆 Top Products** - View most purchased products
- **👥 Top Buyers** - View users with most purchases
- **Product buttons** - View product details
- **🛒 Buy Now** - Purchase selected product
- **« Back to Catalog** - Return to catalog view

## Database Tables

### Users Table
- user_id (Primary Key)
- username
- first_name
- balance
- created_at

### Products Table
- product_id (Primary Key, Auto-increment)
- name
- description
- price
- stock
- created_at

### Transactions Table
- transaction_id (Primary Key, Auto-increment)
- user_id (Foreign Key)
- product_id (Foreign Key)
- amount
- status
- created_at

### Balance History Table
- history_id (Primary Key, Auto-increment)
- user_id (Foreign Key)
- amount
- type (deposit/purchase)
- admin_id
- created_at

## Error Handling

The bot handles various error scenarios:

1. **Product not found** - User-friendly error message
2. **Out of stock** - Prevents purchase and notifies user
3. **Insufficient balance** - Shows required vs available balance
4. **Invalid commands** - Usage instructions provided
5. **Unauthorized admin access** - Permission denied message
6. **Invalid input** - Validation error messages

## Security Features

1. **Admin Verification** - All admin commands check ADMIN_ID
2. **Balance Validation** - Prevents negative balances
3. **Stock Validation** - Prevents overselling
4. **User Authentication** - Built-in Telegram authentication
5. **Transaction Logging** - All transactions are tracked
