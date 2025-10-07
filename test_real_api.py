#!/usr/bin/env python3
"""
Real API Test: Test actual OpenAI API connection and analysis

This script will use your real API key to analyze the sample data
and show you the difference between mock and real analysis.
"""

import os
import sys
from dotenv import load_dotenv

def check_api_key_setup():
    """Check if API key is properly configured"""
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    print("🔑 API KEY SETUP CHECK")
    print("=" * 40)
    
    if not api_key:
        print("❌ No OPENAI_API_KEY found in environment")
        return False
    elif api_key == "your_openai_api_key_here":
        print("❌ API key is still the placeholder")
        print("📝 You need to:")
        print("   1. Get API key from: https://platform.openai.com/api-keys")
        print("   2. Edit .env file: nano .env")
        print("   3. Replace placeholder with your real key")
        return False
    elif api_key.startswith("sk-"):
        print("✅ API key format looks correct")
        print(f"📍 Key starts with: {api_key[:15]}...")
        return True
    else:
        print("⚠️  API key format doesn't look right")
        print("💡 OpenAI keys should start with 'sk-'")
        return False

def test_real_api_connection():
    """Test actual connection to OpenAI API"""
    try:
        from openai import OpenAI
        
        print("\n🧪 TESTING REAL API CONNECTION")
        print("=" * 40)
        
        client = OpenAI()
        
        # Simple test call
        print("📡 Making test API call...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Say 'API connection successful!' and nothing else."}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        if "authentication" in str(e).lower() or "api key" in str(e).lower():
            print("💡 This looks like an API key issue")
            print("   • Double-check your API key in .env")
            print("   • Make sure you have billing set up at OpenAI")
        return False

def run_real_analysis_test():
    """Run real analysis on sample data"""
    print("\n🎯 RUNNING REAL UX ANALYSIS")
    print("=" * 40)
    
    try:
        # Import and run the enhanced main function
        import subprocess
        result = subprocess.run([
            '/Users/stevenvillarino/Projects/stevenvillarino/agent-uxr/.venv/bin/python',
            'main_enhanced.py',
            'sample_data/user_interview_dashboard.txt',
            '--verbose'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Real analysis completed successfully!")
            print("\n📊 Output preview:")
            print(result.stdout[-500:])  # Last 500 chars
        else:
            print("❌ Analysis failed:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Analysis timed out (>60s)")
    except Exception as e:
        print(f"❌ Error running analysis: {e}")

def show_setup_instructions():
    """Show step-by-step setup instructions"""
    print("\n🚀 TO GET REAL DATA FLOW WORKING:")
    print("=" * 50)
    
    instructions = [
        "1. 🌐 Go to: https://platform.openai.com/api-keys",
        "2. 🔐 Create account or log in",
        "3. 💳 Add billing method (required for API access)",
        "4. 🔑 Generate new API key",
        "5. 📝 Copy the key (starts with 'sk-')",
        "6. ✏️  Edit .env file: nano .env",
        "7. 🔄 Replace 'your_openai_api_key_here' with real key",
        "8. 💾 Save file",
        "9. 🧪 Run this test again: python test_real_api.py"
    ]
    
    for instruction in instructions:
        print(f"   {instruction}")
    
    print(f"\n💰 Expected costs:")
    print(f"   • API setup: Free")
    print(f"   • Per analysis: $0.02-0.15")
    print(f"   • Monthly minimum: $5 (OpenAI requirement)")

if __name__ == "__main__":
    print("🔥 REAL API TESTING SCRIPT")
    print("=" * 50)
    print("This will test your actual OpenAI API connection")
    print("and run real analysis (not mock data)")
    print()
    
    # Step 1: Check API key
    if not check_api_key_setup():
        show_setup_instructions()
        sys.exit(1)
    
    # Step 2: Test connection
    if not test_real_api_connection():
        show_setup_instructions()
        sys.exit(1)
    
    # Step 3: Run real analysis
    run_real_analysis_test()
    
    print("\n🎉 REAL API TESTING COMPLETE!")
    print("🚀 You now have real data flow working!")
    print("💡 Try: python main_enhanced.py sample_data/user_interview_dashboard.txt")