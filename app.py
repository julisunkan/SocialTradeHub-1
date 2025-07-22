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
from wtforms import StringField, TextAreaField, SelectField, DecimalField, IntegerField, BooleanField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import datetime, timedelta
from decimal import Decimal
import uuid
import json
from functools import wraps
from PIL import Image
import os
from forms import (
    RegistrationForm, LoginForm, SocialAccountForm,
    WalletDepositForm, PurchaseForm, AdminAccountReviewForm,
    AdminDepositReviewForm, AdminPurchaseReviewForm, AdminUserManagementForm,
    SettingsForm, SearchForm
)

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

# Import db from models and initialize with app
from models import db
db.init_app(app)
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

# Import models from models.py
from models import User, SocialAccount, Purchase, WalletDeposit, Settings, Notification, Referral, Invoice

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

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    referral_code = StringField('Referral Code (Optional)', validators=[Optional()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SocialAccountForm(FlaskForm):
    platform = SelectField('Platform', choices=[
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('snapchat', 'Snapchat'),
        ('pinterest', 'Pinterest'),
        ('discord', 'Discord'),
        ('telegram', 'Telegram'),
        ('whatsapp_business', 'WhatsApp Business')
    ], validators=[DataRequired()])

    username = StringField('Account Username', validators=[
        DataRequired(), 
        Length(min=1, max=100)
    ])
    followers_count = IntegerField('Followers Count', validators=[
        DataRequired(), 
        NumberRange(min=0)
    ])
    engagement_rate = DecimalField('Engagement Rate (%)', validators=[
        Optional(), 
        NumberRange(min=0, max=100)
    ], places=2)
    account_age = StringField('Account Age', validators=[
        DataRequired(), 
        Length(max=50)
    ])
    niche = StringField('Niche/Category', validators=[
        DataRequired(), 
        Length(max=100)
    ])
    price = DecimalField('Price (₦)', validators=[
        DataRequired(), 
        NumberRange(min=1)
    ], places=2)
    description = TextAreaField('Description', validators=[
        DataRequired(), 
        Length(min=10, max=1000)
    ])
    screenshots = FileField('Account Screenshots', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    login_email = StringField('Login Email', validators=[
        DataRequired(), 
        Email()
    ])
    login_password = StringField('Login Password', validators=[
        DataRequired()
    ])
    additional_info = TextAreaField('Additional Information', validators=[
        Optional(), 
        Length(max=500)
    ])
    submit = SubmitField('List Account')

class WalletDepositForm(FlaskForm):
    amount = DecimalField('Amount (₦)', validators=[DataRequired(), NumberRange(min=100)], places=2)
    reference_number = StringField('Transaction Reference/ID', validators=[DataRequired()])
    payment_proof = FileField('Payment Receipt/Screenshot', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDF only!')
    ])
    submit = SubmitField('Submit Deposit Request')

class AdminAccountReviewForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    admin_notes = TextAreaField('Admin Notes', validators=[Optional()])
    is_featured = BooleanField('Featured Account')
    submit = SubmitField('Update Account')

class AdminDepositReviewForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    admin_notes = TextAreaField('Admin Notes', validators=[Optional()])
    submit = SubmitField('Update Deposit')

class AdminPurchaseReviewForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    account_delivered = BooleanField('Account Delivered')
    submit = SubmitField('Update Purchase')

class AdminUserManagementForm(FlaskForm):
    is_verified = BooleanField('Verified')
    is_active = BooleanField('Active')
    is_banned = BooleanField('Banned')
    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('admin', 'Admin')
    ], validators=[DataRequired()])
    submit = SubmitField('Update User')

class PurchaseForm(FlaskForm):
    payment_method = SelectField('Payment Method', choices=[
        ('wallet', 'Wallet Balance'),
        ('bank_transfer', 'Bank Transfer')
    ], validators=[DataRequired()])
    payment_reference = StringField('Payment Reference', validators=[Optional()])
    payment_proof = FileField('Payment Proof', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDF only!')
    ])
    submit = SubmitField('Complete Purchase')

class SearchForm(FlaskForm):
    platform = SelectField('Platform', choices=[], validators=[Optional()])
    min_price = DecimalField('Min Price', validators=[Optional(), NumberRange(min=0)])
    max_price = DecimalField('Max Price', validators=[Optional(), NumberRange(min=0)])
    min_followers = IntegerField('Min Followers', validators=[Optional(), NumberRange(min=0)])
    niche = StringField('Niche', validators=[Optional()])
    submit = SubmitField('Search')

