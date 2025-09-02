#!/usr/bin/env python3
"""
MentWel Setup Script
Helps configure the MentWel platform for first-time setup
"""

import os
import sys
import subprocess

def print_banner():
    """Print MentWel setup banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                        MentWel Setup                        ║
    ║              Digital Mental Health Platform                  ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        sys.exit(1)
    print("✅ Python version check passed")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        sys.exit(1)

def create_env_file():
    """Create .env file from template"""
    print("\n🔧 Creating environment configuration...")
    
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("Skipping .env creation")
            return
    
    env_content = """# MentWel Environment Configuration

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=mentwel-secret-key-change-in-production
DEBUG=True

# Database Configuration (use SQLite by default for quick start)
DATABASE_URL=sqlite:///instance/mentwel_dev.db
DEV_DATABASE_URL=sqlite:///instance/mentwel_dev.db

# PayStack Configuration
PAYSTACK_SECRET_KEY=sk_test_your_paystack_secret_key_here
PAYSTACK_PUBLIC_KEY=pk_test_your_paystack_public_key_here
PAYSTACK_BASE_URL=https://api.paystack.co

# Hugging Face Configuration
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Email Configuration (for password recovery)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com

# JWT Configuration
JWT_SECRET_KEY=jwt-secret-key-change-in-production
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created")
    print("⚠️  Please edit .env file with your actual API keys and database credentials")

def ensure_instance_dir():
    """Ensure instance directory for SQLite exists"""
    os.makedirs('instance', exist_ok=True)

def initialize_database():
    """Initialize database tables"""
    print("\n🗃️  Initializing database tables...")
    try:
        subprocess.check_call([sys.executable, "-m", "flask", "--app", "run.py", "init-db"])
        print("✅ Database tables created successfully")
    except subprocess.CalledProcessError:
        print("❌ Error creating database tables")
        return False
    return True

def seed_database():
    """Seed database with initial data"""
    print("\n🌱 Seeding database with initial data...")
    try:
        subprocess.check_call([sys.executable, "-m", "flask", "--app", "run.py", "seed-data"])
        print("✅ Database seeded successfully")
    except subprocess.CalledProcessError:
        print("❌ Error seeding database")
        return False
    return True

def create_admin_user():
    """Create admin user"""
    print("\n👤 Creating admin user...")
    try:
        subprocess.check_call([sys.executable, "-m", "flask", "--app", "run.py", "create-admin"])
        print("✅ Admin user created successfully")
        print("📝 Admin credentials: ADMIN001 / admin123")
    except subprocess.CalledProcessError:
        print("❌ Error creating admin user")
        return False
    return True

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running basic tests...")
    try:
        # Test database connection
        subprocess.check_call([sys.executable, "-c", """
from app import create_app, db
app = create_app()
with app.app_context():
    conn = db.engine.connect(); conn.execute(db.text('SELECT 1')); conn.close()
print('Database connection test passed')
        """])
        print("✅ Basic tests passed")
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        return False
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                        Setup Complete!                      ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🎉 MentWel has been set up successfully!
    
    📋 Next Steps:
    1. Edit .env file with your actual API keys:
       - PayStack API keys (for payments)
       - Hugging Face API key (for sentiment analysis)
       - Email configuration (for password recovery)
    
    2. Start the application:
       python run.py
    
    3. Access the platform:
       http://localhost:5000
    
    4. Login with admin credentials:
       Username: ADMIN001
       Password: admin123
    
    📚 Documentation:
    - README.md - Complete setup and usage guide
    - API endpoints are documented in the code
    
    🆘 Support:
    - Create an issue on GitHub
    - Email: support@mentwel.ng
    
    Happy coding! 🚀
    """)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()

    # Ensure instance directory for SQLite
    ensure_instance_dir()
    
    # Initialize database
    if not initialize_database():
        print("❌ Database initialization failed.")
        return
    
    # Seed database
    if not seed_database():
        print("❌ Database seeding failed.")
        return
    
    # Create admin user
    if not create_admin_user():
        print("❌ Admin user creation failed.")
        return
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed.")
        return
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
