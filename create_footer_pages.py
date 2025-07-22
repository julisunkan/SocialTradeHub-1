
from app import app, db
from models import Page
from datetime import datetime

def create_footer_pages():
    with app.app_context():
        # Create default pages if they don't exist
        pages_data = [
            {
                'title': 'Help Center',
                'slug': 'help-center',
                'content': '''
                <div class="container py-5">
                    <h1>Help Center</h1>
                    <div class="row">
                        <div class="col-md-6">
                            <h3>Getting Started</h3>
                            <ul>
                                <li>How to create an account</li>
                                <li>How to buy social media accounts</li>
                                <li>How to sell your accounts</li>
                                <li>Payment methods and wallet</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h3>Account Security</h3>
                            <ul>
                                <li>Verifying account authenticity</li>
                                <li>Safe transaction practices</li>
                                <li>Reporting suspicious activity</li>
                                <li>Account recovery process</li>
                            </ul>
                        </div>
                    </div>
                    <div class="mt-4">
                        <h3>Need More Help?</h3>
                        <p>Contact our support team at support@socialmarket.com or use our live chat feature.</p>
                    </div>
                </div>
                ''',
                'meta_description': 'Get help with using SocialMarket - your trusted marketplace for social media accounts'
            },
            {
                'title': 'Contact Us',
                'slug': 'contact-us',
                'content': '''
                <div class="container py-5">
                    <h1>Contact Us</h1>
                    <div class="row">
                        <div class="col-md-8">
                            <div class="card">
                                <div class="card-body">
                                    <h3>Get in Touch</h3>
                                    <form>
                                        <div class="mb-3">
                                            <label class="form-label">Name</label>
                                            <input type="text" class="form-control" required>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Email</label>
                                            <input type="email" class="form-control" required>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Subject</label>
                                            <input type="text" class="form-control" required>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Message</label>
                                            <textarea class="form-control" rows="5" required></textarea>
                                        </div>
                                        <button type="submit" class="btn btn-primary">Send Message</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <h3>Contact Information</h3>
                            <p><strong>Email:</strong> support@socialmarket.com</p>
                            <p><strong>Phone:</strong> +234 901 234 5678</p>
                            <p><strong>Address:</strong> Lagos, Nigeria</p>
                            <p><strong>Business Hours:</strong> Mon-Fri 9AM-6PM WAT</p>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Contact SocialMarket support team for help with buying and selling social media accounts'
            },
            {
                'title': 'Safety Tips',
                'slug': 'safety-tips',
                'content': '''
                <div class="container py-5">
                    <h1>Safety Tips</h1>
                    <div class="alert alert-warning">
                        <i class="fas fa-shield-alt me-2"></i>
                        Your safety is our priority. Follow these tips to ensure secure transactions.
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <h3>For Buyers</h3>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">✅ Always use our escrow system</li>
                                <li class="list-group-item">✅ Verify account metrics before purchase</li>
                                <li class="list-group-item">✅ Check seller's reputation and reviews</li>
                                <li class="list-group-item">✅ Ask for account verification</li>
                                <li class="list-group-item">❌ Never pay outside the platform</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h3>For Sellers</h3>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">✅ Provide accurate account information</li>
                                <li class="list-group-item">✅ Upload genuine screenshots</li>
                                <li class="list-group-item">✅ Respond to buyer questions promptly</li>
                                <li class="list-group-item">✅ Transfer accounts only after payment confirmation</li>
                                <li class="list-group-item">❌ Never share personal information</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <h3>Red Flags to Watch Out For</h3>
                        <div class="alert alert-danger">
                            <ul class="mb-0">
                                <li>Requests to communicate outside the platform</li>
                                <li>Unrealistic follower counts or engagement rates</li>
                                <li>Pressure to complete transactions quickly</li>
                                <li>Accounts with suspicious or stolen content</li>
                            </ul>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Stay safe while buying and selling social media accounts on SocialMarket'
            },
            {
                'title': 'Terms of Service',
                'slug': 'terms-of-service',
                'content': '''
                <div class="container py-5">
                    <h1>Terms of Service</h1>
                    <p><em>Last updated: January 2024</em></p>
                    
                    <h3>1. Acceptance of Terms</h3>
                    <p>By accessing and using SocialMarket, you accept and agree to be bound by the terms and provision of this agreement.</p>
                    
                    <h3>2. Account Registration</h3>
                    <p>Users must provide accurate and complete information when creating an account. You are responsible for maintaining the security of your account credentials.</p>
                    
                    <h3>3. Prohibited Activities</h3>
                    <ul>
                        <li>Selling fake or fraudulent accounts</li>
                        <li>Using bots or automation tools</li>
                        <li>Engaging in money laundering or fraud</li>
                        <li>Violating platform policies of social media networks</li>
                    </ul>
                    
                    <h3>4. Payment and Fees</h3>
                    <p>SocialMarket charges a commission on successful transactions. All fees are clearly displayed before completing a purchase.</p>
                    
                    <h3>5. Dispute Resolution</h3>
                    <p>Disputes will be handled through our internal resolution process. We reserve the right to make final decisions on disputed transactions.</p>
                    
                    <h3>6. Limitation of Liability</h3>
                    <p>SocialMarket is not liable for any damages arising from the use of our platform beyond the transaction amount.</p>
                    
                    <h3>7. Changes to Terms</h3>
                    <p>We reserve the right to modify these terms at any time. Continued use of the platform constitutes acceptance of modified terms.</p>
                </div>
                ''',
                'meta_description': 'Terms of Service for SocialMarket - social media account marketplace'
            },
            {
                'title': 'Privacy Policy',
                'slug': 'privacy-policy',
                'content': '''
                <div class="container py-5">
                    <h1>Privacy Policy</h1>
                    <p><em>Last updated: January 2024</em></p>
                    
                    <h3>Information We Collect</h3>
                    <p>We collect information you provide directly to us, such as when you create an account, make a purchase, or contact us for support.</p>
                    
                    <h3>How We Use Your Information</h3>
                    <ul>
                        <li>To provide and maintain our services</li>
                        <li>To process transactions and send notifications</li>
                        <li>To improve our platform and user experience</li>
                        <li>To comply with legal obligations</li>
                    </ul>
                    
                    <h3>Information Sharing</h3>
                    <p>We do not sell, trade, or rent your personal information to third parties. We may share information only in the following circumstances:</p>
                    <ul>
                        <li>With your consent</li>
                        <li>To comply with legal requirements</li>
                        <li>To protect our rights and safety</li>
                    </ul>
                    
                    <h3>Data Security</h3>
                    <p>We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.</p>
                    
                    <h3>Contact Us</h3>
                    <p>If you have questions about this Privacy Policy, please contact us at privacy@socialmarket.com</p>
                </div>
                ''',
                'meta_description': 'Privacy Policy for SocialMarket - how we protect your personal information'
            },
            {
                'title': 'Refund Policy',
                'slug': 'refund-policy',
                'content': '''
                <div class="container py-5">
                    <h1>Refund Policy</h1>
                    
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        We strive to ensure all transactions are completed successfully. However, we understand that issues may arise.
                    </div>
                    
                    <h3>Eligible Refund Scenarios</h3>
                    <ul class="list-group">
                        <li class="list-group-item">Account credentials provided are incorrect or non-functional</li>
                        <li class="list-group-item">Account was suspended or banned before transfer</li>
                        <li class="list-group-item">Significant misrepresentation of account metrics</li>
                        <li class="list-group-item">Seller fails to transfer account within 24 hours</li>
                    </ul>
                    
                    <h3>Refund Process</h3>
                    <ol>
                        <li>Contact our support team within 48 hours of purchase</li>
                        <li>Provide detailed explanation and evidence of the issue</li>
                        <li>Our team will investigate the claim</li>
                        <li>If approved, refund will be processed within 3-5 business days</li>
                    </ol>
                    
                    <h3>Non-Refundable Situations</h3>
                    <ul>
                        <li>Change of mind after successful account transfer</li>
                        <li>Account suspended due to buyer's actions</li>
                        <li>Minor discrepancies in follower counts (less than 5%)</li>
                    </ul>
                    
                    <h3>Contact Support</h3>
                    <p>For refund requests, email us at refunds@socialmarket.com with your transaction ID and detailed explanation.</p>
                </div>
                ''',
                'meta_description': 'SocialMarket refund policy - when and how to request refunds for social media account purchases'
            },
            {
                'title': 'Cookie Policy',
                'slug': 'cookie-policy',
                'content': '''
                <div class="container py-5">
                    <h1>Cookie Policy</h1>
                    
                    <h3>What Are Cookies?</h3>
                    <p>Cookies are small text files that are stored on your device when you visit our website. They help us provide you with a better experience by remembering your preferences and analyzing how you use our site.</p>
                    
                    <h3>Types of Cookies We Use</h3>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <h4>Essential Cookies</h4>
                            <p>These cookies are necessary for the website to function properly. They enable basic features like page navigation and access to secure areas.</p>
                        </div>
                        <div class="col-md-6">
                            <h4>Analytics Cookies</h4>
                            <p>These cookies help us understand how visitors interact with our website by collecting and reporting information anonymously.</p>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <h4>Functional Cookies</h4>
                            <p>These cookies remember your preferences and choices to provide enhanced, personalized features.</p>
                        </div>
                        <div class="col-md-6">
                            <h4>Marketing Cookies</h4>
                            <p>These cookies track your online activity to help advertisers deliver more relevant advertising.</p>
                        </div>
                    </div>
                    
                    <h3>Managing Cookies</h3>
                    <p>You can control and manage cookies in various ways:</p>
                    <ul>
                        <li>Browser settings: Most browsers allow you to manage cookie preferences</li>
                        <li>Third-party tools: Various online tools can help manage cookies</li>
                        <li>Opt-out links: Many advertising networks provide opt-out mechanisms</li>
                    </ul>
                    
                    <div class="alert alert-warning">
                        <strong>Note:</strong> Disabling certain cookies may impact your experience on our website.
                    </div>
                </div>
                ''',
                'meta_description': 'Learn about how SocialMarket uses cookies and how to manage your cookie preferences'
            },
            {
                'title': 'How It Works',
                'slug': 'how-it-works',
                'content': '''
                <div class="container py-5">
                    <h1>How SocialMarket Works</h1>
                    <p class="lead">Your complete guide to buying and selling social media accounts safely</p>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <h2>For Buyers</h2>
                            <div class="timeline">
                                <div class="step">
                                    <div class="step-number">1</div>
                                    <h4>Browse Accounts</h4>
                                    <p>Search through our verified collection of social media accounts from Instagram, TikTok, YouTube, and more.</p>
                                </div>
                                <div class="step">
                                    <div class="step-number">2</div>
                                    <h4>Review Details</h4>
                                    <p>Check follower counts, engagement rates, niche, and account history before making a decision.</p>
                                </div>
                                <div class="step">
                                    <div class="step-number">3</div>
                                    <h4>Secure Purchase</h4>
                                    <p>Use our escrow system to make safe payments. Your money is protected until you receive the account.</p>
                                </div>
                                <div class="step">
                                    <div class="step-number">4</div>
                                    <h4>Get Access</h4>
                                    <p>Receive login credentials and take control of your new social media account immediately.</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <h2>For Sellers</h2>
                            <div class="timeline">
                                <div class="step">
                                    <div class="step-number">1</div>
                                    <h4>List Your Account</h4>
                                    <p>Create a detailed listing with accurate follower counts, engagement metrics, and high-quality screenshots.</p>
                                </div>
                                <div class="step">
                                    <div class="step-number">2</div>
                                    <h4>Verification Process</h4>
                                    <p>Our team reviews your listing to ensure authenticity and compliance with our quality standards.</p>
                                </div>
                                <div class="step">
                                    <div class="step-number">3</div>
                                    <h4>Receive Offers</h4>
                                    <p>Connect with potential buyers and answer their questions about your account.</p>
                                </div>
                                <div class="step">
                                    <div class="step-number">4</div>
                                    <h4>Complete Sale</h4>
                                    <p>Transfer the account securely and receive payment directly to your wallet.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-5">
                        <h2>Why Choose SocialMarket?</h2>
                        <div class="row">
                            <div class="col-md-4 text-center">
                                <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                                <h4>Secure Escrow</h4>
                                <p>Your payments are protected until you receive your account</p>
                            </div>
                            <div class="col-md-4 text-center">
                                <i class="fas fa-check-circle fa-3x text-success mb-3"></i>
                                <h4>Verified Accounts</h4>
                                <p>All accounts are manually reviewed for authenticity</p>
                            </div>
                            <div class="col-md-4 text-center">
                                <i class="fas fa-headset fa-3x text-info mb-3"></i>
                                <h4>24/7 Support</h4>
                                <p>Our team is always here to help with any questions</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <style>
                .timeline .step {
                    margin-bottom: 2rem;
                    padding-left: 4rem;
                    position: relative;
                }
                .step-number {
                    position: absolute;
                    left: 0;
                    top: 0;
                    width: 2.5rem;
                    height: 2.5rem;
                    background: #007bff;
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                }
                </style>
                ''',
                'meta_description': 'Learn how to buy and sell social media accounts safely on SocialMarket'
            },
            {
                'title': 'Pricing',
                'slug': 'pricing',
                'content': '''
                <div class="container py-5">
                    <h1>Pricing & Fees</h1>
                    <p class="lead">Transparent pricing with no hidden fees</p>
                    
                    <div class="row">
                        <div class="col-lg-8">
                            <div class="card">
                                <div class="card-header bg-primary text-white">
                                    <h3 class="mb-0">Commission Structure</h3>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <h4>For Buyers</h4>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item d-flex justify-content-between">
                                                    <span>Platform Fee</span>
                                                    <strong>5%</strong>
                                                </li>
                                                <li class="list-group-item d-flex justify-content-between">
                                                    <span>Payment Processing</span>
                                                    <strong>2.5%</strong>
                                                </li>
                                                <li class="list-group-item d-flex justify-content-between">
                                                    <span>Escrow Protection</span>
                                                    <strong>Free</strong>
                                                </li>
                                            </ul>
                                        </div>
                                        <div class="col-md-6">
                                            <h4>For Sellers</h4>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item d-flex justify-content-between">
                                                    <span>Listing Fee</span>
                                                    <strong>Free</strong>
                                                </li>
                                                <li class="list-group-item d-flex justify-content-between">
                                                    <span>Success Fee</span>
                                                    <strong>5%</strong>
                                                </li>
                                                <li class="list-group-item d-flex justify-content-between">
                                                    <span>Withdrawal Fee</span>
                                                    <strong>₦100</strong>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                    
                                    <div class="alert alert-info mt-4">
                                        <i class="fas fa-info-circle me-2"></i>
                                        All fees are automatically calculated and displayed before you complete any transaction.
                                    </div>
                                </div>
                            </div>
                            
                            <div class="card mt-4">
                                <div class="card-header">
                                    <h3 class="mb-0">Payment Methods</h3>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <h5>Accepted Methods</h5>
                                            <ul>
                                                <li>Bank Transfer (Nigeria)</li>
                                                <li>SocialMarket Wallet</li>
                                                <li>Mobile Money (Coming Soon)</li>
                                                <li>Cryptocurrency (Coming Soon)</li>
                                            </ul>
                                        </div>
                                        <div class="col-md-6">
                                            <h5>Processing Times</h5>
                                            <ul>
                                                <li>Wallet: Instant</li>
                                                <li>Bank Transfer: 1-3 hours</li>
                                                <li>Withdrawals: 24-48 hours</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-lg-4">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h4>Need Help?</h4>
                                    <p>Have questions about our pricing or need a custom quote for bulk purchases?</p>
                                    <a href="/contact-us" class="btn btn-primary">Contact Support</a>
                                </div>
                            </div>
                            
                            <div class="card mt-4">
                                <div class="card-body">
                                    <h5>Fee Calculator</h5>
                                    <div class="mb-3">
                                        <label class="form-label">Account Price</label>
                                        <input type="number" class="form-control" id="priceInput" placeholder="Enter price in ₦">
                                    </div>
                                    <div class="alert alert-secondary">
                                        <small>Total Cost: <span id="totalCost">₦0.00</span></small><br>
                                        <small>Platform Fee: <span id="platformFee">₦0.00</span></small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                document.getElementById('priceInput').addEventListener('input', function() {
                    const price = parseFloat(this.value) || 0;
                    const platformFee = price * 0.075; // 5% + 2.5%
                    const total = price + platformFee;
                    
                    document.getElementById('platformFee').textContent = '₦' + platformFee.toFixed(2);
                    document.getElementById('totalCost').textContent = '₦' + total.toFixed(2);
                });
                </script>
                ''',
                'meta_description': 'SocialMarket pricing and fees for buying and selling social media accounts'
            }
        ]
        
        for page_data in pages_data:
            existing_page = Page.query.filter_by(slug=page_data['slug']).first()
            if not existing_page:
                page = Page(
                    title=page_data['title'],
                    slug=page_data['slug'],
                    content=page_data['content'],
                    meta_description=page_data['meta_description'],
                    seo_title=page_data['title'],
                    is_active=True,
                    updated_by=1  # Admin user ID
                )
                db.session.add(page)
                print(f"Created page: {page_data['title']}")
            else:
                print(f"Page already exists: {page_data['title']}")
        
        db.session.commit()
        print("Footer pages created successfully!")

if __name__ == '__main__':
    create_footer_pages()
