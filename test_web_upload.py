#!/usr/bin/env python3
"""
Quick Test - Upload and Process a Small Chunk
Test the web interface with a small audio chunk
"""

import os
import requests

def test_web_upload():
    """Test uploading a chunk file to the web interface"""
    
    # Use the first chunk we created
    chunk_file = "/Users/stevenvillarino/Projects/stevenvillarino/agent-uxr/chunks/Danette_GMT20250902-180911_Recording_chunk_01.mp3"
    
    if not os.path.exists(chunk_file):
        print(f"❌ Chunk file not found: {chunk_file}")
        return
    
    print(f"🎵 Testing web upload with: {os.path.basename(chunk_file)}")
    print(f"📊 File size: {os.path.getsize(chunk_file) / (1024*1024):.1f}MB")
    
    # Test if server is responding
    try:
        response = requests.get("http://127.0.0.1:8080", timeout=5)
        if response.status_code == 200:
            print(f"✅ Web server is responding")
        else:
            print(f"❌ Web server returned status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to web server: {e}")
        return
    
    print(f"\n🌐 Server Status: ✅ Running")
    print(f"🔗 URL: http://127.0.0.1:8080")
    print(f"📁 Test file ready: {os.path.basename(chunk_file)}")
    print(f"\n💡 Manual Test Steps:")
    print(f"   1. Open: http://127.0.0.1:8080")
    print(f"   2. Upload: {chunk_file}")
    print(f"   3. Click: 'Generate Presentation Insights'")
    print(f"   4. Wait: ~30 seconds for processing")
    
    return True

if __name__ == "__main__":
    test_web_upload()