class SettingsForm(FlaskForm):
    site_name = StringField('Site Name', validators=[DataRequired()])
    commission_rate = DecimalField('Commission Rate (%)', validators=[DataRequired(), NumberRange(min=0, max=100)], places=2)
    referral_commission = DecimalField('Referral Commission (%)', validators=[DataRequired(), NumberRange(min=0, max=100)], places=2)
    min_withdrawal = DecimalField('Min Withdrawal', validators=[DataRequired(), NumberRange(min=0)], places=2)
    max_withdrawal = DecimalField('Max Withdrawal', validators=[DataRequired(), NumberRange(min=0)], places=2)

    # Primary Bank Account Details
    bank_name = StringField('Bank Name', validators=[Optional()])
    account_number = StringField('Account Number', validators=[Optional()])
    account_name = StringField('Account Name', validators=[Optional()])

    # Alternative Bank Account Details
    bank_name_2 = StringField('Alternative Bank Name', validators=[Optional()])
    account_number_2 = StringField('Alternative Account Number', validators=[Optional()])
    account_name_2 = StringField('Alternative Account Name', validators=[Optional()])

    # Payment Instructions
    payment_instructions = TextAreaField('Payment Instructions', validators=[Optional()])

    admin_email = EmailField('Admin Email', validators=[Optional(), Email()])
    submit = SubmitField('Save Settings')

# Utility functions
def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, upload_path, max_size=(800, 600)):
    if file and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif', 'pdf'}):
        filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(upload_path, filename)

        # Create directory if it doesn't exist
        os.makedirs(upload_path, exist_ok=True)

        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Resize image if it's too large
            image = Image.open(file)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            image.save(filepath, optimize=True, quality=85)
        else:
            file.save(filepath)

        return filename
    return None

