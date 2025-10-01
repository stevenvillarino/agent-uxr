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
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
    # Enhanced prompt for speaker-aware analysis
    if transcription_info and transcription_info.get("has_diarization"):
        system_prompt = """
        You are an expert user research analyst. Your task is to analyze the provided
        transcript that includes speaker identification and extract:
        1. A concise summary (2-3 sentences)
        2. The top 3-5 key themes
        3. Speaker-specific insights if multiple speakers are detected
        
        Return the output as a valid JSON object with keys: "summary", "themes", and optionally "speaker_insights".
        The "themes" value should be a list of strings.
        """
    else:
        system_prompt = """
        You are an expert user research analyst. Your task is to analyze the provided
        transcript and extract a concise summary and the top 3-5 key themes.
        Return the output as a valid JSON object with two keys: "summary" and "themes".
        The "themes" value should be a list of strings.
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
    Formats the extracted insights into a Marp Markdown presentation string.
    Enhanced to show diarization capabilities when available.
    """
    if not insights or "summary" not in insights or "themes" not in insights:
        return "# Error\n\nCould not generate presentation."

    # Marp front-matter
    content = f"---\nmarp: true\ntheme: default\n---\n\n"
    
    # Title Slide
    content += f"# {title}\n\n"
    
    # Add transcription service info
    if insights.get("transcription_service"):
        service = insights["transcription_service"].title()
        diarization = "✅ Speaker Separation" if insights.get("has_diarization") else "❌ No Speaker Separation"
        content += f"*Transcribed with {service} | {diarization}*\n\n"
    
    content += "---\n\n"
    
    # Summary Slide
    content += f"## Executive Summary\n\n{insights['summary']}\n\n---\n\n"
    
    # Theme Slides
    content += "## Key Themes\n\n"
    for i, theme in enumerate(insights['themes']):
        content += f"{i+1}. {theme}\n"
    
    # Speaker insights if available
    if insights.get("speaker_insights"):
        content += "\n---\n\n## Speaker Insights\n\n"
        for speaker_insight in insights["speaker_insights"]:
            content += f"- {speaker_insight}\n"
    
    # Add capability note
    content += "\n---\n\n## Transcription Capabilities\n\n"
    content += "| Service | Transcription | Speaker Diarization |\n"
    content += "|---------|---------------|--------------------|\n"
    content += "| OpenAI Whisper | ✅ Excellent | ❌ Not Available |\n"
    content += "| AWS Transcribe | ✅ Good | ✅ Available |\n"
    content += "| Azure Speech | ✅ Good | ✅ Available |\n"
    
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