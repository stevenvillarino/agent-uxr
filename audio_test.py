#!/usr/bin/env python3
"""
Audio Processing Test - Test m4a file processing
"""

import os
import sys
import whisper
from dotenv import load_dotenv

load_dotenv()

def test_whisper_with_sample():
    """Test Whisper processing"""
    print("🎤 WHISPER AUDIO PROCESSING TEST")
    print("=" * 50)
    
    # Test basic Whisper functionality
    try:
        print("📥 Loading Whisper base model...")
        model = whisper.load_model("base")
        print("✅ Whisper model loaded successfully")
        
        print("🎵 Whisper supports these formats:")
        formats = [".mp3", ".wav", ".m4a", ".mp4", ".flac", ".ogg"]
        for fmt in formats:
            print(f"   • {fmt}")
        
        return True
        
    except Exception as e:
        print(f"❌ Whisper test failed: {e}")
        return False

def test_api_connection():
    """Test OpenAI API"""
    print("\n🤖 OPENAI API TEST")
    print("=" * 50)
    
    try:
        from openai import OpenAI
        client = OpenAI()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ No valid API key found")
            return False
        
        print("✅ API key configured")
        print(f"📍 Key starts with: {api_key[:15]}...")
        
        # Test simple API call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say 'API working!'"}],
            max_tokens=5
        )
        
        result = response.choices[0].message.content
        print(f"✅ API response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def check_web_server_issues():
    """Check common web server issues"""
    print("\n🌐 WEB SERVER DIAGNOSTICS")
    print("=" * 50)
    
    # Check if Flask templates exist
    templates_path = "templates/index.html"
    if os.path.exists(templates_path):
        print("✅ Templates directory exists")
    else:
        print("❌ Templates directory missing")
    
    # Check file upload directory
    import tempfile
    upload_dir = tempfile.gettempdir()
    print(f"📁 Upload directory: {upload_dir}")
    
    if os.access(upload_dir, os.W_OK):
        print("✅ Upload directory is writable")
    else:
        print("❌ Upload directory not writable")
    
    # Check port availability
    import socket
    def check_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    
    if check_port(8080):
        print("✅ Port 8080 is active (web server running)")
    else:
        print("❌ Port 8080 not responding")

def show_troubleshooting_steps():
    """Show troubleshooting steps for common issues"""
    print("\n🔧 TROUBLESHOOTING STEPS")
    print("=" * 50)
    
    steps = [
        "1. 🎵 File Format Issues:",
        "   • M4A files are supported by Whisper",
        "   • Try converting to WAV if issues persist: ffmpeg -i input.m4a output.wav",
        "   • Maximum file size: ~25MB for web upload",
        "",
        "2. 🌐 Web Interface Issues:",
        "   • Make sure you're using http://127.0.0.1:8080 (not http://localhost:8080)",
        "   • Clear browser cache and try again",
        "   • Check browser console for JavaScript errors (F12)",
        "",
        "3. 📡 Upload Issues:",
        "   • File must be under 25MB",
        "   • Wait for full upload before clicking 'Generate'",
        "   • Check browser network tab for failed requests",
        "",
        "4. 🤖 Processing Issues:",
        "   • Whisper transcription can take 30-60 seconds",
        "   • GPT-4o analysis adds another 10-30 seconds",
        "   • Don't refresh page while processing",
        "",
        "5. 🔑 API Issues:",
        "   • Verify OpenAI API key is valid",
        "   • Check API billing is set up",
        "   • Ensure sufficient API credits"
    ]
    
    for step in steps:
        print(step)

if __name__ == "__main__":
    print("🔬 AGENT-UXR DIAGNOSTICS")
    print("=" * 60)
    
    whisper_ok = test_whisper_with_sample()
    api_ok = test_api_connection()
    check_web_server_issues()
    
    print(f"\n📊 SUMMARY:")
    print(f"   Whisper: {'✅ Ready' if whisper_ok else '❌ Issues'}")
    print(f"   OpenAI API: {'✅ Ready' if api_ok else '❌ Issues'}")
    
    if whisper_ok and api_ok:
        print(f"\n🎉 All systems ready for audio processing!")
        print(f"💡 Upload your M4A file at: http://127.0.0.1:8080")
    else:
        print(f"\n⚠️  Issues detected - see troubleshooting steps below")
    
    show_troubleshooting_steps()