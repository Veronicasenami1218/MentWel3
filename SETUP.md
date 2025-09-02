# MentWel Platform Setup Guide

This guide will help you set up and run the MentWel digital mental health platform on your local machine.

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have the following installed:
- **Python 3.8+**
- **MySQL 8.0+**
- **Git**

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd mentwel

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Using the Setup Script
```bash
# Run the automated setup
python setup.py
```

#### Option B: Manual Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE mentwel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Initialize database tables
python init_db.py
```

### 4. Start the Application

```bash
# Start the development server
python start.py
```

Open your browser and go to: **http://localhost:5000**

## 🔧 Manual Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost/mentwel_db

# Paystack Configuration (for payments)
PAYSTACK_SECRET_KEY=<your-paystack-secret-key>
PAYSTACK_PUBLIC_KEY=<your-paystack-public-key>

# Hugging Face Configuration (for AI analysis)
HUGGINGFACE_API_KEY=<your-huggingface-api-key>

# Email Configuration (for password recovery)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### Database Configuration

1. **Install MySQL** if you haven't already
2. **Create Database:**
   ```sql
   CREATE DATABASE mentwel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. **Create User (Optional):**
   ```sql
   CREATE USER 'mentwel_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON mentwel_db.* TO 'mentwel_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

## 📁 Project Structure

```
mentwel/
├── app/                    # Flask application
│   ├── __init__.py        # App factory
│   ├── models.py          # Database models
│   ├── auth.py            # Authentication routes
│   ├── payments.py        # Payment routes
│   ├── ai_analysis.py     # AI analysis routes
│   └── routes.py          # Main routes
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images and logos
├── templates/              # HTML templates
│   ├── index.html         # Landing page
│   └── dashboard.html     # User dashboard
├── database/               # Database files
│   └── schema.sql         # Database schema
├── tests/                  # Test files
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── setup.py               # Automated setup
├── start.py               # Quick start script
├── init_db.py             # Database initialization
└── run.py                 # Main application entry
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_app.py
```

### Test Database Connection
```bash
python -c "
from app import create_app, db
app = create_app('development')
with app.app_context():
    db.engine.execute('SELECT 1')
    print('Database connection successful!')
"
```

## 🌐 Accessing the Platform

### Default Admin Account
- **Username:** `ADMIN001`
- **Password:** `admin123`

### Available Routes
- **Landing Page:** `/`
- **Dashboard:** `/dashboard` (requires login)
- **Authentication:** `/auth/login`, `/auth/register`
- **Payments:** `/payments/*`
- **AI Analysis:** `/ai/*`

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Make sure you're in the correct directory
cd mentwel

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

#### 2. Database Connection Errors
```bash
# Check if MySQL is running
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# Verify database exists
mysql -u root -p -e "SHOW DATABASES;"

# Check connection string in .env file
```

#### 3. Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or change port in start.py
```

#### 4. Missing Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies with specific versions
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

To enable debug mode and see detailed error messages:

```python
# In start.py or run.py
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🚀 Production Deployment

For production deployment, see the comprehensive guide in `DEPLOYMENT.md`.

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
    "password": "your_password",
    "email": "optional@email.com",
    "phone_number": "+2348012345678",
    "is_anonymous": true
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
    "anonymous_id": "ABC12345",
    "password": "your_password"
}
```

### Therapy Session Endpoints

#### Create Session
```http
POST /api/sessions
Content-Type: application/json

{
    "therapist_id": 1,
    "session_type": "video",
    "preferred_date": "2024-01-15",
    "preferred_time": "14:00",
    "session_notes": "Session notes"
}
```

### Payment Endpoints

#### Initialize Payment
```http
POST /payments/initialize
Content-Type: application/json

{
    "package_id": 1,
    "amount": 5000.00,
    "email": "user@example.com"
}
```

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** in your terminal
2. **Verify your configuration** in `.env` file
3. **Test database connection** using the test script
4. **Check dependencies** are properly installed
5. **Review error messages** for specific issues

## 📝 Development Notes

- The platform uses **Flask-Login** for session management
- **bcrypt** is used for password hashing
- **PayStack** integration for Nigerian payments
- **Hugging Face API** for sentiment analysis
- **MySQL** with **SQLAlchemy** ORM
- **Responsive design** with vanilla CSS/JS

## 🔄 Updates and Maintenance

To update the platform:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart the application
python start.py
```

---

**Happy coding! 🚀**

The MentWel platform is now ready to provide accessible mental health support to Nigeria.
