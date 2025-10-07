# Agent-UXR Startup Guide 🚀

Welcome to Agent-UXR! This guide will get you up and running quickly with automated setup and troubleshooting tips.

## Quick Start (Automated Setup)

### 1. Run the Setup Script

```bash
# Make the setup script executable and run it
chmod +x setup.sh
./setup.sh
```

### 2. Manual Setup (if script fails)

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate    # On Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env file with your API keys
```

### 3. Required Environment Variables

Create a `.env` file in the project root with:

```env
# Required for AI analysis
OPENAI_API_KEY=your_openai_api_key_here

# Optional - for enhanced transcription services
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=your_azure_region_here
AWS_ACCESS_KEY_ID=your_aws_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here
```

## Demo Options

### Option 1: Basic Text Analysis
```bash
python main.py sample_data/user_interview_dashboard.txt
```

### Option 2: Web Interface
```bash
python web_app.py
# Open http://localhost:5000 in your browser
```

### Option 3: Audio Transcription + Analysis
```bash
python main_with_whisper.py your_audio_file.mp3
```

### Option 4: Live Session Recording
```bash
python adk_live_session.py
# Navigate to http://localhost:5000/live for real-time recording
```

## Troubleshooting Common Issues

### ❌ "Getting irrelevant or boilerplate insights"

**Problem**: The AI is giving generic analysis instead of UX-specific insights.

**Solution**: The issue is in the system prompt. Use the enhanced version:

```bash
# Use the enhanced main file with better prompts
python main_enhanced.py sample_data/user_interview_dashboard.txt
```

### ❌ "Module not found" errors

**Solution**: Make sure virtual environment is activated:
```bash
source .venv/bin/activate  # macOS/Linux
pip list  # Verify packages are installed
```

### ❌ OpenAI API errors

**Solution**: Check your API key and billing:
```bash
# Test API key
python -c "
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
print('API Key loaded:', bool(os.getenv('OPENAI_API_KEY')))
"
```

### ❌ Audio file not supported

**Solution**: Convert to supported format:
```bash
# Install ffmpeg if needed
brew install ffmpeg  # macOS
# or
sudo apt install ffmpeg  # Linux

# Convert audio file
ffmpeg -i input.m4a output.wav
```

## Sample Test Commands

```bash
# Quick test with sample data
python main_enhanced.py sample_data/user_interview_dashboard.txt

# Test web interface
python web_app.py &
curl http://localhost:5000

# Test Whisper transcription
python test_whisper_api.py

# Run all tests
chmod +x quick_test.sh
./quick_test.sh
```

## Expected Output

After successful setup, you should see:
1. ✅ A `presentation.md` file generated
2. ✅ Structured insights about user research findings
3. ✅ UX-specific themes and actionable recommendations
4. ✅ Clean, professional presentation format

## Support

If you encounter issues:
1. Check the `CHANGELOG.md` for recent fixes
2. Review `docs/guides/TROUBLESHOOTING.md`
3. Run the diagnostic script: `python test_analysis.py`

---
*Last updated: October 7, 2025*