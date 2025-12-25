# Usage Examples

This file contains practical examples of how to use the Telegram Auto-Order Bot.

## Initial Setup Example

### Step 1: Install and Configure
```bash
# Clone the repository
git clone https://github.com/yasirarism/telegram-auto-order-bot.git
cd telegram-auto-order-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your BOT_TOKEN and ADMIN_ID
```

### Step 2: Initialize Database with Sample Products
```bash
python init_db.py
```

**Output:**
```
Adding sample products to database...
✓ Added: Basic Package - Rp 25,000
✓ Added: Standard Package - Rp 50,000
✓ Added: Premium Package - Rp 100,000
✓ Added: VIP Package - Rp 200,000
✓ Added: Enterprise Package - Rp 500,000

✓ Successfully added 5 sample products!

You can now start the bot with: python bot.py
```

### Step 3: Start the Bot
```bash
python bot.py
```

**Output:**
```
INFO - Starting bot...
```

## User Workflow Examples

### Example 1: New User Registration
1. User opens Telegram and searches for your bot
2. User sends `/start`
3. Bot responds with welcome message and statistics
4. User is automatically registered in the database

### Example 2: Browsing Products
1. User clicks "📦 Catalog" button
2. Bot displays all available products with inline buttons
3. User clicks on "Premium Package"
4. Bot shows detailed product information
5. User sees "🛒 Buy Now" button

### Example 3: Making a Purchase

**Scenario: User has sufficient balance**

1. Admin adds balance first:
   ```
   /addbalance 123456789 150000
   ```

2. User browses catalog and selects "Premium Package"

3. User clicks "🛒 Buy Now"

4. Bot processes purchase:
   - Checks balance (✓ 150,000 >= 100,000)
   - Deducts amount from balance
   - Reduces product stock
   - Creates transaction record
   - Sends confirmation

5. Bot responds:
   ```
   ✅ Purchase Successful!

   Product: Premium Package
   Price: Rp 100,000
   New Balance: Rp 50,000

   Thank you for your purchase!
   ```

**Scenario: User has insufficient balance**

1. User has balance: Rp 25,000
2. User tries to buy "Premium Package" (Rp 100,000)
3. Bot responds:
   ```
   ❌ Insufficient balance!

   Product price: Rp 100,000
   Your balance: Rp 25,000

   Please deposit more funds.
   ```

### Example 4: Checking Account Information
1. User clicks "👤 Account Info"
2. Bot displays:
   ```
   👤 Account Information

   Name: John Doe
   Username: @johndoe
   User ID: 123456789
   💰 Balance: Rp 50,000
   📊 Total Transactions: 1
   ```

### Example 5: Viewing Top Products and Buyers
1. User sends `/start`
2. User clicks "🏆 Top Products"
3. Bot shows ranking of most purchased products
4. User can click "👥 Top Buyers" to see top buyers

## Admin Workflow Examples

### Example 1: Adding Balance to User

**Command:**
```
/addbalance 123456789 100000
```

**Bot Response:**
```
✅ Balance Added Successfully

User: John Doe (ID: 123456789)
Amount Added: Rp 100,000
New Balance: Rp 150,000
```

**What happens in the database:**
- User balance updated: +100,000
- Balance history record created
- Admin ID logged for audit trail

### Example 2: Adding Multiple Products

**Add Basic Package:**
```
/addproduct "Basic Package" 25000 50 "Entry-level package with basic features"
```

**Add Premium Package:**
```
/addproduct "Premium Package" 100000 20 "Premium package with all features unlocked"
```

**Add VIP Package:**
```
/addproduct "VIP Package" 200000 10 "VIP package with exclusive benefits"
```

### Example 3: Using Admin Panel

1. Admin sends `/admin`
2. Bot shows admin panel with buttons
3. Admin clicks "👥 View Users"
4. Bot shows list of users with their balances
5. Admin clicks "📊 Statistics"
6. Bot shows:
   ```
   📊 Bot Statistics

   👥 Total Users: 585
   📦 Total Products: 5
   ✅ Completed Transactions: 6202
   ```

### Example 4: Managing User Accounts

**Scenario: User requests deposit**

1. User contacts admin via "💬 Private Message"
2. User provides payment proof
3. Admin verifies payment
4. Admin executes:
   ```
   /addbalance 123456789 50000
   ```
5. User receives balance update
6. User can now make purchases

