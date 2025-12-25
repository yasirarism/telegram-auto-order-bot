"""Database module for managing users, products, and transactions."""
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
import config

class Database:
    """Database handler for the Telegram bot."""
    
    def __init__(self, db_name: str = config.DATABASE_NAME):
        """Initialize database connection."""
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                balance REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')
        
        # Balance history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS balance_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                admin_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # User operations
    def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add a new user or update existing user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, first_name))
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_user_balance(self, user_id: int) -> float:
        """Get user balance."""
        user = self.get_user(user_id)
        return user['balance'] if user else 0.0
    
    def update_balance(self, user_id: int, amount: float, admin_id: int = None):
        """Update user balance."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET balance = balance + ? WHERE user_id = ?
        ''', (amount, user_id))
        
        # Record balance change
        cursor.execute('''
            INSERT INTO balance_history (user_id, amount, type, admin_id)
            VALUES (?, ?, ?, ?)
        ''', (user_id, amount, 'deposit' if amount > 0 else 'purchase', admin_id))
        
        conn.commit()
        conn.close()
    
    def get_total_users(self) -> int:
        """Get total number of users."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM users')
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0
    
    def get_all_users(self) -> List[dict]:
        """Get all users."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Product operations
    def add_product(self, name: str, description: str, price: float, stock: int = 0):
        """Add a new product."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, description, price, stock)
            VALUES (?, ?, ?, ?)
        ''', (name, description, price, stock))
        conn.commit()
        conn.close()
    
    def get_product(self, product_id: int) -> Optional[dict]:
        """Get product information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_all_products(self) -> List[dict]:
        """Get all products."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products ORDER BY product_id')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def update_product_stock(self, product_id: int, quantity: int):
        """Update product stock."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products SET stock = stock - ? WHERE product_id = ?
        ''', (quantity, product_id))
        conn.commit()
        conn.close()
    
    # Transaction operations
    def create_transaction(self, user_id: int, product_id: int, amount: float) -> int:
        """Create a new transaction."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (user_id, product_id, amount, status)
            VALUES (?, ?, ?, 'completed')
        ''', (user_id, product_id, amount))
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return transaction_id
    
    def get_total_transactions(self) -> int:
        """Get total number of completed transactions."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM transactions WHERE status = 'completed'")
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0
    
    def get_user_transactions(self, user_id: int) -> List[dict]:
        """Get user transaction history."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, p.name as product_name
            FROM transactions t
            JOIN products p ON t.product_id = p.product_id
            WHERE t.user_id = ?
            ORDER BY t.created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_top_buyers(self, limit: int = 10) -> List[Tuple[int, str, int]]:
        """Get top buyers by transaction count."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.user_id, u.first_name, COUNT(t.transaction_id) as total
            FROM users u
            JOIN transactions t ON u.user_id = t.user_id
            WHERE t.status = 'completed'
            GROUP BY u.user_id
            ORDER BY total DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [(row['user_id'], row['first_name'], row['total']) for row in rows]
    
    def get_top_products(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get top products by purchase count."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.name, COUNT(t.transaction_id) as total
            FROM products p
            JOIN transactions t ON p.product_id = t.product_id
            WHERE t.status = 'completed'
            GROUP BY p.product_id
            ORDER BY total DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [(row['name'], row['total']) for row in rows]
