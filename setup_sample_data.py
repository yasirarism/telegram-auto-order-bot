"""
Setup script to add sample products and stock for testing
"""

from database import db
from config import Config

def setup_sample_data():
    """Add sample products and stock to database"""
    
    print("🚀 Setting up sample data...\n")
    
    # Sample products
    products = [
        {
            "product_id": "netflix_premium",
            "name": "Netflix Premium",
            "description": "Akun Netflix Premium 1 Bulan\n✅ Garansi 30 hari\n✅ Akses penuh semua film dan series",
            "price": 50000,
            "category": "Streaming"
        },
        {
            "product_id": "spotify_premium",
            "name": "Spotify Premium",
            "description": "Akun Spotify Premium 1 Bulan\n✅ No ads\n✅ Download musik\n✅ High quality audio",
            "price": 30000,
            "category": "Music"
        },
        {
            "product_id": "youtube_premium",
            "name": "YouTube Premium",
            "description": "Akun YouTube Premium 1 Bulan\n✅ No ads\n✅ Background play\n✅ YouTube Music included",
            "price": 35000,
            "category": "Streaming"
        },
        {
            "product_id": "canva_pro",
            "name": "Canva Pro",
            "description": "Akun Canva Pro 1 Bulan\n✅ Premium templates\n✅ Background remover\n✅ Brand kit",
            "price": 40000,
            "category": "Design"
        },
        {
            "product_id": "disney_plus",
            "name": "Disney+ Hotstar",
            "description": "Akun Disney+ Hotstar 1 Bulan\n✅ Disney, Marvel, Star Wars\n✅ Live sports\n✅ HD streaming",
            "price": 45000,
            "category": "Streaming"
        }
    ]
    
    # Add products
    for product in products:
        if db.get_product(product["product_id"]):
            print(f"⏭️  Product '{product['name']}' already exists, skipping...")
        else:
            db.add_product(
                product["product_id"],
                product["name"],
                product["description"],
                product["price"],
                product["category"]
            )
            print(f"✅ Added product: {product['name']}")
    
    print("\n📦 Adding sample stock...\n")
    
    # Sample stock data
    stock_data = {
        "netflix_premium": [
            "Email: netflix1@example.com\nPassword: NetPass123!",
            "Email: netflix2@example.com\nPassword: NetPass456!",
            "Email: netflix3@example.com\nPassword: NetPass789!",
        ],
        "spotify_premium": [
            "Email: spotify1@example.com\nPassword: SpotPass123!",
            "Email: spotify2@example.com\nPassword: SpotPass456!",
        ],
        "youtube_premium": [
            "Email: youtube1@example.com\nPassword: YTPass123!",
            "Email: youtube2@example.com\nPassword: YTPass456!",
            "Email: youtube3@example.com\nPassword: YTPass789!",
        ],
        "canva_pro": [
            "Email: canva1@example.com\nPassword: CanvaPass123!",
        ],
        "disney_plus": [
            "Email: disney1@example.com\nPassword: DisneyPass123!",
            "Email: disney2@example.com\nPassword: DisneyPass456!",
        ]
    }
    
    # Add stock
    for product_id, stocks in stock_data.items():
        count = db.add_bulk_stock(product_id, stocks)
        print(f"✅ Added {count} stock items for {product_id}")
    
    print("\n✨ Sample data setup complete!")
    print("\n📊 Summary:")
    print(f"   - Total Products: {len(products)}")
    print(f"   - Total Stock Items: {sum(len(s) for s in stock_data.values())}")
    print("\n🎉 Bot is ready to use!")

if __name__ == "__main__":
    setup_sample_data()
