from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List, Dict
from config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        
        # Collections
        self.users = self.db.users
        self.products = self.db.products
        self.transactions = self.db.transactions
        self.stocks = self.db.stocks
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        self.users.create_index("user_id", unique=True)
        self.products.create_index("product_id", unique=True)
        self.transactions.create_index("transaction_id", unique=True)
        self.stocks.create_index([("product_id", 1), ("is_used", 1)])
    
    # User operations
    def add_user(self, user_id: int, username: str = None, full_name: str = None) -> bool:
        """Add a new user to the database"""
        try:
            user_data = {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "balance": 0,
                "total_transactions": 0,
                "created_at": datetime.now(),
                "last_active": datetime.now()
            }
            self.users.insert_one(user_data)
            return True
        except:
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        return self.users.find_one({"user_id": user_id})
    
    def update_user_activity(self, user_id: int):
        """Update user's last active timestamp"""
        self.users.update_one(
            {"user_id": user_id},
            {"$set": {"last_active": datetime.now()}}
        )
    
    def update_user_balance(self, user_id: int, amount: float) -> bool:
        """Update user balance (can be positive or negative)"""
        result = self.users.update_one(
            {"user_id": user_id},
            {"$inc": {"balance": amount}}
        )
        return result.modified_count > 0
    
    def get_total_users(self) -> int:
        """Get total number of users"""
        return self.users.count_documents({})
    
    def get_top_buyers(self, limit: int = 10) -> List[Dict]:
        """Get top buyers by transaction count"""
        return list(self.users.find().sort("total_transactions", -1).limit(limit))
    
    # Product operations
    def add_product(self, product_id: str, name: str, description: str, price: float, 
                   category: str = "General") -> bool:
        """Add a new product"""
        try:
            product_data = {
                "product_id": product_id,
                "name": name,
                "description": description,
                "price": price,
                "category": category,
                "total_sold": 0,
                "is_active": True,
                "created_at": datetime.now()
            }
            self.products.insert_one(product_data)
            return True
        except:
            return False
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """Get product data"""
        return self.products.find_one({"product_id": product_id})
    
    def get_all_products(self, is_active: bool = True) -> List[Dict]:
        """Get all products"""
        query = {"is_active": is_active} if is_active is not None else {}
        return list(self.products.find(query))
    
    def get_products_with_stock(self) -> List[Dict]:
        """Get products that have available stock"""
        products = []
        for product in self.get_all_products(is_active=True):
            stock_count = self.get_available_stock_count(product["product_id"])
            if stock_count > 0:
                product["stock_count"] = stock_count
                products.append(product)
        return products
    
    def get_top_products(self, limit: int = 10) -> List[Dict]:
        """Get top products by sales"""
        return list(self.products.find({"is_active": True}).sort("total_sold", -1).limit(limit))
    
    def update_product_sales(self, product_id: str, quantity: int = 1):
        """Increment product sales count"""
        self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"total_sold": quantity}}
        )
    
    # Stock operations
    def add_stock(self, product_id: str, stock_data: str) -> bool:
        """Add stock item for a product"""
        try:
            stock_item = {
                "product_id": product_id,
                "data": stock_data,
                "is_used": False,
                "added_at": datetime.now(),
                "used_at": None,
                "used_by": None
            }
            self.stocks.insert_one(stock_item)
            return True
        except:
            return False
    
    def add_bulk_stock(self, product_id: str, stock_list: List[str]) -> int:
        """Add multiple stock items for a product"""
        count = 0
        for stock_data in stock_list:
            if self.add_stock(product_id, stock_data):
                count += 1
        return count
    
    def get_available_stock(self, product_id: str, quantity: int = 1) -> List[Dict]:
        """Get available stock items"""
        return list(self.stocks.find(
            {"product_id": product_id, "is_used": False}
        ).limit(quantity))
    
    def get_available_stock_count(self, product_id: str) -> int:
        """Get count of available stock"""
        return self.stocks.count_documents({"product_id": product_id, "is_used": False})
    
    def mark_stock_used(self, stock_id, user_id: int) -> bool:
        """Mark stock as used"""
        result = self.stocks.update_one(
            {"_id": stock_id},
            {
                "$set": {
                    "is_used": True,
                    "used_at": datetime.now(),
                    "used_by": user_id
                }
            }
        )
        return result.modified_count > 0
    
    # Transaction operations
    def create_transaction(self, transaction_id: str, user_id: int, product_id: str, 
                          amount: float, quantity: int = 1) -> bool:
        """Create a new transaction"""
        try:
            transaction_data = {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "product_id": product_id,
                "amount": amount,
                "quantity": quantity,
                "status": "completed",
                "created_at": datetime.now()
            }
            self.transactions.insert_one(transaction_data)
            
            # Update user transaction count
            self.users.update_one(
                {"user_id": user_id},
                {"$inc": {"total_transactions": quantity}}
            )
            
            return True
        except:
            return False
    
    def get_total_successful_transactions(self) -> int:
        """Get total count of successful transactions"""
        return self.transactions.count_documents({"status": "completed"})
    
    def get_user_transactions(self, user_id: int) -> List[Dict]:
        """Get all transactions for a user"""
        return list(self.transactions.find({"user_id": user_id}).sort("created_at", -1))

# Global database instance
db = Database()