### Example 5: Restocking Products

When a product runs out of stock, admin can add more:

**Option 1: Add new product with same name (creates duplicate)**
```
/addproduct "Premium Package" 100000 20 "Premium features"
```

**Option 2: Manually update database**
```python
# Run Python shell
python

# In Python shell:
from database import Database
db = Database()

# Update stock for product ID 3
product = db.get_product(3)
# Manually increase stock (would need to add this method)
# For now, admin needs to manage this through direct database access
```

## Advanced Usage Examples

### Example 1: Bulk User Balance Update

For promotional campaigns, admin can use a script:

```python
# bulk_balance.py
from database import Database
import config

db = Database()
users = db.get_all_users()

# Add 10,000 to all users
for user in users:
    db.update_balance(user['user_id'], 10000, admin_id=config.ADMIN_ID)
    print(f"Added Rp 10,000 to {user['first_name']}")
```

### Example 2: Transaction Report

Generate a simple transaction report:

```python
# report.py
from database import Database

db = Database()

print("=== Transaction Report ===\n")
print(f"Total Users: {db.get_total_users()}")
print(f"Total Transactions: {db.get_total_transactions()}")

print("\nTop 5 Products:")
for name, count in db.get_top_products(5):
    print(f"  - {name}: {count} purchases")

print("\nTop 5 Buyers:")
for user_id, name, count in db.get_top_buyers(5):
    print(f"  - {name}: {count} purchases")
```

### Example 3: Custom Product Categories

While not built-in, you could extend the database:

```python
# In database.py, add:
def add_product_with_category(self, name, description, price, stock, category):
    conn = self.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, stock, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, price, stock, category))
    conn.commit()
    conn.close()
```

## Testing Examples

### Test User Flow
```bash
# As a user (via Telegram):
1. /start
2. Click "📦 Catalog"
3. Click on a product
4. Try to buy (should fail - no balance)
5. Click "👤 Account Info" (should show 0 balance)

# As admin (via Telegram):
6. /addbalance YOUR_USER_ID 100000
7. Check balance again (should show 100,000)

# As user again:
8. Try to buy product (should succeed)
9. Check balance (should be reduced)
10. Check account info (should show 1 transaction)
```

### Test Admin Flow
```bash
# As admin:
1. /admin
2. Click "👥 View Users"
3. Click "📊 Statistics"
4. /addbalance USER_ID AMOUNT
5. /addproduct "Test" 1000 5 "Test product"
6. Check catalog to verify new product
```

## Common Scenarios

### Scenario 1: User Can't Afford Product
**User Action:** Tries to buy Premium Package (Rp 100,000)
**User Balance:** Rp 25,000
**Bot Response:** Shows insufficient balance message
**Solution:** User contacts admin for deposit

### Scenario 2: Product Out of Stock
**User Action:** Clicks on sold-out product
**Bot Response:** Shows product details without "Buy" button
**Admin Action:** Restocks using addproduct or database

### Scenario 3: User Wants Refund
**User Action:** Contacts admin
**Admin Action:** Manually adds balance back:
```
/addbalance USER_ID REFUND_AMOUNT
```

### Scenario 4: Wrong Balance Added
**Admin Action:** Add negative amount to correct:
```
# If added 100,000 instead of 10,000, remove 90,000:
# Note: Current implementation doesn't support negative amounts
# Admin would need to manually adjust database
```

## Tips and Best Practices

1. **For Users:**
   - Check balance before shopping
   - Contact admin for deposits
   - Use account info to track transactions
   - Check stock before contacting admin

2. **For Admins:**
   - Always verify payments before adding balance
   - Keep track of manual balance additions
   - Regularly check statistics
   - Monitor stock levels
   - Backup database regularly

3. **For Developers:**
   - Test with small amounts first
   - Keep the database backed up
   - Monitor bot logs for errors
   - Consider adding automated backups
   - Implement payment gateway for automation

## Error Handling Examples

### Invalid Admin Command
```
# Wrong usage:
/addbalance

# Bot response:
Usage: /addbalance <user_id> <amount>
Example: /addbalance 123456789 50000
```

### Invalid User ID
```
/addbalance 999999999 50000

# Bot response:
❌ User not found.
```

### Invalid Amount
```
/addbalance 123456789 abc

# Bot response:
❌ Invalid user ID or amount.
```

This comprehensive example guide should help users and admins understand how to effectively use the bot!
