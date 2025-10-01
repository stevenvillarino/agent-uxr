import os
import json
import argparse
import tempfile
import whisper
from openai import OpenAI

# Initialize the OpenAI client
# Assumes OPENAI_API_KEY environment variable is set
client = OpenAI()

def transcribe_audio_with_whisper(audio_file_path: str) -> str:
    """
    Transcribe audio file using OpenAI Whisper.
    """
    try:
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        
        print(f"Transcribing audio file: {audio_file_path}")
        result = model.transcribe(audio_file_path)
        
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def transcribe_audio_with_openai_api(audio_file_path: str) -> str:
    """
    Transcribe audio file using OpenAI API (Whisper via API).
    This is faster but requires API credits.
    """
    try:
        print(f"Transcribing audio via OpenAI API: {audio_file_path}")
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript
    except Exception as e:
        print(f"Error transcribing audio via API: {e}")
        return None

def get_insights_from_llm(text_content: str) -> dict:
    """
    Sends the transcript to an LLM to extract a summary and key themes.
    """
    system_prompt = """
    You are an expert user research analyst. Your task is to analyze the provided
    transcript and extract a concise summary and the top 3-5 key themes.
    Return the output as a valid JSON object with two keys: "summary" and "themes".
    The "themes" value should be a list of strings.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content}
            ],
            response_format={"type": "json_object"}
        )
        insights = json.loads(response.choices[0].message.content)
        return insights
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return None

def format_marp_presentation(title: str, insights: dict) -> str:
    """
    Formats the extracted insights into a Marp Markdown presentation string.
    """
    if not insights or "summary" not in insights or "themes" not in insights:
        return "# Error\n\nCould not generate presentation."

    # Marp front-matter
    content = f"---\nmarp: true\ntheme: default\n---\n\n"
    
    # Title Slide
    content += f"# {title}\n\n---\n\n"
    
    # Summary Slide
    content += f"## Executive Summary\n\n{insights['summary']}\n\n---\n\n"
    
    # Theme Slides
    content += "## Key Themes\n\n"
    for i, theme in enumerate(insights['themes']):
        content += f"{i+1}. {theme}\n"
    
    return content

def main():
    """
    Main orchestrator for the POC with Whisper support.
    """
    parser = argparse.ArgumentParser(description="Generate a presentation from a research transcript or audio file.")
    parser.add_argument("filepath", type=str, help="Path to the input file (.txt, .mp3, .wav, .m4a, .mp4)")
    parser.add_argument("--use-api", action="store_true", help="Use OpenAI API for transcription (faster but costs credits)")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}")
        return

    file_extension = os.path.splitext(args.filepath)[1].lower()
    
    # Check if it's an audio file
    audio_extensions = ['.mp3', '.wav', '.m4a', '.mp4', '.flac', '.ogg']
    
    if file_extension in audio_extensions:
        print(f"1. Detected audio file: {args.filepath}")
        
        if args.use_api:
            transcript = transcribe_audio_with_openai_api(args.filepath)
        else:
            transcript = transcribe_audio_with_whisper(args.filepath)
        
        if not transcript:
            print("Failed to transcribe audio. Aborting.")
            return
            
        print("2. Transcription completed!")
        
        # Optionally save the transcript
        transcript_filename = os.path.splitext(args.filepath)[0] + "_transcript.txt"
        with open(transcript_filename, 'w') as f:
            f.write(transcript)
        print(f"   Transcript saved to: {transcript_filename}")
        
    elif file_extension == '.txt':
        print(f"1. Reading text transcript from {args.filepath}...")
        with open(args.filepath, 'r') as f:
            transcript = f.read()
    else:
        print(f"Error: Unsupported file format '{file_extension}'. Supported formats: .txt, .mp3, .wav, .m4a, .mp4, .flac, .ogg")
        return

    print("3. Extracting insights using AI...")
    insights = get_insights_from_llm(transcript)

    if insights:
        print("4. Formatting presentation...")
        presentation_title = os.path.splitext(os.path.basename(args.filepath))[0].replace('_', ' ').title()
        marp_content = format_marp_presentation(presentation_title, insights)
        
        output_filename = "presentation.md"
        print(f"5. Writing Marp presentation to {output_filename}...")
        with open(output_filename, 'w') as f:
            f.write(marp_content)
        
        print("\nSuccess! To view your presentation, install the Marp VS Code extension and open presentation.md.")
        if file_extension in audio_extensions:
            print(f"Transcript was also saved to: {transcript_filename}")
    else:
        print("Failed to generate insights. Aborting.")

if __name__ == "__main__":
    main()