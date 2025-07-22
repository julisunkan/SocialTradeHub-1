
from app import app, db
from models import Page, Settings
from datetime import datetime

def create_default_pages():
    with app.app_context():
        # Check if pages already exist
        existing_pages = Page.query.all()
        if existing_pages:
            print("Pages already exist, skipping creation.")
            return

        default_pages = [
            {
                'title': 'Help Center',
                'slug': 'help',
                'content': '''
                <h1>Help Center</h1>
                <h2>Frequently Asked Questions</h2>
                
                <h3>How do I buy a social media account?</h3>
                <p>Browse our marketplace, select an account, and follow the purchase process. Payment can be made via wallet balance or bank transfer.</p>
                
                <h3>How do I sell my account?</h3>
                <p>Click "List Account" in your dashboard, fill out the form with your account details, and submit for review.</p>
                
                <h3>How long does account verification take?</h3>
                <p>Account verification typically takes 24-48 hours.</p>
                
                <h3>What payment methods do you accept?</h3>
                <p>We accept bank transfers and wallet balance payments.</p>
                '''
            },
            {
                'title': 'Contact Us',
                'slug': 'contact',
                'content': '''
                <h1>Contact Us</h1>
                <p>Get in touch with our support team:</p>
                
                <h3>Email Support</h3>
                <p>Email: support@socialmarket.com</p>
                
                <h3>Business Hours</h3>
                <p>Monday - Friday: 9:00 AM - 6:00 PM (WAT)</p>
                <p>Saturday: 10:00 AM - 4:00 PM (WAT)</p>
                <p>Sunday: Closed</p>
                
                <h3>Response Time</h3>
                <p>We typically respond to all inquiries within 24 hours.</p>
                '''
            },
            {
                'title': 'Safety Tips',
                'slug': 'safety',
                'content': '''
                <h1>Safety Tips</h1>
                
                <h2>For Buyers</h2>
                <ul>
                    <li>Always verify account details before purchasing</li>
                    <li>Use our secure payment system</li>
                    <li>Change passwords immediately after receiving account access</li>
                    <li>Enable two-factor authentication</li>
                </ul>
                
                <h2>For Sellers</h2>
                <ul>
                    <li>Provide accurate account information</li>
                    <li>Upload clear screenshots as proof</li>
                    <li>Respond promptly to buyer inquiries</li>
                    <li>Only sell accounts you legitimately own</li>
                </ul>
                
                <h2>General Safety</h2>
                <ul>
                    <li>Never share personal information outside our platform</li>
                    <li>Report suspicious activity immediately</li>
                    <li>Keep records of all transactions</li>
                </ul>
                '''
            },
            {
                'title': 'Terms of Service',
                'slug': 'terms',
                'content': '''
                <h1>Terms of Service</h1>
                <p><strong>Last updated:</strong> January 2024</p>
                
                <h2>1. Acceptance of Terms</h2>
                <p>By using SocialMarket, you agree to these terms.</p>
                
                <h2>2. User Accounts</h2>
                <p>You are responsible for maintaining account security and all activities under your account.</p>
                
                <h2>3. Prohibited Activities</h2>
                <ul>
                    <li>Selling fake or compromised accounts</li>
                    <li>Fraudulent transactions</li>
                    <li>Violating platform social media terms</li>
                </ul>
                
                <h2>4. Payment Terms</h2>
                <p>All payments are processed securely. Commission fees apply to transactions.</p>
                
                <h2>5. Dispute Resolution</h2>
                <p>Disputes will be handled through our support system.</p>
                '''
            },
            {
                'title': 'Privacy Policy',
                'slug': 'privacy',
                'content': '''
                <h1>Privacy Policy</h1>
                <p><strong>Last updated:</strong> January 2024</p>
                
                <h2>Information We Collect</h2>
                <ul>
                    <li>Account information (email, username)</li>
                    <li>Transaction data</li>
                    <li>Usage analytics</li>
                </ul>
                
                <h2>How We Use Information</h2>
                <ul>
                    <li>To provide and improve our services</li>
                    <li>To process transactions</li>
                    <li>To communicate important updates</li>
                </ul>
                
                <h2>Data Security</h2>
                <p>We implement security measures to protect your personal information.</p>
                
                <h2>Contact</h2>
                <p>For privacy concerns, contact us at privacy@socialmarket.com</p>
                '''
            },
            {
                'title': 'How It Works',
                'slug': 'how-it-works',
                'content': '''
                <h1>How It Works</h1>
                
                <h2>For Sellers</h2>
                <ol>
                    <li><strong>Create Account:</strong> Sign up and verify your account</li>
                    <li><strong>List Your Account:</strong> Provide details and screenshots</li>
                    <li><strong>Get Approved:</strong> Our team reviews your listing</li>
                    <li><strong>Receive Payment:</strong> Get paid when your account sells</li>
                </ol>
                
                <h2>For Buyers</h2>
                <ol>
                    <li><strong>Browse Accounts:</strong> Find accounts that match your needs</li>
                    <li><strong>Make Payment:</strong> Pay securely through our platform</li>
                    <li><strong>Receive Access:</strong> Get account credentials upon approval</li>
                    <li><strong>Take Ownership:</strong> Change passwords and secure the account</li>
                </ol>
                
                <h2>Our Promise</h2>
                <p>We ensure all transactions are secure and provide support throughout the process.</p>
                '''
            }
        ]

        for page_data in default_pages:
            page = Page(
                title=page_data['title'],
                slug=page_data['slug'],
                content=page_data['content'],
                is_active=True,
                updated_by=1  # Admin user
            )
            db.session.add(page)

        # Update settings with default URLs
        settings = Settings.query.first()
        if settings:
            settings.help_center_url = '/help'
            settings.contact_us_url = '/contact'
            settings.safety_tips_url = '/safety'
            settings.terms_of_service_url = '/terms'
            settings.privacy_policy_url = '/privacy'
            settings.how_it_works_url = '/how-it-works'
            settings.updated_at = datetime.utcnow()

        db.session.commit()
        print("Default pages created successfully!")

