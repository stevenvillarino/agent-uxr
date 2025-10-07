#!/usr/bin/env python3
"""
Stable Web Server - No Auto-Reload
"""
import os
os.environ['FLASK_DEBUG'] = '0'  # Disable debug mode to prevent auto-restart

from web_app import app

if __name__ == '__main__':
    print("🚀 Starting STABLE Agent-UXR Web Interface...")
    print("🌐 URL: http://127.0.0.1:8080")
    print("✅ Auto-reload DISABLED - server won't restart!")
    print("📝 Ready for chunk uploads!")
    print("=" * 50)
    
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=False,        # No debug mode
        use_reloader=False  # No auto-reload
    )