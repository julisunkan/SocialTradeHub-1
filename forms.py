from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, DecimalField, IntegerField, BooleanField, PasswordField, EmailField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=20)
    ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')
    ])
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

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    profile_pic = FileField('Profile Picture', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')

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
    amount = DecimalField('Amount (₦)', validators=[DataRequired(), NumberRange(min=100, max=1000000)], places=2)
    deposit_method = SelectField('Deposit Method', choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('cash_deposit', 'Cash Deposit')
    ], validators=[DataRequired()])
    bank_name = StringField('Bank Name', validators=[Optional()])
    account_number = StringField('Account Number', validators=[Optional()])
    account_name = StringField('Account Name', validators=[Optional()])
    reference_number = StringField('Transaction Reference', validators=[
        DataRequired(), 
        Length(max=100)
    ])
    payment_proof = FileField('Payment Proof', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDF only!')
    ])
    submit = SubmitField('Submit Deposit Request')

class PurchaseForm(FlaskForm):
    payment_method = SelectField('Payment Method', choices=[
        ('wallet', 'Wallet Balance'),
        ('bank_transfer', 'Bank Transfer')
    ], validators=[DataRequired()])
    payment_proof = FileField('Payment Proof (if bank transfer)', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDF only!')
    ])
    payment_reference = StringField('Payment Reference (if bank transfer)', validators=[
        Optional(), 
        Length(max=100)
    ])
    submit = SubmitField('Purchase Account')

class AdminAccountReviewForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    admin_notes = TextAreaField('Admin Notes', validators=[
        Optional(), 
        Length(max=500)
    ])
    is_featured = BooleanField('Feature this account')
    submit = SubmitField('Update Status')

class AdminDepositReviewForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    admin_notes = TextAreaField('Admin Notes', validators=[
        Optional(), 
        Length(max=500)
    ])
    submit = SubmitField('Update Status')

class AdminPurchaseReviewForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    account_delivered = BooleanField('Account Details Delivered')
    submit = SubmitField('Update Purchase')

class AdminUserManagementForm(FlaskForm):
    is_verified = BooleanField('Verified User')
    is_active = BooleanField('Active User')
    is_banned = BooleanField('Banned User')
    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('admin', 'Admin')
    ], validators=[DataRequired()])
    submit = SubmitField('Update User')

class SettingsForm(FlaskForm):
    site_name = StringField('Site Name', validators=[DataRequired(), Length(max=100)])
    currency_symbol = StringField('Currency Symbol', validators=[DataRequired(), Length(max=5)])
    currency_code = StringField('Currency Code', validators=[DataRequired(), Length(max=3)])
    commission_rate = DecimalField('Commission Rate (%)', validators=[DataRequired(), NumberRange(min=0, max=50)])
    referral_commission = DecimalField('Referral Commission (%)', validators=[DataRequired(), NumberRange(min=0, max=20)])
    min_withdrawal = DecimalField('Minimum Withdrawal', validators=[DataRequired(), NumberRange(min=0)])
    max_withdrawal = DecimalField('Maximum Withdrawal', validators=[DataRequired(), NumberRange(min=1)])

    # Bank details
    bank_name = StringField('Bank Name', validators=[DataRequired(), Length(max=100)])
    bank_account_number = StringField('Account Number', validators=[DataRequired(), Length(max=20)])
    bank_account_name = StringField('Account Name', validators=[DataRequired(), Length(max=100)])

    # Contact information
    admin_email = EmailField('Admin Email', validators=[DataRequired(), Email()])
    support_email = EmailField('Support Email', validators=[Email()])
    phone_number = StringField('Phone Number', validators=[Length(max=20)])

    # Social media links
    facebook_url = StringField('Facebook URL', validators=[Optional()])
    twitter_url = StringField('Twitter URL', validators=[Optional()])
    instagram_url = StringField('Instagram URL', validators=[Optional()])
    telegram_url = StringField('Telegram URL', validators=[Optional()])
    whatsapp_url = StringField('WhatsApp URL', validators=[Optional()])

    submit = SubmitField('Save Settings')

class PageForm(FlaskForm):
    title = StringField('Page Title', validators=[DataRequired(), Length(max=200)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    meta_description = StringField('Meta Description', validators=[Optional(), Length(max=160)])
    seo_title = StringField('SEO Title', validators=[Optional(), Length(max=200)])
    seo_keywords = StringField('SEO Keywords', validators=[Optional(), Length(max=500)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Page')

class SearchForm(FlaskForm):
    platform = SelectField('Platform', choices=[
        ('', 'All Platforms'),
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
    ], validators=[Optional()])
    min_price = DecimalField('Min Price (₦)', validators=[Optional(), NumberRange(min=0)], places=2)
    max_price = DecimalField('Max Price (₦)', validators=[Optional(), NumberRange(min=0)], places=2)
    min_followers = IntegerField('Min Followers', validators=[Optional(), NumberRange(min=0)])
    niche = StringField('Niche', validators=[Optional(), Length(max=100)])
    sort_by = SelectField('Sort By', choices=[
        ('created_at', 'Newest First'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('followers_desc', 'Followers: High to Low')
    ], validators=[Optional()])
    submit = SubmitField('Search')