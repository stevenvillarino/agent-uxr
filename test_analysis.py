#!/usr/bin/env python3
"""
Test script to verify the analysis functionality works with pasted text.
This simulates what happens when a user pastes text into the web interface.
"""

import os
import sys
from dotenv import load_dotenv
from main import get_insights_from_llm

# Load environment variables
load_dotenv()

# Sample test content
TEST_CONTENT = """
User: I'm really frustrated with the loading times on the new dashboard. It takes forever to load.

Interviewer: Can you tell me more about what you're experiencing?

User: Well, when I first open the dashboard, I have to wait at least 30 seconds before I can see any data. And when I try to filter the results, it freezes for a few seconds.

Interviewer: That sounds frustrating. Are there any aspects of the dashboard that you do like?

User: Actually, yes. Once it loads, the layout is much cleaner than before. The navigation is more intuitive, and I love the new search functionality. The filters work really well once they load.

Interviewer: What about the data visualization?

User: The charts and graphs are excellent. Much easier to understand than the previous version. I just wish the performance was better.
"""

def main():
    print("=" * 80)
    print("Testing Text Analysis with OpenAI")
    print("=" * 80)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("\n❌ ERROR: OPENAI_API_KEY not set in .env file")
        print("\nPlease:")
        print("1. Copy .env.template to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Run this script again")
        sys.exit(1)
    
    print("\n✓ OpenAI API key found")
    print(f"\nTest Content ({len(TEST_CONTENT)} characters):")
    print("-" * 80)
    print(TEST_CONTENT[:200] + "..." if len(TEST_CONTENT) > 200 else TEST_CONTENT)
    print("-" * 80)
    
    print("\n🔄 Analyzing content with OpenAI...")
    
    try:
        insights = get_insights_from_llm(TEST_CONTENT)
        
        if insights:
            print("\n✅ Analysis successful!\n")
            print("=" * 80)
            print("EXECUTIVE SUMMARY")
            print("=" * 80)
            print(insights.get('summary', 'No summary available'))
            
            print("\n" + "=" * 80)
            print("KEY THEMES")
            print("=" * 80)
            themes = insights.get('themes', [])
            if themes:
                for i, theme in enumerate(themes, 1):
                    print(f"{i}. {theme}")
            else:
                print("No themes identified")
            
            print("\n" + "=" * 80)
            print("✅ Test completed successfully!")
            print("=" * 80)
            print("\nThe analysis is working correctly. Your web app should now")
            print("properly analyze pasted text instead of showing mock results.")
        else:
            print("\n❌ ERROR: Failed to get insights from OpenAI")
            print("Please check your API key and try again.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nPlease check:")
        print("1. Your OpenAI API key is valid")
        print("2. You have sufficient API credits")
        print("3. Your network connection is working")
        sys.exit(1)

if __name__ == "__main__":
    main()
