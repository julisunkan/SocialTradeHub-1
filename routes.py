from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, db, mail, limiter
from models import *
from forms import *

@app.context_processor
def inject_settings():
    settings = Settings.query.first()
    return dict(settings=settings)
from datetime import datetime, timedelta
from decimal import Decimal
import os
import json
import uuid
from PIL import Image

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
        'platforms': db.session.query(SocialAccount.platform).distinct().count()
    }
    
    return render_template('index.html', featured_accounts=featured_accounts, 
                         latest_accounts=latest_accounts, stats=stats)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
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
        
        # Create referral record if applicable
        if referrer:
            referral = Referral(
                referrer_id=referrer.id,
                referred_id=user.id,
                commission_type='signup'
            )
            db.session.add(referral)
            db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
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
    
    # Unread notifications
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', user_stats=user_stats, 
                         recent_purchases=recent_purchases, recent_listings=recent_listings,
                         notifications=notifications)

@app.route('/browse')
def browse():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    
    # Build query
    query = SocialAccount.query.filter_by(status='approved')
    
    # Apply filters
    if request.args.get('platform'):
        query = query.filter(SocialAccount.platform == request.args.get('platform'))
    
    if request.args.get('min_price'):
        query = query.filter(SocialAccount.price >= Decimal(request.args.get('min_price')))
    
    if request.args.get('max_price'):
        query = query.filter(SocialAccount.price <= Decimal(request.args.get('max_price')))
    
    if request.args.get('min_followers'):
        query = query.filter(SocialAccount.followers_count >= int(request.args.get('min_followers')))
    
    if request.args.get('niche'):
        query = query.filter(SocialAccount.niche.contains(request.args.get('niche')))
    
    # Apply sorting
    sort_by = request.args.get('sort_by', 'created_at')
    if sort_by == 'price_asc':
        query = query.order_by(SocialAccount.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(SocialAccount.price.desc())
    elif sort_by == 'followers_desc':
        query = query.order_by(SocialAccount.followers_count.desc())
    else:
        query = query.order_by(SocialAccount.created_at.desc())
    
    accounts = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('browse.html', accounts=accounts, form=form)

@app.route('/account/<int:id>')
def view_account(id):
    account = SocialAccount.query.get_or_404(id)
    
    if account.status != 'approved':
        flash('Account not available.', 'error')
        return redirect(url_for('browse'))
    
    # Parse screenshots JSON
    screenshots = []
    if account.screenshots:
        try:
            screenshots = json.loads(account.screenshots)
        except:
            screenshots = []
    
    return render_template('account_detail.html', account=account, screenshots=screenshots)

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
        return redirect(url_for('my_listings'))
    
    return render_template('list_account.html', form=form)

@app.route('/my-listings')
@login_required
def my_listings():
    page = request.args.get('page', 1, type=int)
    accounts = SocialAccount.query.filter_by(seller_id=current_user.id).order_by(
        SocialAccount.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('my_listings.html', accounts=accounts)

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

@app.route('/my-purchases')
@login_required
def my_purchases():
    page = request.args.get('page', 1, type=int)
    purchases = Purchase.query.filter_by(buyer_id=current_user.id).order_by(
        Purchase.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('my_purchases.html', purchases=purchases)

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
            deposit_method=form.deposit_method.data,
            bank_name=form.bank_name.data,
            account_number=form.account_number.data,
            account_name=form.account_name.data,
            reference_number=form.reference_number.data,
            payment_proof=payment_proof_filename
        )
        
        db.session.add(deposit)
        db.session.commit()
        
        flash('Deposit request submitted successfully!', 'success')
        return redirect(url_for('wallet'))
    
    return render_template('deposit.html', form=form, settings=settings)

@app.route('/referrals')
@login_required
def referrals():
    referrals = User.query.filter_by(referred_by=current_user.id).all()
    referral_stats = {
        'total_referrals': len(referrals),
        'total_earnings': current_user.referral_earnings,
        'pending_earnings': Referral.query.filter_by(
            referrer_id=current_user.id, 
            commission_paid=False
        ).count()
    }
    
    return render_template('referrals.html', referrals=referrals, 
                         referral_stats=referral_stats, 
                         referral_code=current_user.referral_code)

# Admin routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    stats = {
        'total_users': User.query.count(),
        'pending_accounts': SocialAccount.query.filter_by(status='pending').count(),
        'pending_deposits': WalletDeposit.query.filter_by(status='pending').count(),
        'pending_purchases': Purchase.query.filter_by(status='pending').count(),
        'total_revenue': db.session.query(db.func.sum(Purchase.commission)).filter_by(status='completed').scalar() or 0
    }
    
    return render_template('admin/dashboard.html', stats=stats)

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

# API routes for AJAX
@app.route('/api/notifications/mark-read/<int:id>', methods=['POST'])
@login_required
def mark_notification_read(id):
    notification = Notification.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    notification.is_read = True
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

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