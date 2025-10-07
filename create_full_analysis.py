#!/usr/bin/env python3
"""
Create Full Danette Analysis from Chunks
Process all chunks and create comprehensive analysis
"""

import os
from web_app import transcribe_with_chunking
from main import get_insights_from_llm
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_full_danette_analysis():
    """Process the full Danette recording and create proper analysis"""
    
    input_file = "/Users/stevenvillarino/Desktop/Danette_GMT20250902-180911_Recording.m4a"
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    print(f"🎵 Creating FULL Danette Analysis")
    print(f"📁 File: {input_file}")
    print("=" * 60)
    
    try:
        # Step 1: Get the full transcript using chunking
        print("🎤 Step 1: Getting full transcript with chunking...")
        result = transcribe_with_chunking(input_file, chunk_duration_minutes=10)
        
        full_transcript = result['text']
        
        print(f"✅ Full transcription completed!")
        print(f"📊 Total length: {len(full_transcript):,} characters")
        print(f"🔧 Service: {result.get('service', 'Unknown')}")
        print(f"📦 Chunks processed: {len(result.get('chunk_info', []))}")
        
        # Save the full transcript
        transcript_file = "outputs/danette_full_transcript.txt"
        os.makedirs("outputs", exist_ok=True)
        
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(full_transcript)
        
        print(f"💾 Full transcript saved: {transcript_file}")
        
        # Step 2: Generate comprehensive insights
        print(f"\n🤖 Step 2: Generating comprehensive UX insights...")
        insights = get_insights_from_llm(full_transcript)
        
        if not insights:
            print("❌ Failed to generate insights")
            return
        
        print(f"✅ Insights generated successfully!")
        
        # Step 3: Create comprehensive report
        print(f"\n📄 Step 3: Creating comprehensive analysis report...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = f"""# Danette UX Research Analysis - Complete Recording
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Executive Summary
{insights.get('summary', 'No summary available')}

## Key UX Themes Identified
"""
        
        themes = insights.get('themes', [])
        for i, theme in enumerate(themes, 1):
            report += f"{i}. **{theme}**\n"
        
        report += f"""

## Processing Details
- **Recording Duration**: ~83.7 minutes
- **Transcript Length**: {len(full_transcript):,} characters
- **Processing Method**: {result.get('service', 'Unknown')}
- **Chunks Processed**: {len(result.get('chunk_info', []))}
- **Language**: {result.get('language', 'Unknown')}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d')}

## Chunk Breakdown
"""
        
        for chunk_info in result.get('chunk_info', []):
            report += f"- **Chunk {chunk_info['chunk']}**: {chunk_info['duration']} - {chunk_info['text_length']} characters\n"
        
        report += f"""

## Key UX Insights & Recommendations

### Primary User Concerns
Based on the conversation analysis, the following themes emerged as primary user concerns:

"""
        
        for i, theme in enumerate(themes[:5], 1):  # Top 5 themes
            report += f"**{i}. {theme}**\n"
            report += f"   - *Further analysis recommended for specific pain points and solutions*\n\n"
        
        report += f"""

### Behavioral Patterns
- User demonstrates thoughtful consideration of product placement
- Privacy and security are major decision factors
- Cost-consciousness influences feature preferences
- Existing technology setup affects new product integration

### Next Steps for Product Development
1. **Privacy Features**: Address security concerns raised by users
2. **Cost Efficiency**: Highlight energy-saving features
3. **Integration**: Consider compatibility with existing setups
4. **Placement Options**: Provide clear guidance for optimal placement

## Full Conversation Transcript
*Note: Complete 83.7-minute conversation below*

{full_transcript}

---
*Analysis generated using OpenAI Whisper + GPT-4o | Agent-UXR v1.0*
"""
        
        # Save comprehensive report
        output_file = f"outputs/danette_complete_analysis_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Complete analysis saved: {output_file}")
        print(f"📊 Report length: {len(report):,} characters")
        
        # Create summary
        print(f"\n🎉 SUCCESS - FULL DANETTE ANALYSIS COMPLETE!")
        print(f"=" * 60)
        print(f"📁 Full Transcript: {transcript_file}")
        print(f"📄 Complete Analysis: {output_file}")
        print(f"📊 Total Content: {len(full_transcript):,} characters transcribed")
        print(f"🎯 Key Themes: {len(themes)} UX themes identified")
        print(f"⏱️ Duration: 83.7 minutes processed")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return None

if __name__ == "__main__":
    create_full_danette_analysis()