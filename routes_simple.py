from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, TextAreaField, SelectField, DecimalField, IntegerField, BooleanField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
import uuid

def register_routes(app, db):
    # Import models from the main app
    from run import User, SocialAccount, Purchase, WalletDeposit, Settings
    
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
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('auth/register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and check_password_hash(user.password_hash, form.password.data):
                if not user.is_active:
                    flash('Your account has been deactivated. Please contact support.', 'error')
                    return redirect(url_for('login'))
                
                if user.is_banned:
                    flash('Your account has been banned. Please contact support.', 'error')
                    return redirect(url_for('login'))
                
                login_user(user, remember=form.remember_me.data)
                from datetime import datetime
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
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
        # User statistics
        user_stats = {
            'accounts_listed': SocialAccount.query.filter_by(seller_id=current_user.id).count(),
            'accounts_sold': Purchase.query.join(SocialAccount).filter(
                SocialAccount.seller_id == current_user.id,
                Purchase.status == 'completed'
            ).count(),
            'purchases_made': Purchase.query.filter_by(buyer_id=current_user.id).count(),
            'wallet_balance': current_user.wallet_balance,
            'referral_earnings': current_user.referral_earnings
        }
        
        # Recent activity
        recent_purchases = Purchase.query.filter_by(buyer_id=current_user.id).order_by(Purchase.created_at.desc()).limit(5).all()
        recent_listings = SocialAccount.query.filter_by(seller_id=current_user.id).order_by(SocialAccount.created_at.desc()).limit(5).all()
        
        return render_template('dashboard/index.html', user_stats=user_stats, 
                             recent_purchases=recent_purchases, recent_listings=recent_listings)

    @app.route('/browse')
    def browse():
        page = request.args.get('page', 1, type=int)
        
        # Build query
        query = SocialAccount.query.filter_by(status='approved')
        
        # Apply filters
        if request.args.get('platform'):
            query = query.filter(SocialAccount.platform == request.args.get('platform'))
        
        accounts = query.paginate(page=page, per_page=12, error_out=False)
        
        return render_template('browse.html', accounts=accounts)

    @app.route('/account/<int:id>')
    def view_account(id):
        account = SocialAccount.query.get_or_404(id)
        
        if account.status != 'approved':
            flash('Account not available.', 'error')
            return redirect(url_for('browse'))
        
        return render_template('account_detail.html', account=account)

    # PWA routes
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
        return app.send_static_file('sw.js')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500