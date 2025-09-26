import os
import json
import argparse
from openai import OpenAI

# Initialize the OpenAI client
# Assumes OPENAI_API_KEY environment variable is set
client = OpenAI()

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
    Main orchestrator for the POC.
    """
    parser = argparse.ArgumentParser(description="Generate a presentation from a research transcript.")
    parser.add_argument("filepath", type=str, help="Path to the input transcript .txt file.")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}")
        return

    print(f"1. Reading transcript from {args.filepath}...")
    with open(args.filepath, 'r') as f:
        transcript = f.read()

    print("2. Extracting insights using AI...")
    insights = get_insights_from_llm(transcript)

    if insights:
        print("3. Formatting presentation...")
        presentation_title = os.path.splitext(os.path.basename(args.filepath))[0].replace('_', ' ').title()
        marp_content = format_marp_presentation(presentation_title, insights)
        
        output_filename = "presentation.md"
        print(f"4. Writing Marp presentation to {output_filename}...")
        with open(output_filename, 'w') as f:
            f.write(marp_content)
        
        print("\nSuccess! To view your presentation, install the Marp VS Code extension and open presentation.md.")
    else:
        print("Failed to generate insights. Aborting.")

if __name__ == "__main__":
    main()
