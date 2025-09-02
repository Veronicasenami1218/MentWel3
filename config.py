import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class for MentWel application"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mentwel-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    # Ensure DEBUG is a real boolean, not a string like 'true'
    DEBUG = str(os.environ.get('DEBUG', 'true')).lower() in ['true', '1', 'on', 'yes']
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:password@localhost/mentwel_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # PayStack Configuration
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
    PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')
    PAYSTACK_BASE_URL = 'https://api.paystack.co'
    
    # Hugging Face Configuration
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
    HUGGINGFACE_API_URL = 'https://api.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest'
    # Optional: Text generation model URL for AI chat (can be overridden via env)
    HUGGINGFACE_TEXT_GEN_URL = os.environ.get('HUGGINGFACE_TEXT_GEN_URL') or \
        'https://api.huggingface.co/models/google/gemma-2b-it'
    
    # Security Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'm4a'}
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False  # Overridden in ProductionConfig
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = False  # Overridden in ProductionConfig
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Email Configuration (for password recovery)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    # Align Flask-Mail debug with app debug
    MAIL_DEBUG = int(bool(DEBUG))
    
    # Supabase Configuration (read-only exposure via app config)
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
    SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    SUPABASE_JWT_SECRET = os.environ.get('SUPABASE_JWT_SECRET')
    
    # CORS Configuration
    # Comma-separated list of allowed origins, e.g. "https://yourdomain.com,https://app.yourdomain.com"
    CORS_ORIGINS = [o.strip() for o in os.environ.get('CORS_ORIGINS', '').split(',') if o.strip()]
    
    # Application Settings
    ANONYMOUS_ID_LENGTH = 8  # Length of anonymous user IDs
    MAX_MESSAGE_LENGTH = 1000  # Maximum message length
    MAX_VOICE_NOTE_SIZE = 10 * 1024 * 1024  # 10MB for voice notes
    
    # Video Call Configuration
    VIDEO_CALL_TIMEOUT = 3600  # 1 hour session timeout
    MAX_VIDEO_CALL_PARTICIPANTS = 2  # Patient and therapist only
    
    # Analytics Configuration
    SENTIMENT_ANALYSIS_ENABLED = True
    ANONYMOUS_ANALYTICS = True  # Ensure no personal data in analytics
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # No-op for base config
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:password@localhost/mentwel_dev'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # Enforce secrets must come from environment in production
        insecure_defaults = {
            'SECRET_KEY': 'mentwel-secret-key-change-in-production',
            'JWT_SECRET_KEY': 'jwt-secret-key-change-in-production',
        }

        secret_key = app.config.get('SECRET_KEY')
        jwt_secret = app.config.get('JWT_SECRET_KEY')
        if not secret_key or secret_key == insecure_defaults['SECRET_KEY']:
            raise RuntimeError('SECRET_KEY must be set via environment in production')
        if not jwt_secret or jwt_secret == insecure_defaults['JWT_SECRET_KEY']:
            raise RuntimeError('JWT_SECRET_KEY must be set via environment in production')

        # Paystack secret must be provided for payment features in production
        if not app.config.get('PAYSTACK_SECRET_KEY'):
            app.logger.warning('PAYSTACK_SECRET_KEY is not set; payment features will not work')

        # Normalize rate limit defaults for Flask-Limiter (list of limits)
        rl_default = app.config.get('RATELIMIT_DEFAULT')
        if isinstance(rl_default, str):
            app.config['RATELIMIT_DEFAULT'] = [s.strip() for s in rl_default.split(';') if s.strip()]
        elif rl_default is None:
            app.config['RATELIMIT_DEFAULT'] = []

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    # Avoid pool options that are invalid for SQLite in-memory engine
    SQLALCHEMY_ENGINE_OPTIONS = {}

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
