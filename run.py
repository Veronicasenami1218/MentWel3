#!/usr/bin/env python3
"""
MentWel - Digital Mental Health Platform
Main application entry point
"""

import os
from app import create_app, db
from app.models import User, TherapySession, Payment, SentimentAnalysis, SessionPackage

# Create Flask application instance
app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'TherapySession': TherapySession,
        'Payment': Payment,
        'SentimentAnalysis': SentimentAnalysis,
        'SessionPackage': SessionPackage
    }

@app.cli.command()
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    print('Database tables created successfully!')

@app.cli.command()
def seed_data():
    """Seed the database with initial data"""
    try:
        # Create default session packages if they don't exist
        packages = [
            {
                'name': 'Single Session',
                'description': 'One therapy session',
                'session_count': 1,
                'duration_days': 30,
                'price': 5000.00
            },
            {
                'name': 'Starter Pack',
                'description': '3 therapy sessions',
                'session_count': 3,
                'duration_days': 90,
                'price': 13500.00
            },
            {
                'name': 'Monthly Plan',
                'description': '8 therapy sessions per month',
                'session_count': 8,
                'duration_days': 30,
                'price': 32000.00
            },
            {
                'name': 'Quarterly Plan',
                'description': '24 therapy sessions over 3 months',
                'session_count': 24,
                'duration_days': 90,
                'price': 90000.00
            }
        ]
        
        for package_data in packages:
            existing = SessionPackage.query.filter_by(package_name=package_data['name']).first()
            if not existing:
                package = SessionPackage(**package_data)
                db.session.add(package)
        
        db.session.commit()
        print('Default packages seeded successfully!')
        
    except Exception as e:
        db.session.rollback()
        print(f'Error seeding data: {str(e)}')

@app.cli.command()
def create_admin():
    """Create an admin user for testing"""
    try:
        # Check if admin user already exists
        admin = User.query.filter_by(anonymous_id='ADMIN001').first()
        if admin:
            print('Admin user already exists!')
            return
        
        # Create admin user
        admin = User(
            anonymous_id='ADMIN001',
            email='admin@mentwel.ng',
            is_anonymous=False,
            is_therapist=True,
            therapist_verified=True,
            therapist_specialization='General Therapy',
            therapist_bio='Administrator account for MentWel platform'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print('Admin user created successfully!')
        print('Anonymous ID: ADMIN001')
        print('Password: admin123')
        
    except Exception as e:
        db.session.rollback()
        print(f'Error creating admin: {str(e)}')

if __name__ == '__main__':
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
