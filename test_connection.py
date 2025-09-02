#!/usr/bin/env python3
"""
Test script to verify MentWel platform connections
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        from app import create_app, db
        print("✅ Flask app imports successful")
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    try:
        from app.models import User, TherapySession, Payment, SentimentAnalysis, SessionPackage
        print("✅ Database models import successful")
    except ImportError as e:
        print(f"❌ Database models import failed: {e}")
        return False
    
    try:
        from config import config
        print("✅ Configuration import successful")
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import config
        
        # Test development config
        dev_config = config['development']
        print(f"✅ Development config loaded: {dev_config.__name__}")
        
        # Test production config
        prod_config = config['production']
        print(f"✅ Production config loaded: {prod_config.__name__}")
        
        # Test default config
        default_config = config['default']
        print(f"✅ Default config loaded: {default_config.__name__}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_app_creation():
    """Test Flask app creation"""
    print("\nTesting Flask app creation...")
    
    try:
        from app import create_app
        
        # Test development app
        app = create_app('development')
        print("✅ Development app created successfully")
        
        # Test production app
        app = create_app('production')
        print("✅ Production app created successfully")
        
        # Test default app
        app = create_app()
        print("✅ Default app created successfully")
        
        return True
    except Exception as e:
        print(f"❌ App creation test failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    try:
        from app import create_app, db
        
        app = create_app('development')
        
        with app.app_context():
            # Test database connection
            db.engine.execute('SELECT 1')
            print("✅ Database connection successful")
            
            # Test if tables can be created
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Clean up
            db.drop_all()
            print("✅ Database cleanup successful")
            
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        print("Note: Make sure MySQL is running and credentials are correct")
        return False

def test_routes():
    """Test route registration"""
    print("\nTesting route registration...")
    
    try:
        from app import create_app
        
        app = create_app('development')
        
        # Check if routes are registered
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.endpoint)
        
        expected_routes = ['main.index', 'main.dashboard', 'auth.register', 'auth.login', 'auth.logout']
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route {route} registered")
            else:
                print(f"⚠️  Route {route} not found")
        
        return True
    except Exception as e:
        print(f"❌ Route test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 MentWel Platform Connection Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_app_creation,
        test_routes,
        test_database_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MentWel platform is ready to run.")
        print("\nTo start the application:")
        print("1. python run.py")
        print("2. Open http://localhost:5000 in your browser")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("- MySQL not running")
        print("- Incorrect database credentials")
        print("- Missing environment variables")
        print("- Python dependencies not installed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
