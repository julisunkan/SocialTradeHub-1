#!/usr/bin/env python3
"""
Social Media Marketplace Platform Startup Script
"""
import subprocess
import sys
import os

def main():
    """Start the Flask application"""
    print("🚀 Starting Social Media Marketplace Platform...")
    print("📊 Database: SQLite (social_marketplace.db)")
    print("💰 Currency: Nigerian Naira (NGN)")
    print("🌐 Server: http://localhost:5000")
    print("-" * 50)
    
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    # Run the Flask application
    try:
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()