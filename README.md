# MentWel - Digital Mental Health Platform

## 🌟 About MentWel

MentWel is a digital mental health platform designed to provide accessible and affordable therapy in Nigeria. Our platform addresses the critical need for mental health support by offering anonymous therapy sessions, making it easier for people to seek help without physical barriers or social stigma.

## 🚀 Key Features

### 🔒 Anonymous Therapy
- **Complete Anonymity**: Users can interact with therapists without revealing their identity
- **Anonymous IDs**: Automatically generated alphanumeric codes for user identification
- **Optional Contact Info**: Phone numbers and emails are optional for account recovery

### 💬 Multiple Communication Channels
- **Written Messages**: Secure text-based communication
- **Voice Notes**: Audio message support for more personal interaction
- **Video Calls**: Face-to-face therapy sessions from the comfort of home

### 🎯 Flexible User Experience
- **Anonymous Mode**: Default setting for maximum privacy
- **Non-Anonymous Option**: Users can choose to reveal their identity if preferred
- **Trust Building**: Video calls help establish therapeutic relationships

### 💳 Monetization
- **PayStack Integration**: Secure payment processing for therapy sessions
- **Flexible Pricing**: Support for different session types and durations
- **Subscription Models**: Recurring payment options for ongoing therapy

### 📊 Analytics & Insights
- **Sentiment Analysis**: AI-powered mood tracking using Hugging Face API
- **Progress Charts**: Visual representation of mental health journey
- **Anonymous Data**: Privacy-preserving analytics for platform improvement

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask (+ Blueprints)
- **Database**: SQLite (default) or MySQL via SQLAlchemy
- **AI**: Hugging Face APIs (Sentiment + optional Text Generation)
- **Payments**: Paystack API
- **Charts**: Chart.js for data visualization

## 📁 Project Structure

```
MentWel/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── app/
│   ├── __init__.py        # app factory, blueprints register
│   ├── models.py          # SQLAlchemy models
│   ├── auth.py            # auth/login/register/logout
│   ├── payments.py        # Paystack integration
│   └── ai_analysis.py     # sentiment + AI chat endpoints
├── instance/
│   └── mentwel_dev.db     # SQLite DB (created at runtime)
├── config.py
├── requirements.txt
├── run.py                 # entrypoint (Flask app)
├── setup.py               # interactive setup helper
└── database/
    └── schema.sql         # optional legacy SQL (not required for SQLite)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Paystack account (test keys ok for dev)
- Hugging Face API access (optional for AI chat; required for sentiment)
  
MySQL is optional. The default dev setup uses SQLite.

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MentWel
   ```

2. **Create and activate a virtual environment (Windows)**
   ```powershell
   py -3 -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env and initialize the app (guided)**
   ```bash
   python setup.py
   ```
   This will:
   - Generate `.env` (defaults to SQLite at `instance/mentwel_dev.db`)
   - Create tables, seed default packages, and create an admin user

   Alternatively, do it manually:
   ```bash
   # create .env (see example below)
   # then initialize DB via Flask CLI
   python -m flask --app run.py init-db
   python -m flask --app run.py seed-data
   python -m flask --app run.py create-admin
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the platform**
   http://localhost:5000

## 🔧 Configuration

### Environment Variables
```env
# Flask
FLASK_ENV=development
SECRET_KEY=replace_me
DEBUG=true

# Database (SQLite default)
DATABASE_URL=sqlite:///instance/mentwel_dev.db
DEV_DATABASE_URL=sqlite:///instance/mentwel_dev.db

# Paystack
PAYSTACK_PUBLIC_KEY=pk_test_xxx
PAYSTACK_SECRET_KEY=sk_test_xxx
PAYSTACK_BASE_URL=https://api.paystack.co

# Hugging Face
HUGGINGFACE_API_KEY=hf_xxx
```

## 🎨 Design Philosophy

### Logo Concept
The MentWel logo represents:
- **Mind & Wellness**: Brain icon combined with wellness symbols
- **Digital Connection**: Modern, clean design reflecting technology
- **Trust & Safety**: Warm colors and rounded shapes for approachability
- **Anonymity**: Abstract design that doesn't reveal personal identity

### Color Scheme
- **Primary**: #4A90E2 (Trust Blue)
- **Secondary**: #7ED321 (Growth Green)
- **Accent**: #F5A623 (Warm Orange)
- **Neutral**: #9B9B9B (Calm Gray)

## 🔒 Security Notes

- Anonymous IDs supported; minimal PII by default
- Secure session management with Flask-Login
- Webhook signature verification for Paystack (HMAC-SHA512)
- Do not commit `.env` or API keys

## 📈 Scalability Architecture

- **Modular design** for easy feature additions
- **Database optimization** for growing user base
- **Caching strategies** for improved performance
- **Load balancing** ready for high traffic
- **Microservices architecture** for future expansion

## 🤝 Contributing

We welcome contributions to make MentWel better for the Nigerian mental health community. Please read our contributing guidelines before submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@mentwel.ng or create an issue in our repository.

---

**MentWel** - Making mental health accessible, one conversation at a time. 💙
