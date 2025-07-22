
#!/usr/bin/env python3
"""Create demo footer pages for the social media marketplace"""

from app import app, db
from models import Page, Settings, User
from datetime import datetime

def create_demo_footer_pages():
    with app.app_context():
        # Get admin user ID
        admin = User.query.filter_by(role='admin').first()
        admin_id = admin.id if admin else 1
        
        # Demo pages data
        pages_data = [
            {
                'title': 'Help Center',
                'slug': 'help-center',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Help Center</h1>
                            
                            <div class="row">
                                <div class="col-md-6 mb-4">
                                    <div class="card border-0 shadow-sm h-100">
                                        <div class="card-body">
                                            <h4 class="text-primary"><i class="fas fa-user-plus me-2"></i>Getting Started</h4>
                                            <ul class="list-unstyled">
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Create your account</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Verify your identity</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Browse available accounts</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Make secure purchases</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-md-6 mb-4">
                                    <div class="card border-0 shadow-sm h-100">
                                        <div class="card-body">
                                            <h4 class="text-info"><i class="fas fa-shield-alt me-2"></i>Account Security</h4>
                                            <ul class="list-unstyled">
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Verify account authenticity</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Safe transaction practices</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Report suspicious activity</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Account recovery process</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="text-center mt-5">
                                <h3>Need More Help?</h3>
                                <p class="lead">Contact our support team 24/7</p>
                                <a href="mailto:support@socialmarket.com" class="btn btn-primary btn-lg">
                                    <i class="fas fa-envelope me-2"></i>Contact Support
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Get help with buying and selling social media accounts on SocialMarket'
            },
            {
                'title': 'Contact Us',
                'slug': 'contact-us',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Contact Us</h1>
                            
                            <div class="row">
                                <div class="col-md-4 mb-4">
                                    <div class="text-center">
                                        <div class="bg-primary text-white rounded-circle mx-auto mb-3" style="width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                                            <i class="fas fa-envelope fa-2x"></i>
                                        </div>
                                        <h4>Email Support</h4>
                                        <p>support@socialmarket.com</p>
                                        <small class="text-muted">Response within 24 hours</small>
                                    </div>
                                </div>
                                
                                <div class="col-md-4 mb-4">
                                    <div class="text-center">
                                        <div class="bg-success text-white rounded-circle mx-auto mb-3" style="width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                                            <i class="fab fa-whatsapp fa-2x"></i>
                                        </div>
                                        <h4>WhatsApp</h4>
                                        <p>+234 800 123 4567</p>
                                        <small class="text-muted">Available 24/7</small>
                                    </div>
                                </div>
                                
                                <div class="col-md-4 mb-4">
                                    <div class="text-center">
                                        <div class="bg-info text-white rounded-circle mx-auto mb-3" style="width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                                            <i class="fab fa-telegram fa-2x"></i>
                                        </div>
                                        <h4>Telegram</h4>
                                        <p>@SocialMarketSupport</p>
                                        <small class="text-muted">Instant messaging</small>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="card border-0 shadow-sm mt-5">
                                <div class="card-body p-4">
                                    <h3 class="mb-4">Send us a Message</h3>
                                    <form>
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <label class="form-label">Your Name</label>
                                                <input type="text" class="form-control" required>
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label class="form-label">Email Address</label>
                                                <input type="email" class="form-control" required>
                                            </div>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Subject</label>
                                            <input type="text" class="form-control" required>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Message</label>
                                            <textarea class="form-control" rows="5" required></textarea>
                                        </div>
                                        <button type="submit" class="btn btn-primary">
                                            <i class="fas fa-paper-plane me-2"></i>Send Message
                                        </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Contact SocialMarket support team for help with your social media account transactions'
            },
            {
                'title': 'Safety Tips',
                'slug': 'safety-tips',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Safety Tips</h1>
                            
                            <div class="alert alert-warning border-0 shadow-sm mb-4">
                                <h5><i class="fas fa-exclamation-triangle me-2"></i>Important Security Notice</h5>
                                <p class="mb-0">Follow these safety guidelines to ensure secure transactions on our platform.</p>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-body">
                                    <h3 class="text-success"><i class="fas fa-shield-alt me-2"></i>For Buyers</h3>
                                    <ul class="list-unstyled">
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Verify account authenticity</strong> - Check screenshots and engagement metrics</li>
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Use escrow protection</strong> - Always pay through our secure wallet system</li>
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Check seller ratings</strong> - Review seller history and feedback</li>
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Communicate through platform</strong> - Keep all communication within SocialMarket</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-body">
                                    <h3 class="text-primary"><i class="fas fa-store me-2"></i>For Sellers</h3>
                                    <ul class="list-unstyled">
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Provide accurate information</strong> - Be honest about follower counts and engagement</li>
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Upload clear screenshots</strong> - Show account analytics and verification status</li>
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Secure account transfer</strong> - Change passwords after successful sale</li>
                                        <li class="mb-3"><i class="fas fa-check-circle text-success me-2"></i><strong>Respond promptly</strong> - Maintain good communication with buyers</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="alert alert-danger border-0 shadow-sm">
                                <h5><i class="fas fa-ban me-2"></i>Red Flags to Avoid</h5>
                                <ul class="mb-0">
                                    <li>Sellers asking for direct payment outside the platform</li>
                                    <li>Accounts with suspicious engagement patterns</li>
                                    <li>Deals that seem too good to be true</li>
                                    <li>Requests to communicate outside SocialMarket</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Essential safety tips for secure social media account transactions on SocialMarket'
            },
            {
                'title': 'Terms of Service',
                'slug': 'terms-of-service',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Terms of Service</h1>
                            <p class="text-center text-muted mb-5">Last updated: January 2025</p>
                            
                            <h3>1. Acceptance of Terms</h3>
                            <p>By accessing and using SocialMarket, you accept and agree to be bound by the terms and provision of this agreement.</p>
                            
                            <h3>2. Account Registration</h3>
                            <ul>
                                <li>You must provide accurate and complete information</li>
                                <li>You are responsible for maintaining account security</li>
                                <li>One account per person is allowed</li>
                                <li>You must be at least 18 years old to use our service</li>
                            </ul>
                            
                            <h3>3. Platform Usage</h3>
                            <ul>
                                <li>Use the platform only for legitimate social media account transactions</li>
                                <li>Do not engage in fraudulent or illegal activities</li>
                                <li>Respect intellectual property rights</li>
                                <li>Follow community guidelines and be respectful to other users</li>
                            </ul>
                            
                            <h3>4. Transaction Terms</h3>
                            <ul>
                                <li>All transactions are subject to our commission fees</li>
                                <li>Payments are processed securely through our wallet system</li>
                                <li>Refunds are handled according to our refund policy</li>
                                <li>Disputes will be mediated by our support team</li>
                            </ul>
                            
                            <h3>5. Account Listings</h3>
                            <ul>
                                <li>Sellers must provide accurate account information</li>
                                <li>All accounts must comply with platform policies</li>
                                <li>We reserve the right to remove listings that violate our terms</li>
                                <li>Sellers are responsible for account authenticity</li>
                            </ul>
                            
                            <h3>6. Limitation of Liability</h3>
                            <p>SocialMarket shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of the platform.</p>
                            
                            <h3>7. Termination</h3>
                            <p>We reserve the right to terminate or suspend accounts that violate these terms of service.</p>
                            
                            <h3>8. Changes to Terms</h3>
                            <p>We reserve the right to modify these terms at any time. Users will be notified of significant changes.</p>
                            
                            <div class="alert alert-info border-0 shadow-sm mt-4">
                                <p class="mb-0"><strong>Questions?</strong> Contact our support team at support@socialmarket.com</p>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Terms of service for SocialMarket - social media account marketplace'
            },
            {
                'title': 'Privacy Policy',
                'slug': 'privacy-policy',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Privacy Policy</h1>
                            <p class="text-center text-muted mb-5">Last updated: January 2025</p>
                            
                            <h3>1. Information We Collect</h3>
                            <h5>Personal Information</h5>
                            <ul>
                                <li>Email address and username</li>
                                <li>Profile information you provide</li>
                                <li>Transaction history and payment information</li>
                                <li>Communication records with support</li>
                            </ul>
                            
                            <h5>Automatically Collected Information</h5>
                            <ul>
                                <li>IP address and device information</li>
                                <li>Browser type and operating system</li>
                                <li>Usage patterns and interaction data</li>
                                <li>Cookies and similar tracking technologies</li>
                            </ul>
                            
                            <h3>2. How We Use Your Information</h3>
                            <ul>
                                <li>To provide and maintain our marketplace service</li>
                                <li>To process transactions and payments</li>
                                <li>To communicate with you about your account</li>
                                <li>To improve our platform and user experience</li>
                                <li>To prevent fraud and ensure security</li>
                                <li>To comply with legal obligations</li>
                            </ul>
                            
                            <h3>3. Information Sharing</h3>
                            <p>We do not sell, trade, or rent your personal information to third parties. We may share information in the following circumstances:</p>
                            <ul>
                                <li>With your explicit consent</li>
                                <li>To comply with legal requirements</li>
                                <li>To protect our rights and prevent fraud</li>
                                <li>With trusted service providers under strict confidentiality</li>
                            </ul>
                            
                            <h3>4. Data Security</h3>
                            <p>We implement appropriate technical and organizational measures to protect your personal information, including:</p>
                            <ul>
                                <li>Encryption of sensitive data</li>
                                <li>Secure payment processing</li>
                                <li>Regular security audits</li>
                                <li>Limited access to personal information</li>
                            </ul>
                            
                            <h3>5. Your Rights</h3>
                            <ul>
                                <li>Access your personal information</li>
                                <li>Correct inaccurate information</li>
                                <li>Request deletion of your data</li>
                                <li>Object to certain processing activities</li>
                                <li>Data portability rights</li>
                            </ul>
                            
                            <h3>6. Cookies</h3>
                            <p>We use cookies to enhance your experience, analyze usage, and provide personalized content. You can control cookie settings through your browser.</p>
                            
                            <h3>7. Changes to This Policy</h3>
                            <p>We may update this privacy policy from time to time. We will notify you of any material changes by posting the new policy on our platform.</p>
                            
                            <div class="alert alert-info border-0 shadow-sm mt-4">
                                <p class="mb-0"><strong>Contact Us:</strong> For privacy-related questions, email us at privacy@socialmarket.com</p>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Privacy policy for SocialMarket - how we collect, use, and protect your personal information'
            },
            {
                'title': 'Refund Policy',
                'slug': 'refund-policy',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Refund Policy</h1>
                            <p class="text-center text-muted mb-5">Last updated: January 2025</p>
                            
                            <div class="alert alert-info border-0 shadow-sm mb-4">
                                <h5><i class="fas fa-info-circle me-2"></i>Our Commitment</h5>
                                <p class="mb-0">We strive to ensure all transactions are secure and satisfactory. This policy outlines when refunds are available.</p>
                            </div>
                            
                            <h3>1. Refund Eligibility</h3>
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-body">
                                    <h5 class="text-success">Full Refund Available:</h5>
                                    <ul>
                                        <li>Account credentials don't work or are incorrect</li>
                                        <li>Account information was misrepresented by seller</li>
                                        <li>Account is suspended/banned before transfer</li>
                                        <li>Seller fails to deliver account within 48 hours</li>
                                        <li>Account violates platform policies</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-body">
                                    <h5 class="text-warning">Partial Refund Available:</h5>
                                    <ul>
                                        <li>Minor discrepancies in follower count (within 10%)</li>
                                        <li>Account performance below expectations</li>
                                        <li>Missing non-essential features mentioned in listing</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-body">
                                    <h5 class="text-danger">No Refund Available:</h5>
                                    <ul>
                                        <li>Account delivered as described and working</li>
                                        <li>Buyer changes mind after successful transfer</li>
                                        <li>Account suspended due to buyer's actions</li>
                                        <li>Request made after 7 days from purchase</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <h3>2. Refund Process</h3>
                            <ol>
                                <li><strong>Submit Request:</strong> Contact support within 7 days of purchase</li>
                                <li><strong>Provide Evidence:</strong> Include screenshots and detailed explanation</li>
                                <li><strong>Investigation:</strong> Our team will review the case within 48 hours</li>
                                <li><strong>Decision:</strong> You'll receive a decision via email</li>
                                <li><strong>Processing:</strong> Approved refunds processed within 3-5 business days</li>
                            </ol>
                            
                            <h3>3. Refund Methods</h3>
                            <ul>
                                <li><strong>Wallet Credit:</strong> Instant credit to your SocialMarket wallet</li>
                                <li><strong>Bank Transfer:</strong> 3-5 business days to your registered account</li>
                                <li><strong>Original Payment Method:</strong> Same method used for purchase</li>
                            </ul>
                            
                            <h3>4. Dispute Resolution</h3>
                            <p>If you're unsatisfied with our refund decision, you can:</p>
                            <ul>
                                <li>Request escalation to senior support team</li>
                                <li>Provide additional evidence for reconsideration</li>
                                <li>Use our mediation service for complex disputes</li>
                            </ul>
                            
                            <div class="alert alert-success border-0 shadow-sm mt-4">
                                <h5><i class="fas fa-headset me-2"></i>Need Help?</h5>
                                <p class="mb-0">Contact our refund team at refunds@socialmarket.com or through live chat for immediate assistance.</p>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'SocialMarket refund policy - when and how to get refunds for social media account purchases'
            },
            {
                'title': 'Cookie Policy',
                'slug': 'cookie-policy',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Cookie Policy</h1>
                            <p class="text-center text-muted mb-5">Last updated: January 2025</p>
                            
                            <h3>What are Cookies?</h3>
                            <p>Cookies are small text files stored on your device when you visit our website. They help us provide you with a better experience by remembering your preferences and understanding how you use our platform.</p>
                            
                            <h3>Types of Cookies We Use</h3>
                            
                            <div class="card border-0 shadow-sm mb-3">
                                <div class="card-body">
                                    <h5 class="text-primary">Essential Cookies</h5>
                                    <p>These cookies are necessary for the website to function properly. They cannot be disabled.</p>
                                    <ul>
                                        <li>Authentication and session management</li>
                                        <li>Security features</li>
                                        <li>Form submission and data validation</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-3">
                                <div class="card-body">
                                    <h5 class="text-success">Functional Cookies</h5>
                                    <p>These cookies enhance functionality and personalization.</p>
                                    <ul>
                                        <li>Language preferences</li>
                                        <li>User interface settings</li>
                                        <li>Shopping cart contents</li>
                                        <li>Recently viewed accounts</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-3">
                                <div class="card-body">
                                    <h5 class="text-info">Analytics Cookies</h5>
                                    <p>These cookies help us understand how visitors interact with our website.</p>
                                    <ul>
                                        <li>Page views and user behavior</li>
                                        <li>Traffic sources and patterns</li>
                                        <li>Feature usage statistics</li>
                                        <li>Performance monitoring</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-body">
                                    <h5 class="text-warning">Marketing Cookies</h5>
                                    <p>These cookies are used to deliver relevant advertisements.</p>
                                    <ul>
                                        <li>Personalized content recommendations</li>
                                        <li>Social media integration</li>
                                        <li>Advertising effectiveness measurement</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <h3>Managing Your Cookies</h3>
                            <p>You can control cookies through:</p>
                            <ul>
                                <li><strong>Browser Settings:</strong> Most browsers allow you to refuse cookies or delete existing ones</li>
                                <li><strong>Cookie Preferences:</strong> Use our cookie preference center (coming soon)</li>
                                <li><strong>Opt-out Tools:</strong> Third-party opt-out tools for marketing cookies</li>
                            </ul>
                            
                            <h3>Third-Party Cookies</h3>
                            <p>Some cookies are set by third-party services we use:</p>
                            <ul>
                                <li>Google Analytics for website analytics</li>
                                <li>Payment processors for transaction security</li>
                                <li>Social media platforms for sharing features</li>
                            </ul>
                            
                            <div class="alert alert-warning border-0 shadow-sm">
                                <h5><i class="fas fa-exclamation-triangle me-2"></i>Important Note</h5>
                                <p class="mb-0">Disabling certain cookies may affect website functionality and your user experience.</p>
                            </div>
                            
                            <div class="alert alert-info border-0 shadow-sm mt-4">
                                <h5><i class="fas fa-envelope me-2"></i>Questions About Cookies?</h5>
                                <p class="mb-0">Contact us at privacy@socialmarket.com for more information about our cookie practices.</p>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'SocialMarket cookie policy - how we use cookies and how you can manage them'
            },
            {
                'title': 'How It Works',
                'slug': 'how-it-works',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-10 mx-auto">
                            <h1 class="display-4 text-center mb-5">How SocialMarket Works</h1>
                            <p class="lead text-center text-muted mb-5">Your trusted marketplace for buying and selling social media accounts safely and securely</p>
                            
                            <div class="row mb-5">
                                <div class="col-md-4 text-center mb-4">
                                    <div class="bg-primary text-white rounded-circle mx-auto mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                                        <i class="fas fa-user-plus fa-2x"></i>
                                    </div>
                                    <h4>1. Create Account</h4>
                                    <p>Sign up for free and verify your identity to start buying or selling social media accounts securely.</p>
                                </div>
                                <div class="col-md-4 text-center mb-4">
                                    <div class="bg-success text-white rounded-circle mx-auto mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                                        <i class="fas fa-search fa-2x"></i>
                                    </div>
                                    <h4>2. Browse & Purchase</h4>
                                    <p>Find the perfect account for your needs and make secure payments with escrow protection.</p>
                                </div>
                                <div class="col-md-4 text-center mb-4">
                                    <div class="bg-info text-white rounded-circle mx-auto mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                                        <i class="fas fa-handshake fa-2x"></i>
                                    </div>
                                    <h4>3. Secure Transfer</h4>
                                    <p>Receive account credentials safely after verification and payment confirmation.</p>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-4">
                                    <div class="card border-0 shadow-sm h-100">
                                        <div class="card-body">
                                            <h3 class="text-primary"><i class="fas fa-shopping-cart me-2"></i>For Buyers</h3>
                                            <ul class="list-unstyled">
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Browse verified social media accounts</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Filter by platform, followers, and price</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>View detailed analytics and screenshots</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Make secure payments with escrow protection</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Get instant access after verification</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-md-6 mb-4">
                                    <div class="card border-0 shadow-sm h-100">
                                        <div class="card-body">
                                            <h3 class="text-success"><i class="fas fa-store me-2"></i>For Sellers</h3>
                                            <ul class="list-unstyled">
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>List your social media accounts for free</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Set your own competitive prices</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Upload screenshots and analytics proof</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Get paid securely after successful transfers</li>
                                                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Build your seller reputation and ratings</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="bg-light rounded p-4 mt-5">
                                <h3 class="text-center mb-4">Why Choose SocialMarket?</h3>
                                <div class="row">
                                    <div class="col-md-3 text-center mb-3">
                                        <i class="fas fa-shield-alt fa-3x text-primary mb-2"></i>
                                        <h6>Secure Escrow</h6>
                                        <small>Protected payments</small>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <i class="fas fa-check-circle fa-3x text-success mb-2"></i>
                                        <h6>Verified Accounts</h6>
                                        <small>Authentic listings only</small>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <i class="fas fa-headset fa-3x text-info mb-2"></i>
                                        <h6>24/7 Support</h6>
                                        <small>Always here to help</small>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <i class="fas fa-bolt fa-3x text-warning mb-2"></i>
                                        <h6>Fast Transfers</h6>
                                        <small>Quick account delivery</small>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="text-center mt-5">
                                <a href="/register" class="btn btn-primary btn-lg me-3">
                                    <i class="fas fa-user-plus me-2"></i>Get Started Today
                                </a>
                                <a href="/browse" class="btn btn-outline-primary btn-lg">
                                    <i class="fas fa-search me-2"></i>Browse Accounts
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'Learn how SocialMarket works - secure marketplace for buying and selling social media accounts'
            },
            {
                'title': 'Pricing & Fees',
                'slug': 'pricing',
                'content': '''
                <div class="container py-5">
                    <div class="row">
                        <div class="col-lg-8 mx-auto">
                            <h1 class="display-4 text-center mb-5">Pricing & Fees</h1>
                            <p class="lead text-center text-muted mb-5">Transparent pricing with no hidden fees</p>
                            
                            <div class="card border-0 shadow-lg mb-4">
                                <div class="card-body p-4">
                                    <h3 class="text-center text-primary mb-4">Commission Structure</h3>
                                    
                                    <div class="row">
                                        <div class="col-md-6 text-center mb-3">
                                            <div class="bg-light rounded p-3">
                                                <h4 class="text-success">5%</h4>
                                                <p class="mb-0">Commission on all sales</p>
                                                <small class="text-muted">Deducted from seller earnings</small>
                                            </div>
                                        </div>
                                        <div class="col-md-6 text-center mb-3">
                                            <div class="bg-light rounded p-3">
                                                <h4 class="text-info">FREE</h4>
                                                <p class="mb-0">Account registration</p>
                                                <small class="text-muted">No setup or monthly fees</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <h3>For Sellers</h3>
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <tbody>
                                        <tr>
                                            <td>Listing accounts</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                        <tr>
                                            <td>Account verification</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                        <tr>
                                            <td>Commission per sale</td>
                                            <td class="text-primary fw-bold">5%</td>
                                        </tr>
                                        <tr>
                                            <td>Withdrawal to bank</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            
                            <h3>For Buyers</h3>
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <tbody>
                                        <tr>
                                            <td>Account registration</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                        <tr>
                                            <td>Browsing accounts</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                        <tr>
                                            <td>Wallet deposits</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                        <tr>
                                            <td>Purchase fees</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                        <tr>
                                            <td>Escrow protection</td>
                                            <td class="text-success fw-bold">FREE</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-body">
                                    <h4>Payment Methods</h4>
                                    <div class="row">
                                        <div class="col-md-6">
                                            <h6>For Deposits:</h6>
                                            <ul class="list-unstyled">
                                                <li><i class="fas fa-university text-primary me-2"></i>Bank Transfer (Nigerian banks)</li>
                                                <li><i class="fas fa-credit-card text-success me-2"></i>Debit/Credit Cards</li>
                                                <li><i class="fas fa-mobile-alt text-info me-2"></i>USSD Banking</li>
                                            </ul>
                                        </div>
                                        <div class="col-md-6">
                                            <h6>For Withdrawals:</h6>
                                            <ul class="list-unstyled">
                                                <li><i class="fas fa-university text-primary me-2"></i>Bank Transfer</li>
                                                <li><i class="fas fa-wallet text-warning me-2"></i>Wallet Balance</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="alert alert-info border-0 shadow-sm">
                                <h5><i class="fas fa-calculator me-2"></i>Quick Price Calculator</h5>
                                <div class="row">
                                    <div class="col-md-6">
                                        <label class="form-label">Account Price (₦)</label>
                                        <input type="number" class="form-control" id="accountPrice" placeholder="10000" onchange="calculateFees()">
                                    </div>
                                    <div class="col-md-6 mt-2">
                                        <label class="form-label">Results:</label>
                                        <p class="mb-1">Commission (5%): <span id="commission">₦0.00</span></p>
                                        <p class="mb-0 fw-bold">Seller Receives: <span id="sellerReceives">₦0.00</span></p>
                                    </div>
                                </div>
                                <script>
                                function calculateFees() {
                                    const price = parseFloat(document.getElementById('accountPrice').value) || 0;
                                    const commission = price * 0.05;
                                    const sellerReceives = price - commission;
                                    
                                    document.getElementById('commission').textContent = '₦' + commission.toFixed(2);
                                    document.getElementById('sellerReceives').textContent = '₦' + sellerReceives.toFixed(2);
                                }
                                </script>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'meta_description': 'SocialMarket pricing and fees for buying and selling social media accounts'
            }
        ]
        
        # Create pages
        created_count = 0
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
                    updated_by=admin_id
                )
                db.session.add(page)
                created_count += 1
                print(f"Created page: {page_data['title']}")
            else:
                print(f"Page already exists: {page_data['title']}")
        
        # Update settings with footer URLs
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
        
        # Set footer link URLs
        settings.help_center_url = '/help-center'
        settings.contact_us_url = '/contact-us'
        settings.safety_tips_url = '/safety-tips'
        settings.terms_of_service_url = '/terms-of-service'
        settings.privacy_policy_url = '/privacy-policy'
        settings.refund_policy_url = '/refund-policy'
        settings.cookie_policy_url = '/cookie-policy'
        settings.how_it_works_url = '/how-it-works'
        settings.pricing_url = '/pricing'
        
        # Set some demo social media URLs
        settings.facebook_url = 'https://facebook.com/socialmarket'
        settings.twitter_url = 'https://twitter.com/socialmarket'
        settings.instagram_url = 'https://instagram.com/socialmarket'
        settings.telegram_url = 'https://t.me/socialmarket'
        settings.whatsapp_url = 'https://wa.me/2348001234567'
        
        settings.updated_at = datetime.utcnow()
        
        db.session.commit()
        print(f"Created {created_count} new pages and updated settings!")
        print("Footer links are now properly connected!")

if __name__ == '__main__':
    create_demo_footer_pages()
