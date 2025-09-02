#!/usr/bin/env python3
"""
Database initialization script for MentWel platform
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize the database"""
    try:
        print("🗄️  Initializing MentWel database...")
        
        # Import app and database
        from app import create_app, db
        from app.models import User, TherapySession, Payment, SentimentAnalysis, SessionPackage
        
        # Create app context
        app = create_app('development')
        
        with app.app_context():
            print("✅ App context created")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created")
            
            # Create initial session packages
            packages = [
                SessionPackage(
                    package_name='Single Session',
                    package_description='One therapy session',
                    session_count=1,
                    package_duration_days=30,
                    package_price=5000.00
                ),
                SessionPackage(
                    package_name='Starter Pack',
                    package_description='3 therapy sessions',
                    session_count=3,
                    package_duration_days=90,
                    package_price=13500.00
                ),
                SessionPackage(
                    package_name='Monthly Plan',
                    package_description='8 therapy sessions per month',
                    session_count=8,
                    package_duration_days=30,
                    package_price=32000.00
                ),
                SessionPackage(
                    package_name='Quarterly Plan',
                    package_description='24 therapy sessions over 3 months',
                    session_count=24,
                    package_duration_days=90,
                    package_price=90000.00
                )
            ]
            
            for package in packages:
                db.session.add(package)
            
            db.session.commit()
            print("✅ Session packages created")

            # Seed a default verified therapist if none exists
            from app.models import User
            existing_therapist = User.query.filter_by(is_therapist=True).first()
            if not existing_therapist:
                import bcrypt
                print("👩‍⚕️  Creating a default verified therapist for development...")
                pwd = 'therapist123'
                password_hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                therapist = User(
                    is_anonymous=False,
                    is_therapist=True,
                    therapist_verified=True,
                    therapist_specialization='General Counseling',
                    therapist_bio='Experienced licensed therapist available for sessions.',
                    therapist_rating=4.8,
                    therapist_sessions_count=0,
                    email='therapist@mentwel.ng',
                    phone_number=None,
                    password_hash=password_hash
                )
                db.session.add(therapist)
                db.session.commit()
                print("✅ Default therapist created: therapist@mentwel.ng / therapist123")
            
            print("\n🎉 Database initialization completed successfully!")
            print("📊 Created tables:")
            print("   - users")
            print("   - therapy_sessions")
            print("   - payments")
            print("   - sentiment_analysis")
            print("   - session_packages")
            
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("💡 Common issues:")
        print("   - MySQL not running")
        print("   - Incorrect database credentials")
        print("   - Database doesn't exist")
        return False

def create_admin_user():
    """Create an admin user"""
    try:
        print("\n👤 Creating admin user...")
        
        from app import create_app, db
        from app.models import User
        import bcrypt
        
        app = create_app('development')
        
        with app.app_context():
            # Check if admin already exists
            admin = User.query.filter_by(anonymous_id='ADMIN001').first()
            if admin:
                print("✅ Admin user already exists")
                return True
            
            # Create admin user
            password = 'admin123'
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            admin_user = User(
                anonymous_id='ADMIN001',
                password_hash=password_hash.decode('utf-8'),
                email='admin@mentwel.ng',
                is_anonymous=False,
                is_therapist=False
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Admin user created successfully")
            print("📝 Admin credentials:")
            print("   Username: ADMIN001")
            print("   Password: admin123")
            
            return True
            
    except Exception as e:
        print(f"❌ Admin user creation failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 MentWel Database Initialization")
    print("=" * 50)
    
    # Initialize database
    if not init_database():
        return False
    
    # Create admin user
    if not create_admin_user():
        return False
    
    print("\n🎉 MentWel platform is ready!")
    print("\nNext steps:")
    print("1. Start the application: python start.py")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Login with admin credentials")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
