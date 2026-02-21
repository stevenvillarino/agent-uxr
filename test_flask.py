import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return "Flask is working!"

if __name__ == '__main__':
    # Use environment variable for debug mode, defaulting to False for security
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5001, debug=debug_mode)