#!/usr/bin/env python3
"""
Database migration script to fix schema issues
"""
import os
import sqlite3
from decimal import Decimal

def fix_database():
    """Fix database schema by adding missing columns"""
    db_path = 'instance/social_marketplace.db'

    if not os.path.exists(db_path):
        print("Database file not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Get existing columns for settings table
        cursor.execute("PRAGMA table_info(settings)")
        settings_columns = [column[1] for column in cursor.fetchall()]
        print(f"Existing settings columns: {settings_columns}")

        # Add missing columns to settings table
        settings_missing = []

        # Check each required column
        required_columns = [
            ('site_description', 'TEXT'),
            ('site_logo', 'TEXT'),
            ('commission_rate', 'DECIMAL(5,2)'),
            ('referral_commission', 'DECIMAL(5,2)'),
            ('min_withdrawal', 'DECIMAL(10,2)'),
            ('max_withdrawal', 'DECIMAL(10,2)'),
            ('admin_email', 'TEXT'),
            ('smtp_server', 'TEXT'),
            ('smtp_port', 'INTEGER'),
            ('smtp_username', 'TEXT'),
            ('smtp_password', 'TEXT'),
            ('bank_name', 'TEXT'),
            ('account_number', 'TEXT'),
            ('account_name', 'TEXT'),
            ('bank_name_2', 'TEXT'),
            ('account_number_2', 'TEXT'),
            ('account_name_2', 'TEXT'),
            ('payment_instructions', 'TEXT'),
            ('facebook_url', 'TEXT'),
            ('twitter_url', 'TEXT'),
            ('instagram_url', 'TEXT'),
            ('telegram_url', 'TEXT'),
            ('whatsapp_url', 'TEXT'),
            ('help_center_url', 'TEXT'),
            ('contact_us_url', 'TEXT'),
            ('safety_tips_url', 'TEXT'),
            ('terms_of_service_url', 'TEXT'),
            ('privacy_policy_url', 'TEXT'),
            ('refund_policy_url', 'TEXT'),
            ('cookie_policy_url', 'TEXT'),
            ('how_it_works_url', 'TEXT'),
            ('pricing_url', 'TEXT'),
            ('updated_at', 'DATETIME')
        ]

        for column_name, column_type in required_columns:
            if column_name not in settings_columns:
                settings_missing.append((column_name, column_type))

        # Add missing columns
        for column_name, column_type in settings_missing:
            try:
                cursor.execute(f"ALTER TABLE settings ADD COLUMN {column_name} {column_type}")
                print(f"Added settings column: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e):
                    print(f"Error adding settings column {column_name}: {e}")

        # Check if page table exists, create it if not
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='page'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE page (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    slug VARCHAR(100) UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    meta_description VARCHAR(160),
                    seo_title VARCHAR(200),
                    seo_keywords VARCHAR(500),
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_by INTEGER,
                    FOREIGN KEY (updated_by) REFERENCES user(id)
                )
            ''')
            print("Created page table")

        # Check if invoice table exists, create it if not
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoice'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE invoice (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    purchase_id INTEGER,
                    invoice_number VARCHAR(50) UNIQUE NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(id),
                    FOREIGN KEY (purchase_id) REFERENCES purchase(id)
                )
            ''')
            print("Created invoice table")

        conn.commit()
        print("Database schema updated successfully!")

    except Exception as e:
        print(f"Error fixing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()