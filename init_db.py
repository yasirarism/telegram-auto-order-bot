"""Initialize database with sample data for testing."""
from database import Database

def init_sample_data():
    """Initialize database with sample products."""
    db = Database()
    
    # Check if products already exist
    existing_products = db.get_all_products()
    if existing_products:
        print(f"Database already has {len(existing_products)} products.")
        response = input("Do you want to add more sample products? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Sample products
    sample_products = [
        {
            'name': 'Basic Package',
            'description': 'Entry-level package with basic features. Perfect for beginners.',
            'price': 25000,
            'stock': 50
        },
        {
            'name': 'Standard Package',
            'description': 'Standard package with advanced features. Great for regular users.',
            'price': 50000,
            'stock': 30
        },
        {
            'name': 'Premium Package',
            'description': 'Premium package with all features unlocked. Best value for money.',
            'price': 100000,
            'stock': 20
        },
        {
            'name': 'VIP Package',
            'description': 'VIP package with exclusive benefits and priority support.',
            'price': 200000,
            'stock': 10
        },
        {
            'name': 'Enterprise Package',
            'description': 'Enterprise solution with custom features and dedicated support.',
            'price': 500000,
            'stock': 5
        }
    ]
    
    print("\nAdding sample products to database...")
    for product in sample_products:
        db.add_product(
            name=product['name'],
            description=product['description'],
            price=product['price'],
            stock=product['stock']
        )
        print(f"✓ Added: {product['name']} - Rp {product['price']:,.0f}")
    
    print(f"\n✓ Successfully added {len(sample_products)} sample products!")
    print("\nYou can now start the bot with: python bot.py")

if __name__ == '__main__':
    init_sample_data()
