import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from decimal import Decimal
import uuid
import json
from functools import wraps

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'social-marketplace-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_marketplace.db'
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
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
mail = Mail(app)
cors = CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

# Create upload directories
os.makedirs('uploads/payment_proofs', exist_ok=True)
os.makedirs('uploads/account_screenshots', exist_ok=True)
os.makedirs('uploads/profile_pics', exist_ok=True)
os.makedirs('static/manifest', exist_ok=True)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin
    
    # Profile information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    profile_pic = db.Column(db.String(255))
    bio = db.Column(db.Text)
    
    # Status
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_banned = db.Column(db.Boolean, default=False)
    
    # Wallet
    wallet_balance = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Referral system
    referral_code = db.Column(db.String(20), unique=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    referral_earnings = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    accounts_for_sale = db.relationship('SocialAccount', foreign_keys='SocialAccount.seller_id', backref='seller', lazy=True)
    purchases = db.relationship('Purchase', foreign_keys='Purchase.buyer_id', backref='buyer', lazy=True)
    deposits = db.relationship('WalletDeposit', foreign_keys='WalletDeposit.user_id', backref='user', lazy=True)
    referrals = db.relationship('User', backref=db.backref('referrer', remote_side=[id]))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8].upper()

class SocialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Account details
    platform = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    followers_count = db.Column(db.Integer)
    engagement_rate = db.Column(db.Float)
    account_age = db.Column(db.String(50))
    niche = db.Column(db.String(100))
    
    # Pricing
    price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Description and media
    description = db.Column(db.Text)
    screenshots = db.Column(db.Text)  # JSON array of image paths
    
    # Account credentials (encrypted)
    login_email = db.Column(db.String(255))
    login_password = db.Column(db.String(255))
    additional_info = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, sold
    is_featured = db.Column(db.Boolean, default=False)
    
    # Admin review
    admin_notes = db.Column(db.Text)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('social_account.id'), nullable=False)
    
    # Transaction details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    commission = db.Column(db.Numeric(10, 2), default=0.00)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    payment_method = db.Column(db.String(50))
    
    # Payment proof
    payment_proof = db.Column(db.String(255))
    payment_reference = db.Column(db.String(100))
    
    # Account delivery
    account_delivered = db.Column(db.Boolean, default=False)
    delivery_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = db.relationship('SocialAccount', backref='purchases')

class WalletDeposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Deposit details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    deposit_method = db.Column(db.String(50))  # bank_transfer, cash_deposit
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20))
    account_name = db.Column(db.String(100))
    
    # Payment proof
    payment_proof = db.Column(db.String(255))
    reference_number = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, rejected
    admin_notes = db.Column(db.Text)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    processed_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Site settings
    site_name = db.Column(db.String(100), default='SocialMarket')
    site_description = db.Column(db.Text)
    site_logo = db.Column(db.String(255))
    
    # Currency settings
    currency_symbol = db.Column(db.String(10), default='₦')
    currency_code = db.Column(db.String(3), default='NGN')
    
    # Commission settings
    commission_rate = db.Column(db.Numeric(5, 2), default=5.00)  # Percentage
    referral_commission = db.Column(db.Numeric(5, 2), default=2.00)  # Percentage
    
    # Withdrawal limits
    min_withdrawal = db.Column(db.Numeric(10, 2), default=1000.00)
    max_withdrawal = db.Column(db.Numeric(10, 2), default=1000000.00)
    
    # Email settings
    smtp_server = db.Column(db.String(100))
    smtp_port = db.Column(db.Integer, default=587)
    smtp_username = db.Column(db.String(100))
    smtp_password = db.Column(db.String(255))
    admin_email = db.Column(db.String(120))
    
    # Bank details for deposits
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20))
    account_name = db.Column(db.String(100))
    
    # Social media links
    facebook_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))
    instagram_url = db.Column(db.String(255))
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Import routes
from routes_simple import register_routes
register_routes(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
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
            
    app.run(host='0.0.0.0', port=5000, debug=True)