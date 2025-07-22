
from run import app, db
from models import Page, User
from datetime import datetime

def create_default_pages():
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(role='admin').first()
        admin_id = admin.id if admin else None
        
        default_pages = [
            {
                'slug': 'privacy-policy',
                'title': 'Privacy Policy',
                'content': '''
                <h2>Privacy Policy</h2>
                <p><em>Last updated: January 2025</em></p>
                
                <h3>Information We Collect</h3>
                <ul>
                    <li>Account information (email, username)</li>
                    <li>Profile details</li>
                    <li>Transaction history</li>
                    <li>Communication records</li>
                </ul>
                
                <h3>How We Use Your Information</h3>
                <ul>
                    <li>To provide and maintain our service</li>
                    <li>To process transactions</li>
                    <li>To communicate with you</li>
                    <li>To improve our platform</li>
                </ul>
                
                <h3>Information Sharing</h3>
                <p>We do not sell or share your personal information with third parties except as described in this policy.</p>
                
                <h3>Data Security</h3>
                <p>We implement appropriate security measures to protect your information.</p>
                
                <h3>Contact Us</h3>
                <p>If you have questions about this privacy policy, please contact us.</p>
                ''',
                'meta_description': 'Privacy policy explaining how we collect, use, and protect your personal information.',
                'seo_title': 'Privacy Policy - Data Protection',
                'seo_keywords': 'privacy, policy, data protection, personal information, security'
            },
            {
                'slug': 'terms-of-service',
                'title': 'Terms of Service',
                'content': '''
                <h2>Terms of Service</h2>
                <p><em>Last updated: January 2025</em></p>
                
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
                'slug': 'refund-policy',
                'title': 'Refund Policy',
                'content': '''
                <h2>Refund Policy</h2>
                <p><em>Last updated: January 2025</em></p>
                
                <h3>Refund Eligibility</h3>
                <ul>
                    <li>Account not delivered within 24 hours</li>
                    <li>Account information is incorrect or invalid</li>
                    <li>Account has been banned or suspended</li>
                    <li>Seller misrepresented account details</li>
                </ul>
                
                <h3>Refund Process</h3>
                <ol>
                    <li>Contact our support team within 48 hours</li>
                    <li>Provide proof of the issue</li>
                    <li>Allow up to 5 business days for investigation</li>
                    <li>Refund will be processed to your wallet</li>
                </ol>
                
                <h3>Non-Refundable Items</h3>
                <ul>
                    <li>Accounts successfully delivered and working</li>
                    <li>Digital goods that have been downloaded</li>
                    <li>Custom work that has been completed</li>
                </ul>
                
                <h3>Contact Support</h3>
                <p>For refund requests, please contact our support team with your order details.</p>
                ''',
                'meta_description': 'Refund policy for social media account purchases and marketplace transactions.',
                'seo_title': 'Refund Policy - Money Back Guarantee',
                'seo_keywords': 'refund, policy, money back, guarantee, return, support'
            },
            {
                'slug': 'cookie-policy',
                'title': 'Cookie Policy',
                'content': '''
                <h2>Cookie Policy</h2>
                <p><em>Last updated: January 2025</em></p>
                
                <h3>What Are Cookies</h3>
                <p>Cookies are small text files that are stored on your device when you visit our website.</p>
                
                <h3>Types of Cookies We Use</h3>
                <ul>
                    <li><strong>Essential Cookies:</strong> Required for the website to function</li>
                    <li><strong>Analytics Cookies:</strong> Help us understand how you use our site</li>
                    <li><strong>Preference Cookies:</strong> Remember your settings and preferences</li>
                </ul>
                
                <h3>Managing Cookies</h3>
                <p>You can control and delete cookies through your browser settings. Note that disabling certain cookies may affect website functionality.</p>
                
                <h3>Third-Party Cookies</h3>
                <p>We may use third-party services that place cookies on your device for analytics and advertising purposes.</p>
                
                <h3>Contact Us</h3>
                <p>If you have questions about our cookie policy, please contact us.</p>
                ''',
                'meta_description': 'Cookie policy explaining how we use cookies and similar technologies on our website.',
                'seo_title': 'Cookie Policy - Website Cookies',
                'seo_keywords': 'cookies, policy, tracking, analytics, privacy, browser'
            },
            {
                'slug': 'help',
                'title': 'Help Center',
                'content': '''
                <h2>Help Center</h2>
                
                <h3>Getting Started</h3>
                <h4>How to Buy an Account</h4>
                <ol>
                    <li>Browse our marketplace</li>
                    <li>Select an account you want to purchase</li>
                    <li>Choose your payment method</li>
                    <li>Complete the transaction</li>
                    <li>Receive account details</li>
                </ol>
                
                <h4>How to Sell an Account</h4>
                <ol>
                    <li>Create a seller account</li>
                    <li>List your social media account</li>
                    <li>Wait for admin approval</li>
                    <li>Receive purchase notifications</li>
                    <li>Deliver account details to buyer</li>
                </ol>
                
                <h3>Payment Methods</h3>
                <ul>
                    <li>Wallet balance</li>
                    <li>Bank transfer</li>
                    <li>Cash deposit</li>
                </ul>
                
                <h3>Common Questions</h3>
                <h4>Is it safe to buy accounts here?</h4>
                <p>Yes, we verify all accounts before approval and offer buyer protection.</p>
                
                <h4>How long does delivery take?</h4>
                <p>Most accounts are delivered within 24 hours of purchase.</p>
                
                <h3>Contact Support</h3>
                <p>Need more help? Contact our support team for assistance.</p>
                ''',
                'meta_description': 'Help center with guides for buying and selling social media accounts safely.',
                'seo_title': 'Help Center - Support and Guides',
                'seo_keywords': 'help, support, guide, tutorial, faq, assistance'
            },
            {
                'slug': 'contact',
                'title': 'Contact Us',
                'content': '''
                <h2>Contact Us</h2>
                
                <h3>Get in Touch</h3>
                <p>We're here to help! Contact us through any of the following methods:</p>
                
                <h3>Support Channels</h3>
                <ul>
                    <li><strong>Email:</strong> support@socialmarket.com</li>
                    <li><strong>WhatsApp:</strong> +1234567890</li>
                    <li><strong>Telegram:</strong> @socialmarketsupport</li>
                </ul>
                
                <h3>Business Hours</h3>
                <ul>
                    <li>Monday - Friday: 9:00 AM - 6:00 PM</li>
                    <li>Saturday: 10:00 AM - 4:00 PM</li>
                    <li>Sunday: Closed</li>
                </ul>
                
                <h3>Response Times</h3>
                <ul>
                    <li>Email: Within 24 hours</li>
                    <li>WhatsApp: Within 2 hours</li>
                    <li>Telegram: Within 1 hour</li>
                </ul>
                
                <h3>Before Contacting Us</h3>
                <p>Please check our Help Center for answers to common questions.</p>
                
                <p>We look forward to hearing from you!</p>
                ''',
                'meta_description': 'Contact information and support channels for customer assistance.',
                'seo_title': 'Contact Us - Customer Support',
                'seo_keywords': 'contact, support, help, email, whatsapp, telegram'
            },
            {
                'slug': 'safety-tips',
                'title': 'Safety Tips',
                'content': '''
                <h2>Safety Tips</h2>
                
                <h3>For Buyers</h3>
                <ul>
                    <li>Always use our secure payment system</li>
                    <li>Verify account details before purchase</li>
                    <li>Check seller ratings and reviews</li>
                    <li>Report suspicious listings</li>
                    <li>Change passwords immediately after purchase</li>
                </ul>
                
                <h3>For Sellers</h3>
                <ul>
                    <li>Provide accurate account information</li>
                    <li>Upload genuine screenshots</li>
                    <li>Respond promptly to buyer inquiries</li>
                    <li>Only sell accounts you own</li>
                    <li>Follow platform guidelines</li>
                </ul>
                
                <h3>Red Flags to Watch For</h3>
                <ul>
                    <li>Requests for payment outside the platform</li>
                    <li>Accounts with suspicious activity</li>
                    <li>Sellers with no ratings or reviews</li>
                    <li>Prices that seem too good to be true</li>
                    <li>Poor quality screenshots or descriptions</li>
                </ul>
                
                <h3>Reporting Issues</h3>
                <p>If you encounter any problems, report them to our support team immediately.</p>
                
                <h3>Account Security</h3>
                <ul>
                    <li>Use strong, unique passwords</li>
                    <li>Enable two-factor authentication</li>
                    <li>Keep your account information private</li>
                    <li>Log out from shared devices</li>
                </ul>
                ''',
                'meta_description': 'Important safety tips for buying and selling social media accounts securely.',
                'seo_title': 'Safety Tips - Secure Trading',
                'seo_keywords': 'safety, security, tips, trading, protection, scam prevention'
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
        print("Default pages initialized successfully!")

if __name__ == '__main__':
    create_default_pages()
