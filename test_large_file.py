#!/usr/bin/env python3
"""
Test Large Audio File Processing
Process the Danette recording with chunking approach
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def test_large_file_processing():
    """Test processing the large Danette file"""
    
    # Import after setting up path
    from web_app import transcribe_with_whisper, get_file_size_mb
    from main import get_insights_from_llm, format_marp_presentation
    
    input_file = "/Users/stevenvillarino/Desktop/Danette_GMT20250902-180911_Recording.m4a"
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    print(f"🎵 Testing large file processing with chunking")
    print(f"📁 File: {input_file}")
    print(f"📊 Size: {get_file_size_mb(input_file):.1f}MB")
    print("=" * 60)
    
    try:
        # Step 1: Transcribe with smart processing
        print(f"🎤 Step 1: Transcribing audio...")
        result = transcribe_with_whisper(input_file)
        
        transcript = result['text']
        print(f"✅ Transcription completed")
        print(f"📝 Service used: {result.get('service', 'Unknown')}")
        print(f"🌍 Language: {result.get('language', 'Unknown')}")
        print(f"📊 Transcript length: {len(transcript)} characters")
        
        if result.get('chunk_info'):
            print(f"📦 Processed in {len(result['chunk_info'])} chunks")
        
        # Step 2: Generate UX insights
        print(f"\n🤖 Step 2: Generating UX insights...")
        insights = get_insights_from_llm(transcript)
        
        if insights:
            print(f"✅ Insights generated successfully")
        else:
            print(f"❌ Failed to generate insights")
            return
        
        # Step 3: Create presentation
        print(f"\n📄 Step 3: Creating presentation...")
        presentation_content = format_marp_presentation(insights, transcript)
        
        # Save results
        timestamp = "chunked_large_file"
        output_file = f"outputs/danette_analysis_{timestamp}.md"
        
        os.makedirs("outputs", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(presentation_content)
        
        print(f"✅ Analysis complete!")
        print(f"📄 Presentation saved: {output_file}")
        print(f"🎉 Your large file has been successfully processed with chunking!")
        
        # Show summary
        print(f"\n📊 PROCESSING SUMMARY:")
        print(f"   Original file: {get_file_size_mb(input_file):.1f}MB")
        print(f"   Transcription: {result.get('service', 'Unknown')}")
        print(f"   Content length: {len(transcript):,} characters")
        print(f"   Output: {output_file}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return None

if __name__ == "__main__":
    test_large_file_processing()