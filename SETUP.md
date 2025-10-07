# Setup & Troubleshooting Guide

## Quick Start

### 1. Environment Setup

```bash
# Clone and navigate to project
cd agent-uxr

# Create .env file with your API keys
cp .env.template .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python web_app.py
```

Then open: http://localhost:5000

## Troubleshooting

### Text Analysis Shows Same Results

**Problem:** Pasted text always shows same generic analysis

**Solution:** This was fixed on Oct 6, 2025. Update to latest version.

**Verify Fix:**
```bash
python test_analysis.py
```

### Audio Transcription Not Working

**Problem:** "Whisper not installed" or compatibility errors

**Solution:** We use OpenAI Whisper API (cloud-based), not local installation.

**Requirements:**
- Valid `OPENAI_API_KEY` in `.env`
- Internet connection
- Audio file under 25MB

**Verify:**
```bash
python test_whisper_api.py
```

### ElevenLabs Credits Ran Out

**Problem:** Can't use ElevenLabs transcription

**Solution:** Use OpenAI Whisper instead (default option)
- Select "OpenAI Whisper" in web interface
- Cost: $0.006/minute (~$0.36/hour)
- No speaker diarization, but works great for general transcription

### API Key Errors

**Problem:** "API key not found" or authentication errors

**Check:**
```bash
# Verify .env file exists
cat .env | grep OPENAI_API_KEY

# Should show: OPENAI_API_KEY=sk-...
# NOT: OPENAI_API_KEY=your_openai_api_key_here
```

**Solution:** Update `.env` with real API key from https://platform.openai.com/api-keys

### Python Version Issues

**Current:** Python 3.13.3 ✅

**Compatible with:**
- OpenAI Whisper API (cloud) ✅
- All other features ✅

**Not compatible with:**
- Local Whisper installation (requires Python 3.11)
- We don't use local Whisper, so this is fine ✅

## Testing

### Test Text Analysis
```bash
python test_analysis.py
```

### Test Whisper API
```bash
python test_whisper_api.py
```

### Test Full App
```bash
python web_app.py
# Then test in browser at http://localhost:5000
```

## Configuration

### Required
- `OPENAI_API_KEY` - For GPT-4 analysis and Whisper API

### Optional
- `ELEVENLABS_API_KEY` - For speaker diarization (only if needed)

## Cost Guide

| Service | Cost | When to Use |
|---------|------|-------------|
| **OpenAI GPT-4** | ~$0.01-0.05/analysis | Text analysis (required) |
| **OpenAI Whisper API** | $0.006/minute | Audio transcription (default) |
| **ElevenLabs** | $0.005/minute | Only if need speaker diarization |

**Example Monthly Costs:**
- 100 text analyses: ~$2-5
- 50 hours of audio: ~$18 (Whisper API)
- Total: ~$20-25/month for moderate usage

## Common Workflows

### Analyze Pasted Text
1. Enter title
2. Choose "Paste Text"
3. Paste your content
4. Click "Generate Presentation"
5. Download results

### Transcribe Audio
1. Enter title
2. Choose "Upload Audio File"
3. Select file
4. Choose "OpenAI Whisper"
5. Click "Generate Presentation"
6. Get transcription + analysis

### Export Results
1. After generating insights
2. Choose export format (Markdown/HTML/JSON)
3. Select template style
4. Click download

## File Structure

```
agent-uxr/
├── web_app.py              # Main Flask application
├── main.py                 # Core analysis functions
├── templates/              # HTML templates
│   └── index.html         # Web interface
├── test_analysis.py        # Test text analysis
├── test_whisper_api.py     # Test audio transcription
├── .env                    # Your API keys (create from template)
└── docs/                   # Additional documentation
```

## Getting Help

1. **Check this guide first**
2. **Run test scripts** to diagnose issues
3. **Check terminal logs** for error messages
4. **Verify API keys** in `.env` file

## Recent Updates

- **Oct 6, 2025:** Fixed text analysis, updated to Whisper API
- **Oct 2, 2025:** Production deployment ready
- See `CHANGELOG.md` for complete history
