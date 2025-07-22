# Social Media Marketplace Platform

## Overview
A progressive web app marketplace for buying and selling social media accounts with comprehensive admin management, referral system, and wallet functionality. Built with Flask/Python backend and modern frontend with Naira (NGN) currency support.

## Project Architecture
- **Backend**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS/JavaScript with PWA capabilities
- **Authentication**: Flask-Login with user roles (user, admin)
- **Currency**: Nigerian Naira (NGN)
- **Payment**: Bank deposit and manual verification system

## Core Features
### User Features
- User registration/login with email verification
- Profile management with KYC verification
- Wallet system with deposit functionality
- Browse and purchase social media accounts
- List accounts for sale with detailed information
- Upload payment proofs and invoices
- Referral system with commission tracking
- Purchase history and transaction logs

### Admin Features
- User management (ban/unban, verify payments)
- Account verification and approval
- Payment verification and release of login details
- Commission and settings management
- SMTP configuration and testing
- Invoice generation and management
- Platform statistics and analytics

### Social Media Platforms Supported
- Instagram, Facebook, Twitter/X, TikTok, YouTube, LinkedIn, Snapchat, Pinterest, Discord, Telegram, WhatsApp Business

## Recent Changes
- 2025-07-22: Initial project setup with Flask backend and SQLite database (switched from PostgreSQL)
- 2025-07-22: Comprehensive database schema design for all features
- 2025-07-22: PWA configuration for mobile app experience
- 2025-07-22: Created complete social media marketplace with user authentication
- 2025-07-22: Built responsive frontend with Bootstrap 5 and custom CSS
- 2025-07-22: Added sample data with 5 social media accounts across different platforms
- 2025-07-22: Flask application successfully running on port 5000
- 2025-07-22: Implemented manual payment system as requested by user
- 2025-07-22: Fixed Flask-SQLAlchemy integration issues by consolidating into single app.py
- 2025-07-22: Created comprehensive demo script showcasing all platform features
- 2025-07-22: Platform fully operational with 4 users, 5 approved accounts, admin panel ready

## User Preferences
- Currency: Nigerian Naira (NGN)
- Focus on attractive, professional interface
- Include advanced features for marketplace functionality
- Progressive Web App (PWA) capabilities required