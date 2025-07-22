
#!/usr/bin/env python3
import os
from app import app, db
from decimal import Decimal

def migrate_database():
    """Create or recreate the database with the correct schema"""
    with app.app_context():
        try:
            # Drop all tables first
            db.drop_all()
            print("Dropped existing tables")
        except Exception as e:
            print(f"Error dropping tables (this is normal if no DB exists): {e}")
        
        # Create all tables with the new schema
        db.create_all()
        print("Created all tables with new schema")
        
        # Check if admin user exists, if not create one
        from app import User, Settings, generate_password_hash
        
        admin = User.query.filter_by(email='admin@socialmedia.com').first()
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@socialmedia.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                is_verified=True,
                is_active=True
            )
            db.session.add(admin_user)
            print("Created admin user")
        
        # Create default settings if they don't exist
        settings = Settings.query.first()
        if not settings:
            default_settings = Settings(
                site_name='SocialMarket',
                currency_symbol='₦',
                currency_code='NGN',
                commission_rate=Decimal('5.0'),
                referral_commission=Decimal('2.0'),
                min_withdrawal=Decimal('1000'),
                max_withdrawal=Decimal('1000000'),
                admin_email='admin@socialmedia.com'
            )
            db.session.add(default_settings)
            print("Created default settings")
        
        db.session.commit()
        print("Database migration completed successfully!")

if __name__ == '__main__':
    migrate_database()
