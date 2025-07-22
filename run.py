
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash
from decimal import Decimal

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'social-marketplace-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/social_marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Initialize extensions
from models import db
db.init_app(app)

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)
CORS(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Import routes after app initialization
from routes import *

if __name__ == '__main__':
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('uploads/account_screenshots', exist_ok=True)
    os.makedirs('uploads/payment_proofs', exist_ok=True)

    with app.app_context():
        db.create_all()

        # Import models
        from models import User, Settings

        # Create admin user if not exists
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

            # Create default settings
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
            db.session.commit()
            print("Admin user and default settings created!")

    app.run(host='0.0.0.0', port=5000, debug=True)
