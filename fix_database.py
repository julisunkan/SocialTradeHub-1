
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
        
        # Add missing settings columns
        settings_missing = []
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
        
        for column_name, column_type in settings_missing:
            try:
                cursor.execute(f"ALTER TABLE settings ADD COLUMN {column_name} {column_type}")
                print(f"Added settings column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding settings column {column_name}: {e}")
        
        conn.commit()
        print("Database schema updated successfully!")
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