# Routes
@app.route('/')
def index():
    # Get featured accounts
    featured_accounts = SocialAccount.query.filter_by(status='approved', is_featured=True).limit(6).all()

    # Get latest accounts
    latest_accounts = SocialAccount.query.filter_by(status='approved').order_by(SocialAccount.created_at.desc()).limit(8).all()

    # Get statistics
    stats = {
        'total_accounts': SocialAccount.query.filter_by(status='approved').count(),
        'total_users': User.query.filter_by(is_active=True).count(),
        'total_sales': Purchase.query.filter_by(status='completed').count(),
        'platforms': 11  # Static count for now
    }

    return render_template('index.html', featured_accounts=featured_accounts, 
                         latest_accounts=latest_accounts, stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if referral code is valid
        referrer = None
        if form.referral_code.data:
            referrer = User.query.filter_by(referral_code=form.referral_code.data).first()
            if not referrer:
                flash('Invalid referral code.', 'warning')

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            referred_by=referrer.id if referrer else None
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')

    return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            if user.is_banned:
                flash('Your account has been banned. Please contact support.', 'error')
                return render_template('auth/login.html', form=form)

            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Redirect to next page if specified
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's accounts
    user_accounts = SocialAccount.query.filter_by(seller_id=current_user.id).all()

    # Get user's purchases
    user_purchases = Purchase.query.filter_by(buyer_id=current_user.id).all()

    # Get user's deposits
    user_deposits = WalletDeposit.query.filter_by(user_id=current_user.id).order_by(WalletDeposit.created_at.desc()).limit(5).all()

    # Calculate statistics
    total_sales = Purchase.query.join(SocialAccount).filter(
        SocialAccount.seller_id == current_user.id,
        Purchase.status == 'completed'
    ).count()

    user_stats = {
        'accounts_listed': len(user_accounts),
        'accounts_sold': total_sales,
        'purchases_made': len(user_purchases),
        'wallet_balance': current_user.wallet_balance,
        'referral_earnings': current_user.referral_earnings
    }

    # Recent activity
    recent_purchases = Purchase.query.filter_by(buyer_id=current_user.id).order_by(Purchase.created_at.desc()).limit(5).all()
    recent_listings = SocialAccount.query.filter_by(seller_id=current_user.id).order_by(SocialAccount.created_at.desc()).limit(5).all()

    return render_template('dashboard/index.html', 
                         user_stats=user_stats,
                         recent_purchases=recent_purchases,
                         recent_listings=recent_listings)

@app.route('/browse')
def browse():
    # Get filter parameters
    platform = request.args.get('platform', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_followers = request.args.get('min_followers', type=int)
    niche = request.args.get('niche', '')
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')

    # Build query
    query = SocialAccount.query.filter_by(status='approved')

    if platform:
        query = query.filter(SocialAccount.platform == platform)
    if min_price:
        query = query.filter(SocialAccount.price >= min_price)
    if max_price:
        query = query.filter(SocialAccount.price <= max_price)
    if min_followers:
        query = query.filter(SocialAccount.followers_count >= min_followers)
    if niche:
        query = query.filter(SocialAccount.niche.contains(niche))

    # Apply sorting
    if sort_by == 'price':
        if order == 'asc':
            query = query.order_by(SocialAccount.price.asc())
        else:
            query = query.order_by(SocialAccount.price.desc())
    elif sort_by == 'followers':
        if order == 'asc':
            query = query.order_by(SocialAccount.followers_count.asc())
        else:
            query = query.order_by(SocialAccount.followers_count.desc())
    else:  # created_at
        if order == 'asc':
            query = query.order_by(SocialAccount.created_at.asc())
        else:
            query = query.order_by(SocialAccount.created_at.desc())

    accounts = query.all()

    # Get unique platforms and niches for filters
    platforms = db.session.query(SocialAccount.platform).filter_by(status='approved').distinct().all()
    platforms = [p[0] for p in platforms]

    niches = db.session.query(SocialAccount.niche).filter_by(status='approved').distinct().all()
    niches = [n[0] for n in niches if n[0]]

    return render_template('browse.html', 
                         accounts=accounts, 
                         platforms=platforms, 
                         niches=niches,
                         current_filters={
                             'platform': platform,
                             'min_price': min_price,
                             'max_price': max_price,
                             'min_followers': min_followers,
                             'niche': niche,
                             'sort_by': sort_by,
                             'order': order
                         })

@app.route('/account/<int:account_id>')
def account_detail(account_id):
    account = SocialAccount.query.get_or_404(account_id)

    if account.status != 'approved':
        flash('Account not available.', 'error')
        return redirect(url_for('browse'))

    # Get similar accounts
    similar_accounts = SocialAccount.query.filter(
        SocialAccount.platform == account.platform,
        SocialAccount.status == 'approved',
        SocialAccount.id != account.id
    ).limit(4).all()

    return render_template('account_detail.html', account=account, similar_accounts=similar_accounts)

@app.route('/list-account', methods=['GET', 'POST'])
@login_required
def list_account():
    form = SocialAccountForm()

    if form.validate_on_submit():
        # Save screenshot
        screenshot_filename = None
        if form.screenshots.data:
            screenshot_filename = save_uploaded_file(
                form.screenshots.data, 
                'uploads/account_screenshots'
            )

        # Create account listing
        account = SocialAccount(
            seller_id=current_user.id,
            platform=form.platform.data,
            username=form.username.data,
            followers_count=form.followers_count.data,
            engagement_rate=form.engagement_rate.data,
            account_age=form.account_age.data,
            niche=form.niche.data,
            price=form.price.data,
            description=form.description.data,
            screenshots=json.dumps([screenshot_filename]) if screenshot_filename else None,
            login_email=form.login_email.data,
            login_password=form.login_password.data,
            additional_info=form.additional_info.data
        )

        db.session.add(account)
        db.session.commit()

        flash('Account listed successfully! It will be reviewed by our team.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('list_account.html', form=form)

@app.route('/wallet')
@login_required
def wallet():
    page = request.args.get('page', 1, type=int)
    deposits = WalletDeposit.query.filter_by(user_id=current_user.id).order_by(
        WalletDeposit.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)

    return render_template('wallet.html', deposits=deposits)

@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    form = WalletDepositForm()
    settings = Settings.query.first()

    if form.validate_on_submit():
        payment_proof_filename = None
        if form.payment_proof.data:
            payment_proof_filename = save_uploaded_file(
                form.payment_proof.data,
                'uploads/payment_proofs'
            )

        deposit = WalletDeposit(
            user_id=current_user.id,
            amount=form.amount.data,
            reference_number=form.reference_number.data,
            payment_proof=payment_proof_filename
        )

        db.session.add(deposit)
        db.session.commit()

        flash('Deposit request submitted successfully!', 'success')
        return redirect(url_for('wallet'))

    return render_template('deposit.html', form=form, settings=settings)

@app.route('/my-listings')
@login_required
def my_listings():
    page = request.args.get('page', 1, type=int)
    accounts = SocialAccount.query.filter_by(seller_id=current_user.id).order_by(
        SocialAccount.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)

    return render_template('my_listings.html', accounts=accounts)

@app.route('/my-purchases')
@login_required
def my_purchases():
    page = request.args.get('page', 1, type=int)
    purchases = Purchase.query.filter_by(buyer_id=current_user.id).order_by(
        Purchase.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)

    return render_template('my_purchases.html', purchases=purchases)

@app.route('/referrals')
@login_required
def referrals():
    referrals = User.query.filter_by(referred_by=current_user.id).all()
    referral_stats = {
        'total_referrals': len(referrals),
        'total_earnings': current_user.referral_earnings,
        'pending_earnings': 0  # You can implement this logic later
    }

    return render_template('referrals.html', referrals=referrals, 
                         referral_stats=referral_stats, 
                         referral_code=current_user.referral_code)

# Admin routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    # Get statistics
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'total_accounts': SocialAccount.query.count(),
        'pending_accounts': SocialAccount.query.filter_by(status='pending').count(),
        'approved_accounts': SocialAccount.query.filter_by(status='approved').count(),
        'total_purchases': Purchase.query.count(),
        'pending_purchases': Purchase.query.filter_by(status='pending').count(),
        'completed_purchases': Purchase.query.filter_by(status='completed').count(),
        'pending_deposits': WalletDeposit.query.filter_by(status='pending').count(),
        'total_deposits': WalletDeposit.query.count()
    }

    # Get recent activities
    recent_accounts = SocialAccount.query.order_by(SocialAccount.created_at.desc()).limit(5).all()
    recent_purchases = Purchase.query.order_by(Purchase.created_at.desc()).limit(5).all()
    recent_deposits = WalletDeposit.query.order_by(WalletDeposit.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_accounts=recent_accounts,
                         recent_purchases=recent_purchases,
                         recent_deposits=recent_deposits)

@app.route('/admin/accounts')
@login_required
@admin_required
def admin_accounts():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'pending')

    accounts = SocialAccount.query.filter_by(status=status_filter).order_by(
        SocialAccount.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/accounts.html', accounts=accounts, 
                         current_status=status_filter)

@app.route('/admin/deposits')
@login_required
@admin_required
def admin_deposits():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'pending')

    deposits = WalletDeposit.query.filter_by(status=status_filter).order_by(
        WalletDeposit.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/deposits.html', deposits=deposits, 
                         current_status=status_filter)

