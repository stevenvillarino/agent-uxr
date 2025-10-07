import os
import json
import argparse
import tempfile
import whisper
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
# This will use OPENAI_API_KEY from environment or .env file
client = OpenAI()

def transcribe_audio_with_whisper(audio_file_path: str) -> dict:
    """
    Transcribe audio file using OpenAI Whisper.
    Note: Whisper does NOT provide speaker diarization.
    """
    try:
        model_name = os.getenv('WHISPER_MODEL', 'base')
        print(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        
        print(f"Transcribing audio file: {audio_file_path}")
        result = model.transcribe(audio_file_path)
        
        return {
            "text": result["text"],
            "segments": result.get("segments", []),
            "language": result.get("language", "unknown"),
            "has_diarization": False,
            "transcription_service": "whisper"
        }
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def transcribe_with_aws_transcribe(audio_file_path: str) -> dict:
    """
    Transcribe audio with speaker diarization using AWS Transcribe.
    This is a placeholder - requires AWS setup and implementation.
    """
    try:
        # This would require AWS SDK setup
        import boto3
        
        print("AWS Transcribe with speaker diarization is not yet implemented.")
        print("This would provide speaker separation: [Speaker 1] Hello [Speaker 2] Hi there")
        
        # Placeholder return
        return {
            "text": "AWS Transcribe integration not implemented yet",
            "segments": [],
            "language": "en",
            "has_diarization": True,
            "transcription_service": "aws-transcribe",
            "speakers": []
        }
    except ImportError:
        print("AWS SDK (boto3) not installed. Install with: pip install boto3")
        return None
    except Exception as e:
        print(f"Error with AWS Transcribe: {e}")
        return None

def get_insights_from_llm(text_content: str, transcription_info: dict = None) -> dict:
    """
    Sends the transcript to an LLM to extract a summary and key themes.
    Enhanced to handle speaker information if available.
    """
    # Enhanced prompt for UX-focused analysis
    if transcription_info and transcription_info.get("has_diarization"):
        system_prompt = """
        You are a senior UX researcher with expertise in user experience design and behavioral analysis.
        
        Analyze this user research transcript with speaker identification. Focus on extracting specific, actionable UX insights:
        
        ANALYZE FOR:
        - User pain points and specific frustrations mentioned
        - Usability issues and interface problems
        - User goals, motivations, and mental models
        - Feature requests and improvement suggestions
        - Accessibility concerns or barriers
        - Workflow inefficiencies and friction points
        - Positive user experiences and what works well
        
        AVOID generic statements. Be specific to what users actually said.
        
        Return JSON with:
        - "summary": Executive summary highlighting critical UX findings (2-3 sentences)
        - "themes": 4-6 specific, actionable UX themes (not generic statements)
        - "pain_points": Top 3-5 specific user frustrations mentioned
        - "recommendations": 3-4 concrete UX improvements prioritized by impact
        - "speaker_insights": Key insights organized by speaker role if multiple speakers
        """
    else:
        system_prompt = """
        You are a senior UX researcher with expertise in user experience design and behavioral analysis.
        
        Analyze this user research transcript and extract specific, actionable UX insights grounded in what users actually said:
        
        CRITICAL ANALYSIS REQUIREMENTS:
        1. QUOTE ACTUAL USER WORDS - Include direct quotes that support each insight
        2. BE SPECIFIC - Avoid generic UX statements like "users want better navigation"
        3. IDENTIFY ROOT CAUSES - Don't just list complaints, explain the underlying UX problems
        4. PRIORITIZE BY IMPACT - Focus on issues that affect core user workflows
        
        ANALYZE FOR:
        - Specific usability failures: "I clicked X expecting Y but got Z"
        - Emotional reactions: frustration, confusion, delight expressed by users
        - Mental model mismatches: where user expectations don't match interface behavior
        - Workflow interruptions: specific points where users get stuck or lose efficiency
        - Feature gaps: explicit requests for missing functionality
        - Accessibility barriers: any mention of difficulty seeing, hearing, or interacting
        - Success moments: what specifically works well and why
        
        EXAMPLE FORMAT FOR INSIGHTS:
        Instead of: "Users want better navigation"
        Write: "Users confused by 'Analytics' vs 'Insights' tabs - participant said 'I don't know what the difference is between Analytics and Insights - those feel like they could be the same thing' - suggests navigation taxonomy needs clarification"
        
        Return JSON with:
        - "summary": 2-3 sentences highlighting the most critical UX findings with user impact
        - "themes": 4-6 specific UX themes, each with supporting user quotes or examples
        - "pain_points": Top 3-5 specific frustrations with exact user quotes
        - "recommendations": 3-4 concrete UX improvements with rationale tied to user feedback
        - "user_quotes": 5-8 most revealing direct quotes that illustrate key insights
        """
    
    try:
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content}
            ],
            response_format={"type": "json_object"}
        )
        insights = json.loads(response.choices[0].message.content)
        
        # Add transcription metadata
        if transcription_info:
            insights["transcription_service"] = transcription_info.get("transcription_service", "unknown")
            insights["has_diarization"] = transcription_info.get("has_diarization", False)
            insights["detected_language"] = transcription_info.get("language", "unknown")
        
        return insights
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return None

