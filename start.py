#!/usr/bin/env python3
"""
Simple startup script for MentWel platform
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the MentWel platform"""
    try:
        print("🚀 Starting MentWel Platform...")
        
        # Import and create app
        from app import create_app
        app = create_app('development')
        
        print("✅ Flask app created successfully")
        print("🌐 Starting development server...")
        print("📱 Open http://localhost:5000 in your browser")
        print("⏹️  Press Ctrl+C to stop the server")
        
        # Start the app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        return False

if __name__ == "__main__":
    main()
