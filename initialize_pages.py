
from run import app, db
from models import Page, User

def create_default_pages():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Get admin user
        admin = User.query.filter_by(role='admin').first()
        admin_id = admin.id if admin else None
        
        # Default pages content
        default_pages = [
            {
                'slug': 'help',
                'title': 'Help Center',
                'content': '''
                <h2>Welcome to our Help Center</h2>
                <p>Find answers to common questions and get support for using our platform.</p>
                
                <h3>Getting Started</h3>
                <ul>
                    <li>How to create an account</li>
                    <li>How to list your social media account</li>
                    <li>How to purchase an account</li>
                    <li>Understanding our verification process</li>
                </ul>
                
                <h3>Account Management</h3>
                <ul>
                    <li>Managing your profile</li>
                    <li>Wallet and payments</li>
                    <li>Security settings</li>
                </ul>
                
                <h3>Need More Help?</h3>
                <p>If you can't find what you're looking for, please contact our support team.</p>
                ''',
                'meta_description': 'Get help and support for using our social media marketplace platform.',
                'seo_title': 'Help Center - Get Support',
                'seo_keywords': 'help, support, faq, guide, tutorial'
            },
            {
                'slug': 'contact',
                'title': 'Contact Us',
                'content': '''
                <h2>Get in Touch</h2>
                <p>We'd love to hear from you. Here's how you can reach us.</p>
                
                <div style="margin: 2rem 0;">
                    <h3>Customer Support</h3>
                    <p><strong>Email:</strong> support@socialmarket.com</p>
                    <p><strong>Response Time:</strong> Within 24 hours</p>
                </div>
                
                <div style="margin: 2rem 0;">
                    <h3>Business Inquiries</h3>
                    <p><strong>Email:</strong> business@socialmarket.com</p>
                    <p>For partnerships, advertising, and business opportunities</p>
                </div>
                
                <div style="margin: 2rem 0;">
                    <h3>Office Hours</h3>
                    <p>Monday - Friday: 9:00 AM - 6:00 PM (GMT)</p>
                    <p>Saturday: 10:00 AM - 4:00 PM (GMT)</p>
                    <p>Sunday: Closed</p>
                </div>
                ''',
                'meta_description': 'Contact our support team for help with your social media marketplace needs.',
                'seo_title': 'Contact Us - Get Support',
                'seo_keywords': 'contact, support, email, help, customer service'
            },
            {
                'slug': 'safety-tips',
                'title': 'Safety Tips',
                'content': '''
                <h2>Stay Safe While Trading</h2>
                <p>Your security is our priority. Follow these guidelines to protect yourself.</p>
                
                <h3>For Buyers</h3>
                <ul>
                    <li>Always verify account details before purchasing</li>
                    <li>Use our secure payment system</li>
                    <li>Check seller ratings and reviews</li>
                    <li>Report suspicious activity immediately</li>
                </ul>
                
                <h3>For Sellers</h3>
                <ul>
                    <li>Provide accurate account information</li>
                    <li>Respond to buyer inquiries promptly</li>
                    <li>Transfer account details securely</li>
                    <li>Keep records of all transactions</li>
                </ul>
                
                <h3>Red Flags</h3>
                <ul>
                    <li>Requests for payment outside our platform</li>
                    <li>Accounts with no verification</li>
                    <li>Prices that seem too good to be true</li>
                    <li>Pressure to complete transactions quickly</li>
                </ul>
                
                <p><strong>Remember:</strong> If something doesn't feel right, trust your instincts and contact our support team.</p>
                ''',
                'meta_description': 'Important safety tips for buying and selling social media accounts securely.',
                'seo_title': 'Safety Tips - Secure Trading',
                'seo_keywords': 'safety, security, tips, trading, protection, scam prevention'
            },
            {
                'slug': 'terms-of-service',
                'title': 'Terms of Service',
                'content': '''
                <h2>Terms of Service</h2>
                <p><em>Last updated: [Date]</em></p>
                
                <h3>1. Acceptance of Terms</h3>
                <p>By using our platform, you agree to these terms and conditions.</p>
                
                <h3>2. User Responsibilities</h3>
                <ul>
                    <li>Provide accurate information</li>
                    <li>Comply with all applicable laws</li>
                    <li>Respect other users</li>
                    <li>Use the platform for lawful purposes only</li>
                </ul>
                
                <h3>3. Account Trading</h3>
                <p>Users are responsible for ensuring they have the right to sell social media accounts and that all account information is accurate.</p>
                
                <h3>4. Prohibited Activities</h3>
                <ul>
                    <li>Selling fake or compromised accounts</li>
                    <li>Fraudulent activities</li>
                    <li>Harassment of other users</li>
                    <li>Violation of platform policies</li>
                </ul>
                
                <h3>5. Limitation of Liability</h3>
                <p>Our platform serves as a marketplace. We are not responsible for disputes between buyers and sellers.</p>
                
                <h3>6. Changes to Terms</h3>
                <p>We reserve the right to modify these terms at any time. Users will be notified of significant changes.</p>
                
                <p>For questions about these terms, please contact us.</p>
                ''',
                'meta_description': 'Terms of service and user agreement for our social media marketplace.',
                'seo_title': 'Terms of Service - User Agreement',
                'seo_keywords': 'terms, service, agreement, legal, conditions, policy'
            },
            {
                'slug': 'privacy-policy',
                'title': 'Privacy Policy',
                'content': '''
                <h2>Privacy Policy</h2>
                <p><em>Last updated: [Date]</em></p>
                
                <h3>Information We Collect</h3>
                <ul>
                    <li>Account information (email, username)</li>
                    <li>Profile details</li>
                    <li>Transaction history</li>
                    <li>Communication records</li>
                </ul>
                
                <h3>How We Use Your Information</h3>
                <ul>
                    <li>To provide our services</li>
                    <li>To process transactions</li>
                    <li>To communicate with you</li>
                    <li>To improve our platform</li>
                </ul>
                
                <h3>Information Sharing</h3>
                <p>We do not sell or share your personal information with third parties except as required by law or with your consent.</p>
                
                <h3>Data Security</h3>
                <p>We implement appropriate security measures to protect your personal information.</p>
                
                <h3>Your Rights</h3>
                <ul>
                    <li>Access your personal data</li>
                    <li>Correct inaccurate information</li>
                    <li>Delete your account</li>
                    <li>Export your data</li>
                </ul>
                
                <h3>Contact Us</h3>
                <p>For privacy-related questions, contact us at privacy@socialmarket.com</p>
                ''',
                'meta_description': 'Our privacy policy explaining how we collect, use, and protect your personal information.',
                'seo_title': 'Privacy Policy - Data Protection',
                'seo_keywords': 'privacy, policy, data, protection, personal information, security'
            }
        ]
        
        for page_data in default_pages:
            # Check if page already exists
            existing_page = Page.query.filter_by(slug=page_data['slug']).first()
            if not existing_page:
                page = Page(
                    slug=page_data['slug'],
                    title=page_data['title'],
                    content=page_data['content'],
                    meta_description=page_data['meta_description'],
                    seo_title=page_data['seo_title'],
                    seo_keywords=page_data['seo_keywords'],
                    is_active=True,
                    updated_by=admin_id
                )
                db.session.add(page)
                print(f"Created page: {page_data['title']}")
            else:
                print(f"Page already exists: {page_data['title']}")
        
        db.session.commit()
        print("Default pages initialization completed!")

if __name__ == '__main__':
    create_default_pages()