def format_marp_presentation(title: str, insights: dict) -> str:
    """
    Formats the UX insights into a comprehensive Marp presentation.
    Enhanced to show transcription capabilities and UX-specific content.
    """
    if not insights or "summary" not in insights:
        return "# Error\n\nCould not generate presentation."

    # Marp front-matter with custom styling
    content = """---
marp: true
theme: default
class: invert
paginate: true
---

<!-- _class: lead -->
"""
    
    # Title Slide
    content += f"# {title}\n## UX Research Insights\n\n"
    
    # Add transcription service info
    if insights.get("transcription_service"):
        service = insights["transcription_service"].title()
        diarization = "✅ Speaker Separation" if insights.get("has_diarization") else "❌ No Speaker Separation"
        content += f"*Transcribed with {service} | {diarization}*\n\n"
    
    content += "*Generated by Agent-UXR*\n\n---\n\n"
    
    # Executive Summary
    content += f"## Executive Summary\n\n{insights['summary']}\n\n---\n\n"
    
    # Key Themes
    if "themes" in insights:
        content += "## Key UX Themes\n\n"
        for i, theme in enumerate(insights['themes'], 1):
            content += f"### {i}. {theme}\n\n"
        content += "---\n\n"
    
    # Pain Points
    if "pain_points" in insights:
        content += "## 🚨 Critical Pain Points\n\n"
        for i, pain in enumerate(insights['pain_points'], 1):
            content += f"**{i}.** {pain}\n\n"
        content += "---\n\n"
    
    # Recommendations
    if "recommendations" in insights:
        content += "## 💡 Prioritized Recommendations\n\n"
        for i, rec in enumerate(insights['recommendations'], 1):
            content += f"### {i}. {rec}\n\n"
        content += "---\n\n"
    
    # User Quotes
    if "user_quotes" in insights:
        content += "## 💬 Key User Quotes\n\n"
        for i, quote in enumerate(insights['user_quotes'], 1):
            content += f"> \"{quote}\"\n\n"
        content += "---\n\n"
    
    # Speaker insights if available
    if insights.get("speaker_insights"):
        content += "## 👥 Speaker-Specific Insights\n\n"
        for speaker_insight in insights["speaker_insights"]:
            content += f"- {speaker_insight}\n\n"
        content += "---\n\n"
    
    # Next Steps
    content += """## Next Steps

1. **Prioritize** critical pain points for immediate fixes
2. **Prototype** top recommended solutions  
3. **Validate** changes with follow-up user testing
4. **Measure** impact with analytics and user feedback

---

## Transcription Capabilities

| Service | Transcription | Speaker Diarization |
|---------|---------------|---------------------|
| OpenAI Whisper | ✅ Excellent | ❌ Not Available |
| AWS Transcribe | ✅ Good | ✅ Available |
| Azure Speech | ✅ Good | ✅ Available |

---

<!-- _class: lead -->

## Questions?

*Ready for actionable UX improvements*"""
    
    return content

