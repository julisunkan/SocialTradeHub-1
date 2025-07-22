
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from decimal import Decimal
import uuid

# Create db instance that will be initialized later
db = SQLAlchemy()

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
    accounts_reviewed = db.relationship('SocialAccount', foreign_keys='SocialAccount.reviewed_by', backref='reviewer', lazy=True)
    purchases = db.relationship('Purchase', backref='buyer', lazy=True)
    deposits = db.relationship('WalletDeposit', foreign_keys='WalletDeposit.user_id', backref='user', lazy=True)
    processed_deposits = db.relationship('WalletDeposit', foreign_keys='WalletDeposit.processed_by', backref='processor', lazy=True)
    referrals = db.relationship('User', backref=db.backref('referrer', remote_side=[id]))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8].upper()

class SocialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Account details
    platform = db.Column(db.String(50), nullable=False)  # instagram, facebook, twitter, etc.
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

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    
    # Invoice details
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), default=0.00)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='unpaid')  # unpaid, paid, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='invoices')
    purchase = db.relationship('Purchase', backref='invoice', uselist=False)

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Commission details
    commission_amount = db.Column(db.Numeric(10, 2), default=0.00)
    commission_paid = db.Column(db.Boolean, default=False)
    commission_type = db.Column(db.String(50))  # signup, purchase
    
    # Related transaction
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    referrer = db.relationship('User', foreign_keys=[referrer_id], backref='referrals_made')
    referred = db.relationship('User', foreign_keys=[referred_id], backref='referral_record')

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
    telegram_url = db.Column(db.String(255))
    whatsapp_url = db.Column(db.String(255))
    
    # Footer links
    help_center_url = db.Column(db.String(255))
    contact_us_url = db.Column(db.String(255))
    safety_tips_url = db.Column(db.String(255))
    terms_of_service_url = db.Column(db.String(255))
    privacy_policy_url = db.Column(db.String(255))
    refund_policy_url = db.Column(db.String(255))
    cookie_policy_url = db.Column(db.String(255))
    how_it_works_url = db.Column(db.String(255))
    pricing_url = db.Column(db.String(255))
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Notification details
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50))  # info, warning, success, error
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Activity details
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='activity_logs')
