
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
