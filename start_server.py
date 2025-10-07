#!/usr/bin/env python3
"""
Simple Web Server Starter
"""
from web_app import app

if __name__ == '__main__':
    print("🚀 Starting Agent-UXR Web Interface...")
    print("🌐 URL: http://127.0.0.1:8080")
    print("📝 Ready for audio file uploads!")
    print("=" * 50)
    
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=True,
        use_reloader=False  # Disable reloader to avoid issues
    )