#!/usr/bin/env python3
"""
Quick setup verification script
Tests that all dependencies and API keys are configured correctly
"""

import os
import sys

def test_imports():
    """Test that required packages can be imported"""
    print("🔍 Testing imports...")
    
    tests = {
        "Flask": "flask",
        "OpenAI": "openai",
        "Python-dotenv": "dotenv",
        "Requests": "requests",
    }
    
    optional_tests = {
        "LangGraph": "langgraph.graph",
        "LangChain": "langchain",
        "Anthropic": "anthropic",
    }
    
    failed = []
    
    # Test required imports
    for name, module in tests.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - REQUIRED")
            failed.append(name)
    
    # Test optional imports (for multi-agent system)
    print("\n🔍 Testing optional imports (for multi-agent)...")
    for name, module in optional_tests.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ⚠️  {name} - Optional (run: pip install -r requirements-langgraph.txt)")
    
    return len(failed) == 0

def test_env_keys():
    """Test that API keys are configured"""
    print("\n🔑 Testing API keys...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = {
        "OPENAI_API_KEY": "OpenAI",
        "ELEVENLABS_API_KEY": "ElevenLabs",
    }
    
    optional_keys = {
        "ANTHROPIC_API_KEY": "Anthropic (for multi-agent)",
    }
    
    missing = []
    
    # Check required keys
    for key, name in required_keys.items():
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}":
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - REQUIRED")
            missing.append(name)
    
    # Check optional keys
    for key, name in optional_keys.items():
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}":
            print(f"  ✅ {name}")
        else:
            print(f"  ⚠️  {name} - Recommended")
    
    return len(missing) == 0

def main():
    print("="*60)
    print("🚀 InsightDeck Agent - Setup Verification")
    print("="*60)
    print()
    
    imports_ok = test_imports()
    env_ok = test_env_keys()
    
    print()
    print("="*60)
    
    if imports_ok and env_ok:
        print("✅ ALL CHECKS PASSED - Ready for basic features!")
        print()
        print("Next steps:")
        print("  1. Add your ElevenLabs API key to .env")
        print("  2. Run: python web_app.py")
        print("  3. Open: http://localhost:5000")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("For basic features:")
        print("  - Install: pip install -r requirements.txt")
        print("  - Configure API keys in .env file")
        print()
        print("For multi-agent features:")
        print("  - Install: pip install -r requirements-langgraph.txt")
        print("  - Add ANTHROPIC_API_KEY to .env file")
        return 1

if __name__ == "__main__":
    sys.exit(main())
