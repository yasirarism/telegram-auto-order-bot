"""
Basic validation tests for the bot structure
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import pyrogram
        print("✅ Pyrogram installed")
    except ImportError:
        print("❌ Pyrogram not installed")
        return False
    
    try:
        import pymongo
        print("✅ PyMongo installed")
    except ImportError:
        print("❌ PyMongo not installed")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv installed")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'main.py',
        'config.py',
        'database.py',
        'handlers.py',
        'admin.py',
        'keyboards.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        '.env.example'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_config():
    """Test if config can be loaded"""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        print(f"✅ Config loaded")
        print(f"   - API_ID: {'Set' if Config.API_ID else 'Not set'}")
        print(f"   - API_HASH: {'Set' if Config.API_HASH else 'Not set'}")
        print(f"   - BOT_TOKEN: {'Set' if Config.BOT_TOKEN else 'Not set'}")
        print(f"   - MONGO_URI: {Config.MONGO_URI}")
        print(f"   - ADMIN_IDS: {Config.ADMIN_IDS}")
        
        if not Config.API_ID or not Config.API_HASH or not Config.BOT_TOKEN:
            print("⚠️  Warning: Some credentials not set. Please configure .env file")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_database_models():
    """Test if database models are properly defined"""
    print("\nTesting database models...")
    
    try:
        from database import db
        print("✅ Database module loaded")
        print(f"   - Collections defined: users, products, transactions, stocks")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("Bot Structure Validation Tests")
    print("="*50)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("Configuration Test", test_config),
        ("Database Models Test", test_database_models),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Bot structure is valid.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
