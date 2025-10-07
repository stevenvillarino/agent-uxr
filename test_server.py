#!/usr/bin/env python3
"""
Simple test web server to verify port 8080 works
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return """
    <html>
    <head><title>Test Server</title></head>
    <body>
        <h1>🎉 Port 8080 Test Server Working!</h1>
        <p>This confirms the port is accessible.</p>
        <p>If you can see this, the web server setup is working.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🧪 Starting test server on port 8080...")
    print("🌐 Open http://127.0.0.1:8080 to test")
    app.run(debug=True, host='127.0.0.1', port=8080)