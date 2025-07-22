
#!/usr/bin/env python3
"""
Database migration script to fix schema issues
"""
import os
import sqlite3
from decimal import Decimal

def fix_database():
    """Fix database schema issues"""
    db_path = 'instance/social_marketplace.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database doesn't exist. Will be created on first run.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if wallet_deposit table exists and get its columns
        cursor.execute("PRAGMA table_info(wallet_deposit)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current wallet_deposit columns: {columns}")
        
        # Add missing columns if they don't exist
        missing_columns = []
        
        if 'deposit_method' not in columns:
            missing_columns.append(('deposit_method', 'TEXT'))
        if 'bank_name' not in columns:
            missing_columns.append(('bank_name', 'TEXT'))
        if 'account_number' not in columns:
            missing_columns.append(('account_number', 'TEXT'))
        if 'account_name' not in columns:
            missing_columns.append(('account_name', 'TEXT'))
        if 'payment_proof' not in columns:
            missing_columns.append(('payment_proof', 'TEXT'))
        if 'reference_number' not in columns:
            missing_columns.append(('reference_number', 'TEXT'))
        if 'admin_notes' not in columns:
            missing_columns.append(('admin_notes', 'TEXT'))
        if 'processed_by' not in columns:
            missing_columns.append(('processed_by', 'INTEGER'))
        if 'processed_at' not in columns:
            missing_columns.append(('processed_at', 'DATETIME'))
        
        # Add missing columns
        for column_name, column_type in missing_columns:
            try:
                cursor.execute(f"ALTER TABLE wallet_deposit ADD COLUMN {column_name} {column_type}")
                print(f"Added column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding column {column_name}: {e}")
        
        # Check settings table
        cursor.execute("PRAGMA table_info(settings)")
        settings_columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current settings columns: {settings_columns}")
        
        # Add missing settings columns
        settings_missing = []
        if 'site_description' not in settings_columns:
            settings_missing.append(('site_description', 'TEXT'))
        if 'site_logo' not in settings_columns:
            settings_missing.append(('site_logo', 'TEXT'))
        if 'currency_symbol' not in settings_columns:
            settings_missing.append(('currency_symbol', 'TEXT'))
        if 'currency_code' not in settings_columns:
            settings_missing.append(('currency_code', 'TEXT'))
        if 'commission_rate' not in settings_columns:
            settings_missing.append(('commission_rate', 'DECIMAL(5,2)'))
        if 'referral_commission' not in settings_columns:
            settings_missing.append(('referral_commission', 'DECIMAL(5,2)'))
        if 'min_withdrawal' not in settings_columns:
            settings_missing.append(('min_withdrawal', 'DECIMAL(10,2)'))
        if 'max_withdrawal' not in settings_columns:
            settings_missing.append(('max_withdrawal', 'DECIMAL(10,2)'))
        if 'admin_email' not in settings_columns:
            settings_missing.append(('admin_email', 'TEXT'))
        if 'smtp_server' not in settings_columns:
            settings_missing.append(('smtp_server', 'TEXT'))
        if 'smtp_port' not in settings_columns:
            settings_missing.append(('smtp_port', 'INTEGER'))
        if 'smtp_username' not in settings_columns:
            settings_missing.append(('smtp_username', 'TEXT'))
        if 'smtp_password' not in settings_columns:
            settings_missing.append(('smtp_password', 'TEXT'))
        if 'bank_name' not in settings_columns:
            settings_missing.append(('bank_name', 'TEXT'))
        if 'account_number' not in settings_columns:
            settings_missing.append(('account_number', 'TEXT'))
        if 'account_name' not in settings_columns:
            settings_missing.append(('account_name', 'TEXT'))
        if 'facebook_url' not in settings_columns:
            settings_missing.append(('facebook_url', 'TEXT'))
        if 'twitter_url' not in settings_columns:
            settings_missing.append(('twitter_url', 'TEXT'))
        if 'instagram_url' not in settings_columns:
            settings_missing.append(('instagram_url', 'TEXT'))
        if 'telegram_url' not in settings_columns:
            settings_missing.append(('telegram_url', 'TEXT'))
        if 'whatsapp_url' not in settings_columns:
            settings_missing.append(('whatsapp_url', 'TEXT'))
        if 'help_center_url' not in settings_columns:
            settings_missing.append(('help_center_url', 'TEXT'))
        if 'contact_us_url' not in settings_columns:
            settings_missing.append(('contact_us_url', 'TEXT'))
        if 'safety_tips_url' not in settings_columns:
            settings_missing.append(('safety_tips_url', 'TEXT'))
        if 'terms_of_service_url' not in settings_columns:
            settings_missing.append(('terms_of_service_url', 'TEXT'))
        if 'privacy_policy_url' not in settings_columns:
            settings_missing.append(('privacy_policy_url', 'TEXT'))
        if 'refund_policy_url' not in settings_columns:
            settings_missing.append(('refund_policy_url', 'TEXT'))
        if 'cookie_policy_url' not in settings_columns:
            settings_missing.append(('cookie_policy_url', 'TEXT'))
        if 'how_it_works_url' not in settings_columns:
            settings_missing.append(('how_it_works_url', 'TEXT'))
        if 'pricing_url' not in settings_columns:
            settings_missing.append(('pricing_url', 'TEXT'))
        if 'updated_at' not in settings_columns:
            settings_missing.append(('updated_at', 'DATETIME'))
        
        for column_name, column_type in settings_missing:
            try:
                cursor.execute(f"ALTER TABLE settings ADD COLUMN {column_name} {column_type}")
                print(f"Added settings column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding settings column {column_name}: {e}")
        
        # Check notification table
        cursor.execute("PRAGMA table_info(notification)")
        notification_columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current notification columns: {notification_columns}")
        
        # Add missing notification columns
        notification_missing = []
        if 'type' not in notification_columns:
            notification_missing.append(('type', 'TEXT'))
        
        for column_name, column_type in notification_missing:
            try:
                cursor.execute(f"ALTER TABLE notification ADD COLUMN {column_name} {column_type}")
                print(f"Added notification column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding notification column {column_name}: {e}")
        
        # Check activity_log table
        cursor.execute("PRAGMA table_info(activity_log)")
        activity_log_columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current activity_log columns: {activity_log_columns}")
        
        # Add missing activity_log columns
        activity_log_missing = []
        if 'ip_address' not in activity_log_columns:
            activity_log_missing.append(('ip_address', 'TEXT'))
        if 'user_agent' not in activity_log_columns:
            activity_log_missing.append(('user_agent', 'TEXT'))
        
        for column_name, column_type in activity_log_missing:
            try:
                cursor.execute(f"ALTER TABLE activity_log ADD COLUMN {column_name} {column_type}")
                print(f"Added activity_log column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding activity_log column {column_name}: {e}")
        
        conn.commit()
        print("Database schema updated successfully!")
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
