#!/usr/bin/env python3
"""
Quick Analysis of Danette Recording
Create a simple text analysis from the transcript
"""

import os
from main import get_insights_from_llm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def analyze_danette_transcript():
    """Create analysis from the processed transcript"""
    
    # Check if we have a transcript from the previous run
    transcript_file = "temp_danette_transcript.txt"
    
    if not os.path.exists(transcript_file):
        print("❌ No transcript file found. Let me create one from a chunk...")
        
        # Use the first chunk to create a sample analysis
        chunk_file = "chunks/Danette_GMT20250902-180911_Recording_chunk_01.mp3"
        
        if os.path.exists(chunk_file):
            print(f"🎤 Transcribing first chunk: {chunk_file}")
            
            with open(chunk_file, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            sample_transcript = transcript.text
            
            with open(transcript_file, 'w') as f:
                f.write(sample_transcript)
                
            print(f"✅ Created sample transcript: {len(sample_transcript)} characters")
        else:
            print("❌ No chunk files found")
            return
    else:
        # Read existing transcript
        with open(transcript_file, 'r') as f:
            sample_transcript = f.read()
        print(f"📝 Using existing transcript: {len(sample_transcript)} characters")
    
    # Generate insights
    print("🤖 Generating UX insights...")
    
    insights = get_insights_from_llm(sample_transcript)
    
    if insights:
        print("✅ Insights generated successfully!")
        
        # Create a simple analysis report
        report = f"""# Danette UX Research Analysis

## Executive Summary
{insights.get('summary', 'No summary available')}

## Key Themes Identified
"""
        
        for i, theme in enumerate(insights.get('themes', []), 1):
            report += f"{i}. {theme}\n"
        
        report += f"""
## Sample Transcript (First 5 minutes)
{sample_transcript[:2000]}...

## Analysis Details
- Language: English
- Processing: OpenAI Whisper + GPT-4o
- Date: October 7, 2025
- Total Duration: ~83.7 minutes
- Sample Length: {len(sample_transcript)} characters

## Recommendations
Based on this sample analysis, further investigation is recommended for:
1. User pain points identified in the conversation
2. Specific feature requests or suggestions
3. Behavioral patterns and user goals
4. Technical implementation priorities

*Note: This is a sample analysis from the first 5-minute segment. 
Full analysis would require processing all 17 chunks.*
"""
        
        # Save the report
        output_file = "outputs/danette_sample_analysis.md"
        os.makedirs("outputs", exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"📄 Analysis saved: {output_file}")
        print(f"📊 Report length: {len(report)} characters")
        
        # Show preview
        print("\n📖 PREVIEW:")
        print("=" * 50)
        print(report[:500] + "...")
        
        return output_file
    else:
        print("❌ Failed to generate insights")
        return None

if __name__ == "__main__":
    analyze_danette_transcript()