def main():
    """
    Main orchestrator for the POC with enhanced transcription options.
    """
    parser = argparse.ArgumentParser(description="Generate a presentation from a research transcript or audio file.")
    parser.add_argument("filepath", type=str, help="Path to the input file (.txt, .mp3, .wav, .m4a, .mp4)")
    parser.add_argument("--service", choices=["whisper", "aws", "azure"], default="whisper",
                       help="Transcription service to use")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}")
        return

    file_extension = os.path.splitext(args.filepath)[1].lower()
    
    # Check if it's an audio file
    audio_extensions = ['.mp3', '.wav', '.m4a', '.mp4', '.flac', '.ogg']
    
    if file_extension in audio_extensions:
        print(f"1. Detected audio file: {args.filepath}")
        
        transcription_result = None
        
        if args.service == "whisper":
            print("Using OpenAI Whisper (no speaker diarization)")
            transcription_result = transcribe_audio_with_whisper(args.filepath)
        elif args.service == "aws":
            print("Using AWS Transcribe (with speaker diarization)")
            transcription_result = transcribe_with_aws_transcribe(args.filepath)
        elif args.service == "azure":
            print("Azure Speech Services not yet implemented")
            return
        
        if not transcription_result:
            print("Failed to transcribe audio. Aborting.")
            return
            
        transcript = transcription_result["text"]
        print("2. Transcription completed!")
        
        # Show diarization status
        if transcription_result.get("has_diarization"):
            print("   ✅ Speaker diarization available")
        else:
            print("   ❌ No speaker diarization (use --service aws for speakers)")
        
        # Optionally save the transcript
        transcript_filename = os.path.splitext(args.filepath)[0] + "_transcript.txt"
        with open(transcript_filename, 'w') as f:
            f.write(transcript)
        print(f"   Transcript saved to: {transcript_filename}")
        
    elif file_extension == '.txt':
        print(f"1. Reading text transcript from {args.filepath}...")
        with open(args.filepath, 'r') as f:
            transcript = f.read()
        transcription_result = {"text": transcript, "has_diarization": False, "transcription_service": "manual"}
    else:
        print(f"Error: Unsupported file format '{file_extension}'. Supported formats: .txt, .mp3, .wav, .m4a, .mp4, .flac, .ogg")
        return

    print("3. Extracting insights using AI...")
    insights = get_insights_from_llm(transcript, transcription_result)

    if insights:
        print("4. Formatting presentation...")
        presentation_title = os.path.splitext(os.path.basename(args.filepath))[0].replace('_', ' ').title()
        marp_content = format_marp_presentation(presentation_title, insights)
        
        output_filename = "presentation.md"
        print(f"5. Writing Marp presentation to {output_filename}...")
        with open(output_filename, 'w') as f:
            f.write(marp_content)
        
        print("\n✅ Success! To view your presentation, install the Marp VS Code extension and open presentation.md.")
        if file_extension in audio_extensions:
            print(f"📄 Transcript was also saved to: {transcript_filename}")
            
        # Show capability summary
        print(f"\n📊 Transcription Summary:")
        print(f"   Service: {transcription_result.get('transcription_service', 'unknown').title()}")
        print(f"   Speaker Diarization: {'✅ Yes' if transcription_result.get('has_diarization') else '❌ No'}")
        print(f"   Language: {transcription_result.get('language', 'unknown')}")
    else:
        print("Failed to generate insights. Aborting.")

if __name__ == "__main__":
    main()