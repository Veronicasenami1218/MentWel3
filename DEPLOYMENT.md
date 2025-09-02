# MentWel Deployment Guide

This guide provides comprehensive instructions for deploying the MentWel digital mental health platform to various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Database Setup](#database-setup)
8. [SSL/HTTPS Setup](#sslhttps-setup)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Backup and Recovery](#backup-and-recovery)
11. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **MySQL**: 8.0 or higher
- **Node.js**: 14 or higher (for asset compilation)
- **Git**: Latest version
- **Nginx**: 1.18 or higher (for production)
- **Redis**: 6.0 or higher (optional, for caching)

### Required Accounts

- **PayStack Account**: For payment processing
- **Hugging Face Account**: For AI sentiment analysis
- **Email Service**: Gmail, SendGrid, or similar for password recovery
- **Domain Name**: For production deployment

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mentwel.git
cd mentwel
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Setup Script

```bash
python setup.py
```

This will:
- Check Python version
- Install dependencies
- Create `.env` file
- Setup database
- Initialize tables
- Seed initial data
- Create admin user

### 5. Start Development Server

```bash
python run.py
```

Access the application at `http://localhost:5000`

## Production Deployment

### Option 1: Traditional Server Deployment

#### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv mysql-server nginx redis-server -y

# Install Node.js (for asset compilation)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/mentwel
sudo chown $USER:$USER /var/www/mentwel

# Clone repository
git clone https://github.com/your-username/mentwel.git /var/www/mentwel
cd /var/www/mentwel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### 3. Database Setup

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE mentwel_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mentwel_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON mentwel_prod.* TO 'mentwel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 4. Environment Configuration

```bash
# Create production environment file
cp .env.example .env
nano .env
```

Update the following variables:

```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
DATABASE_URL=mysql+pymysql://mentwel_user:strong_password_here@localhost/mentwel_prod

# Paystack Configuration (examples; do not use real keys in docs)
PAYSTACK_SECRET_KEY=<your-paystack-secret-key>
PAYSTACK_PUBLIC_KEY=<your-paystack-public-key>

# Hugging Face Configuration
HUGGINGFACE_API_KEY=<your-huggingface-api-key>

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

#### 5. Initialize Database

```bash
# Initialize database tables
python run.py init-db

# Seed initial data
python run.py seed-data

# Create admin user
python run.py create-admin
```

#### 6. Gunicorn Configuration

Create `/etc/systemd/system/mentwel.service`:

```ini
[Unit]
Description=MentWel Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mentwel
Environment="PATH=/var/www/mentwel/venv/bin"
ExecStart=/var/www/mentwel/venv/bin/gunicorn --workers 3 --bind unix:mentwel.sock -m 007 run:app

[Install]
WantedBy=multi-user.target
```

#### 7. Nginx Configuration

Create `/etc/nginx/sites-available/mentwel`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/mentwel/mentwel.sock;
    }

    location /static {
        alias /var/www/mentwel/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /var/www/mentwel/uploads;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/mentwel /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 8. Start Services

```bash
# Start Gunicorn service
sudo systemctl start mentwel
sudo systemctl enable mentwel

# Check status
sudo systemctl status mentwel
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=mysql+pymysql://mentwel_user:password@db/mentwel_prod
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads
    restart: always

  db:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=mentwel_prod
      - MYSQL_USER=mentwel_user
      - MYSQL_PASSWORD=strong_password_here
      - MYSQL_ROOT_PASSWORD=root_password_here
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: always

volumes:
  mysql_data:
```

#### 3. Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# Initialize database
docker-compose exec web python run.py init-db
docker-compose exec web python run.py seed-data
docker-compose exec web python run.py create-admin

# Check logs
docker-compose logs -f
```

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Instance Setup

```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# Follow Traditional Server Deployment steps above
```

#### 2. RDS Database Setup

- Create RDS MySQL instance
- Configure security groups
- Update DATABASE_URL in .env

#### 3. Load Balancer Setup

- Create Application Load Balancer
- Configure target groups
- Set up health checks

#### 4. Auto Scaling

- Create launch template
- Configure auto scaling group
- Set up scaling policies

### Heroku Deployment

#### 1. Create Heroku App

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create mentwel-app

# Add MySQL addon
heroku addons:create jawsdb:kitefin
```

#### 2. Configure Environment Variables

```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your_secret_key
heroku config:set PAYSTACK_SECRET_KEY=your_paystack_key
heroku config:set PAYSTACK_PUBLIC_KEY=your_paystack_public_key
heroku config:set HUGGINGFACE_API_KEY=your_huggingface_key
```

#### 3. Deploy Application

```bash
# Add Heroku remote
heroku git:remote -a mentwel-app

# Deploy
git push heroku main

# Run database migrations
heroku run python run.py init-db
heroku run python run.py seed-data
heroku run python run.py create-admin
```

### DigitalOcean App Platform

#### 1. Create App

- Connect GitHub repository
- Select Python environment
- Configure build settings

#### 2. Add Database

- Create managed MySQL database
- Configure connection string

#### 3. Configure Environment

- Set environment variables
- Configure build commands

## Environment Configuration

### Development Environment

```env
FLASK_ENV=development
DEBUG=True
DATABASE_URL=mysql+pymysql://root:password@localhost/mentwel_dev
```

### Staging Environment

```env
FLASK_ENV=staging
DEBUG=False
DATABASE_URL=mysql+pymysql://user:password@staging-db/mentwel_staging
```

### Production Environment

```env
FLASK_ENV=production
DEBUG=False
DATABASE_URL=mysql+pymysql://user:password@prod-db/mentwel_prod
```

## Database Setup

### MySQL Configuration

```sql
-- Create database
CREATE DATABASE mentwel_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'mentwel_user'@'localhost' IDENTIFIED BY 'strong_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON mentwel_prod.* TO 'mentwel_user'@'localhost';
FLUSH PRIVILEGES;

-- Import schema
mysql -u mentwel_user -p mentwel_prod < database/schema.sql
```

### Database Optimization

```sql
-- Add indexes for better performance
CREATE INDEX idx_users_anonymous_id ON users(anonymous_id);
CREATE INDEX idx_sessions_patient_id ON therapy_sessions(patient_id);
CREATE INDEX idx_sessions_therapist_id ON therapy_sessions(therapist_id);
CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_sentiment_user_id ON sentiment_analysis(user_id);
```

## SSL/HTTPS Setup

### Let's Encrypt SSL

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Update Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/mentwel/mentwel.sock;
    }

    location /static {
        alias /var/www/mentwel/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## Monitoring and Logging

### Application Logging

```python
# Add to config.py
import logging
from logging.handlers import RotatingFileHandler

class ProductionConfig(Config):
    # Logging configuration
    LOG_LEVEL = logging.INFO
    LOG_FILE = '/var/log/mentwel/app.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
```

### System Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor application
sudo journalctl -u mentwel -f

# Monitor nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks

```python
@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        # Check external services
        # PayStack API check
        # Hugging Face API check
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
```

## Backup and Recovery

### Database Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/mentwel"
DB_NAME="mentwel_prod"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create database backup
mysqldump -u mentwel_user -p$DB_PASSWORD $DB_NAME > $BACKUP_DIR/mentwel_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/mentwel_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "mentwel_*.sql.gz" -mtime +7 -delete

echo "Backup completed: mentwel_$DATE.sql.gz"
```

### File Backup

```bash
#!/bin/bash
# backup_files.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/mentwel"
APP_DIR="/var/www/mentwel"

# Backup uploads directory
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C $APP_DIR uploads/

# Backup configuration
cp $APP_DIR/.env $BACKUP_DIR/env_$DATE

echo "File backup completed"
```

### Automated Backups

```bash
# Add to crontab
sudo crontab -e

# Daily database backup at 2 AM
0 2 * * * /var/www/mentwel/scripts/backup.sh

# Weekly file backup on Sundays at 3 AM
0 3 * * 0 /var/www/mentwel/scripts/backup_files.sh
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues

```bash
# Check MySQL status
sudo systemctl status mysql

# Check connection
mysql -u mentwel_user -p -h localhost

# Check firewall
sudo ufw status
```

#### 2. Application Not Starting

```bash
# Check logs
sudo journalctl -u mentwel -f

# Check permissions
sudo chown -R www-data:www-data /var/www/mentwel

# Check virtual environment
source /var/www/mentwel/venv/bin/activate
python -c "import flask; print(flask.__version__)"
```

#### 3. Nginx Issues

```bash
# Check nginx configuration
sudo nginx -t

# Check nginx status
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/nginx/error.log
```

#### 4. SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Check nginx SSL configuration
sudo nginx -t
```

### Performance Optimization

#### 1. Database Optimization

```sql
-- Analyze table performance
ANALYZE TABLE users, therapy_sessions, payments, sentiment_analysis;

-- Optimize tables
OPTIMIZE TABLE users, therapy_sessions, payments, sentiment_analysis;
```

#### 2. Application Optimization

```python
# Enable caching
from flask_caching import Cache

cache = Cache()

# Cache frequently accessed data
@cache.memoize(timeout=300)
def get_user_stats(user_id):
    # Expensive database query
    pass
```

#### 3. Static File Optimization

```bash
# Compress static files
sudo apt install nginx-extras

# Add to nginx configuration
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

### Security Checklist

- [ ] Change default MySQL root password
- [ ] Configure firewall (UFW)
- [ ] Enable SSL/HTTPS
- [ ] Set secure file permissions
- [ ] Regular security updates
- [ ] Monitor access logs
- [ ] Backup encryption
- [ ] API key rotation
- [ ] Rate limiting
- [ ] Input validation

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**:
   - Check application logs
   - Monitor disk space
   - Review security updates

2. **Monthly**:
   - Update dependencies
   - Review performance metrics
   - Test backup restoration

3. **Quarterly**:
   - Security audit
   - Performance optimization
   - SSL certificate renewal

### Contact Information

- **Technical Support**: support@mentwel.ng
- **Emergency Contact**: +234-XXX-XXX-XXXX
- **Documentation**: https://docs.mentwel.ng
- **GitHub Issues**: https://github.com/your-username/mentwel/issues

---

**Note**: This deployment guide is comprehensive and covers most deployment scenarios. Adjust configurations based on your specific requirements and infrastructure.