@app.route('/admin/purchases')
@login_required
@admin_required
def admin_purchases():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'pending')

    purchases = Purchase.query.filter_by(status=status_filter).order_by(
        Purchase.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/purchases.html', purchases=purchases, 
                         current_status=status_filter)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_manage_user(id):
    user = User.query.get_or_404(id)
    form = AdminUserManagementForm()

    if form.validate_on_submit():
        user.is_verified = form.is_verified.data
        user.is_active = form.is_active.data
        user.is_banned = form.is_banned.data
        user.role = form.role.data

        db.session.commit()

        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))

    # Pre-populate form
    form.is_verified.data = user.is_verified
    form.is_active.data = user.is_active
    form.is_banned.data = user.is_banned
    form.role.data = user.role

    return render_template('admin/manage_user.html', user=user, form=form)

@app.route('/admin/account/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_review_account(id):
    account = SocialAccount.query.get_or_404(id)
    form = AdminAccountReviewForm()

    if form.validate_on_submit():
        account.status = form.status.data
        account.admin_notes = form.admin_notes.data
        account.is_featured = form.is_featured.data
        account.reviewed_by = current_user.id
        account.reviewed_at = datetime.utcnow()

        db.session.commit()

        flash(f'Account {form.status.data} successfully!', 'success')
        return redirect(url_for('admin_accounts'))

    # Pre-populate form
    form.status.data = account.status
    form.admin_notes.data = account.admin_notes
    form.is_featured.data = account.is_featured

    return render_template('admin/review_account.html', account=account, form=form)

@app.route('/admin/deposit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_review_deposit(id):
    deposit = WalletDeposit.query.get_or_404(id)
    form = AdminDepositReviewForm()

    if form.validate_on_submit():
        if form.status.data == 'confirmed' and deposit.status == 'pending':
            # Add to user wallet
            deposit.user.wallet_balance += deposit.amount

        deposit.status = form.status.data
        deposit.admin_notes = form.admin_notes.data
        deposit.processed_by = current_user.id
        deposit.processed_at = datetime.utcnow()

        db.session.commit()

        flash(f'Deposit {form.status.data} successfully!', 'success')
        return redirect(url_for('admin_deposits'))

    return render_template('admin/review_deposit.html', deposit=deposit, form=form)

@app.route('/admin/purchase/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_review_purchase(id):
    purchase = Purchase.query.get_or_404(id)
    form = AdminPurchaseReviewForm()

    if form.validate_on_submit():
        purchase.status = form.status.data
        purchase.account_delivered = form.account_delivered.data

        if form.account_delivered.data:
            purchase.delivery_date = datetime.utcnow()

        db.session.commit()

        flash(f'Purchase updated successfully!', 'success')
        return redirect(url_for('admin_purchases'))

    return render_template('admin/review_purchase.html', purchase=purchase, form=form)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_settings():
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()

    form = SettingsForm(obj=settings)

    if form.validate_on_submit():
        form.populate_obj(settings)
        settings.updated_at = datetime.utcnow()
        db.session.commit()

        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))

    return render_template('admin/settings.html', form=form, settings=settings)

@app.route('/purchase/<int:id>', methods=['GET', 'POST'])
@login_required
def purchase_account(id):
    account = SocialAccount.query.get_or_404(id)

    if account.status != 'approved':
        flash('Account not available for purchase.', 'error')
        return redirect(url_for('browse'))

    if account.seller_id == current_user.id:
        flash('You cannot purchase your own account.', 'error')
        return redirect(url_for('account_detail', account_id=id))

    form = PurchaseForm()
    settings = Settings.query.first()

    # Calculate total with commission
    commission = account.price * (settings.commission_rate / 100) if settings else Decimal('0')
    total_amount = account.price + commission

    if form.validate_on_submit():
        if form.payment_method.data == 'wallet':
            if current_user.wallet_balance < total_amount:
                flash('Insufficient wallet balance.', 'error')
                return redirect(url_for('purchase_account', id=id))

            # Deduct from wallet
            current_user.wallet_balance -= total_amount

            # Create purchase record
            purchase = Purchase(
                buyer_id=current_user.id,
                account_id=account.id,
                amount=account.price,
                commission=commission,
                total_amount=total_amount,
                status='confirmed',
                payment_method='wallet'
            )

            # Mark account as sold
            account.status = 'sold'

        else:  # Bank transfer
            payment_proof_filename = None
            if form.payment_proof.data:
                payment_proof_filename = save_uploaded_file(
                    form.payment_proof.data,
                    'uploads/payment_proofs'
                )

            purchase = Purchase(
                buyer_id=current_user.id,
                account_id=account.id,
                amount=account.price,
                commission=commission,
                total_amount=total_amount,
                status='pending',
                payment_method='bank_transfer',
                payment_proof=payment_proof_filename,
                payment_reference=form.payment_reference.data
            )

        db.session.add(purchase)
        db.session.commit()

        # Generate invoice
        invoice = Invoice(
            user_id=current_user.id,
            purchase_id=purchase.id,
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            amount=account.price,
            total_amount=total_amount
        )
        db.session.add(invoice)
        db.session.commit()

        flash('Purchase submitted successfully!', 'success')
        return redirect(url_for('my_purchases'))

    return render_template('purchase_account.html', account=account, form=form, 
                         total_amount=total_amount, commission=commission)

# PWA Routes
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "SocialMarket",
        "short_name": "SocialMarket",
        "description": "Buy and sell social media accounts",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#3b82f6",
        "icons": [
            {
                "src": "/static/icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

# File serving
@app.route('/uploads/<path:filename>')
@login_required
@admin_required
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

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