if __name__ == '__main__':
    create_default_pages()
#!/usr/bin/env python3
"""Create default pages for footer links"""

from app import app, db
from models import Page

def create_default_pages():
    """Create default pages for footer links"""
    with app.app_context():
        # Default pages to create
        default_pages = [
            {
                'title': 'How It Works',
                'slug': 'how-it-works',
                'content': '''
<h2>How SocialMarket Works</h2>

<div class="row">
    <div class="col-md-4 text-center mb-4">
        <i class="fas fa-user-plus fa-3x text-primary mb-3"></i>
        <h4>1. Create Account</h4>
        <p>Sign up for free and verify your identity to start buying or selling social media accounts.</p>
    </div>
    <div class="col-md-4 text-center mb-4">
        <i class="fas fa-search fa-3x text-success mb-3"></i>
        <h4>2. Browse & Purchase</h4>
        <p>Find the perfect account for your needs and make secure payments with escrow protection.</p>
    </div>
    <div class="col-md-4 text-center mb-4">
        <i class="fas fa-handshake fa-3x text-info mb-3"></i>
        <h4>3. Secure Transfer</h4>
        <p>Receive account credentials safely after verification and payment confirmation.</p>
    </div>
</div>

<h3>For Sellers</h3>
<ul>
    <li>List your social media accounts for free</li>
    <li>Set your own prices</li>
    <li>Get paid securely after successful transfers</li>
    <li>Build your seller reputation</li>
</ul>

<h3>For Buyers</h3>
<ul>
    <li>Browse verified social media accounts</li>
    <li>Make secure payments</li>
    <li>Get instant access after verification</li>
    <li>24/7 customer support</li>
</ul>
                ''',
                'is_published': True
            },
            {
                'title': 'Pricing',
                'slug': 'pricing',
                'content': '''
<h2>Pricing & Fees</h2>

<div class="alert alert-info">
    <h4>Simple, Transparent Pricing</h4>
    <p>No hidden fees, no monthly subscriptions. You only pay when you successfully complete a transaction.</p>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4>For Sellers</h4>
            </div>
            <div class="card-body">
                <ul>
                    <li><strong>Listing Fee:</strong> FREE</li>
                    <li><strong>Success Fee:</strong> 5% of sale price</li>
                    <li><strong>Payment Processing:</strong> Included</li>
                    <li><strong>Customer Support:</strong> Included</li>
                </ul>
                <p class="text-muted">You only pay when you successfully sell an account!</p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4>For Buyers</h4>
            </div>
            <div class="card-body">
                <ul>
                    <li><strong>Browse Accounts:</strong> FREE</li>
                    <li><strong>Purchase Fee:</strong> Included in price</li>
                    <li><strong>Escrow Protection:</strong> FREE</li>
                    <li><strong>Customer Support:</strong> FREE</li>
                </ul>
                <p class="text-muted">No additional fees - the price you see is what you pay!</p>
            </div>
        </div>
    </div>
</div>

<h3>Minimum Amounts</h3>
<ul>
    <li><strong>Minimum Deposit:</strong> ₦100</li>
    <li><strong>Minimum Withdrawal:</strong> ₦500</li>
    <li><strong>Maximum Withdrawal:</strong> ₦50,000 per day</li>
</ul>
                ''',
                'is_published': True
            },
            {
                'title': 'Terms of Service',
                'slug': 'terms-of-service',
                'content': '''
<h2>Terms of Service</h2>

<div class="alert alert-warning">
    <p><strong>Last Updated:</strong> January 2024</p>
</div>

<h3>1. Acceptance of Terms</h3>
<p>By accessing and using SocialMarket, you accept and agree to be bound by the terms and provision of this agreement.</p>

<h3>2. Account Registration</h3>
<ul>
    <li>You must provide accurate and complete information</li>
    <li>You are responsible for maintaining account security</li>
    <li>One account per person is allowed</li>
    <li>You must be at least 18 years old</li>
</ul>

<h3>3. Prohibited Activities</h3>
<ul>
    <li>Selling fake or inactive social media accounts</li>
    <li>Fraudulent payment or verification documents</li>
    <li>Harassment or abusive behavior</li>
    <li>Violating social media platform terms</li>
</ul>

<h3>4. Payment Terms</h3>
<ul>
    <li>All payments are processed in Nigerian Naira (₦)</li>
    <li>Escrow protection for all transactions</li>
    <li>Refunds processed within 7-14 business days</li>
    <li>Service fees are non-refundable</li>
</ul>

<h3>5. Account Verification</h3>
<p>All social media accounts undergo verification before listing. We reserve the right to reject accounts that don't meet our quality standards.</p>

<h3>6. Limitation of Liability</h3>
<p>SocialMarket acts as an intermediary platform. We are not responsible for disputes between buyers and sellers, but we provide mediation services.</p>

<h3>7. Contact Information</h3>
<p>For questions about these terms, please contact us at support@socialmarket.com</p>
                ''',
                'is_published': True
            },
            {
                'title': 'Privacy Policy',
                'slug': 'privacy-policy',
                'content': '''
<h2>Privacy Policy</h2>

<div class="alert alert-info">
    <p><strong>Effective Date:</strong> January 2024</p>
</div>

<h3>Information We Collect</h3>
<ul>
    <li><strong>Personal Information:</strong> Name, email, phone number</li>
    <li><strong>Financial Information:</strong> Bank details for withdrawals</li>
    <li><strong>Usage Data:</strong> How you interact with our platform</li>
    <li><strong>Account Information:</strong> Social media account details you list</li>
</ul>

<h3>How We Use Your Information</h3>
<ul>
    <li>To provide and maintain our service</li>
    <li>To process transactions and payments</li>
    <li>To communicate with you about your account</li>
    <li>To prevent fraud and ensure security</li>
    <li>To improve our platform and services</li>
</ul>

<h3>Information Sharing</h3>
<p>We do not sell, trade, or rent your personal information to third parties. We may share information only:</p>
<ul>
    <li>With your explicit consent</li>
    <li>To comply with legal requirements</li>
    <li>To protect our rights and prevent fraud</li>
    <li>With service providers who assist our operations</li>
</ul>

<h3>Data Security</h3>
<p>We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.</p>

<h3>Your Rights</h3>
<ul>
    <li>Access your personal data</li>
    <li>Correct inaccurate information</li>
    <li>Request deletion of your data</li>
    <li>Withdraw consent for data processing</li>
</ul>

<h3>Contact Us</h3>
<p>If you have questions about this Privacy Policy, contact us at privacy@socialmarket.com</p>
                ''',
                'is_published': True
            },
            {
                'title': 'Safety Tips',
                'slug': 'safety-tips',
                'content': '''
<h2>Safety Tips</h2>

<div class="alert alert-success">
    <h4><i class="fas fa-shield-alt"></i> Your Safety is Our Priority</h4>
    <p>Follow these guidelines to ensure safe and successful transactions on SocialMarket.</p>
</div>

<h3>For Buyers</h3>
<div class="card mb-4">
    <div class="card-body">
        <h5><i class="fas fa-search text-primary"></i> Before Purchasing</h5>
        <ul>
            <li>Verify account statistics and engagement rates</li>
            <li>Check seller ratings and reviews</li>
            <li>Ask questions about the account history</li>
            <li>Ensure account matches your target audience</li>
        </ul>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5><i class="fas fa-credit-card text-success"></i> During Purchase</h5>
        <ul>
            <li>Only pay through our secure platform</li>
            <li>Never share personal financial information</li>
            <li>Keep all communication on the platform</li>
            <li>Document any issues immediately</li>
        </ul>
    </div>
</div>

<h3>For Sellers</h3>
<div class="card mb-4">
    <div class="card-body">
        <h5><i class="fas fa-list text-info"></i> When Listing</h5>
        <ul>
            <li>Provide accurate account information</li>
            <li>Upload genuine screenshots</li>
            <li>Set fair and competitive prices</li>
            <li>Respond promptly to buyer inquiries</li>
        </ul>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5><i class="fas fa-handshake text-warning"></i> During Sale</h5>
        <ul>
            <li>Wait for payment confirmation</li>
            <li>Transfer accounts only after verification</li>
            <li>Provide complete account access</li>
            <li>Maintain professionalism</li>
        </ul>
    </div>
</div>

<h3>Red Flags to Avoid</h3>
<div class="alert alert-danger">
    <ul>
        <li>Requests for payment outside the platform</li>
        <li>Pressure to complete transactions quickly</li>
        <li>Accounts with suspicious engagement patterns</li>
        <li>Sellers unwilling to provide verification</li>
        <li>Prices significantly below market value</li>
    </ul>
</div>

<h3>Get Help</h3>
<p>If you encounter any issues or have concerns, contact our support team immediately at support@socialmarket.com</p>
                ''',
                'is_published': True
            }
        ]
        
        # Create pages
        for page_data in default_pages:
            # Check if page already exists
            existing_page = Page.query.filter_by(slug=page_data['slug']).first()
            if not existing_page:
                page = Page(
                    title=page_data['title'],
                    slug=page_data['slug'],
                    content=page_data['content'],
                    is_published=page_data['is_published']
                )
                db.session.add(page)
                print(f"Created page: {page_data['title']}")
            else:
                print(f"Page already exists: {page_data['title']}")
        
        db.session.commit()
        print("Default pages created successfully!")

if __name__ == '__main__':
    create_default_pages()
