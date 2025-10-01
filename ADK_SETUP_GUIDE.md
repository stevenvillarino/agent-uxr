# 🚀 ADK-Enhanced InsightDeck Agent Setup Guide

## 🎯 Overview

This guide will help you set up the enhanced InsightDeck Agent with Google's Agent Development Kit (ADK) for real-time research session processing, multi-agent intelligence, and advanced audio analysis.

## 📋 Prerequisites

### Required Accounts & API Keys
- **OpenAI Account**: For GPT-4o analysis ([Get API Key](https://platform.openai.com/api-keys))
- **Google Cloud Account**: For ADK and Vertex AI ([Setup Guide](https://cloud.google.com/docs/get-started))
- **ElevenLabs Account** (Optional): For enhanced speaker diarization ([Get API Key](https://elevenlabs.io/))

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 16+ (for any frontend build tools)
- **Memory**: 8GB RAM minimum (16GB recommended for live sessions)
- **Storage**: 2GB free space
- **Internet**: Stable connection for real-time processing

## 🛠 Installation Steps

### 1. Clone and Navigate to Repository

```bash
git clone https://github.com/stevenvillarino/agent-uxr.git
cd agent-uxr
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install ADK-enhanced dependencies
pip install -r requirements-adk.txt

# Install additional NLP models (optional)
python -m spacy download en_core_web_sm
```

### 4. Google Cloud Setup

#### A. Create Google Cloud Project
```bash
# Install Google Cloud CLI
# macOS:
brew install google-cloud-sdk
# Windows: Download from https://cloud.google.com/sdk/docs/install

# Initialize gcloud
gcloud init

# Create new project (or use existing)
gcloud projects create insightdeck-adk --name="InsightDeck ADK"
gcloud config set project insightdeck-adk
```

#### B. Enable Required APIs
```bash
# Enable necessary Google Cloud APIs
gcloud services enable speech.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

#### C. Create Service Account
```bash
# Create service account
gcloud iam service-accounts create insightdeck-agent \
    --display-name="InsightDeck Agent Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding insightdeck-adk \
    --member="serviceAccount:insightdeck-agent@insightdeck-adk.iam.gserviceaccount.com" \
    --role="roles/speech.client"

gcloud projects add-iam-policy-binding insightdeck-adk \
    --member="serviceAccount:insightdeck-agent@insightdeck-adk.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download service account key
gcloud iam service-accounts keys create credentials.json \
    --iam-account=insightdeck-agent@insightdeck-adk.iam.gserviceaccount.com
```

### 5. Environment Configuration

Create `.env` file in the project root:

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
GOOGLE_CLOUD_PROJECT=insightdeck-adk
VERTEX_AI_LOCATION=us-central1

# ElevenLabs Configuration (Optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Application Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your_secret_key_here

# Redis Configuration (for session management)
REDIS_URL=redis://localhost:6379

# WebSocket Configuration
WEBSOCKET_HOST=localhost
WEBSOCKET_PORT=8081
```

### 6. Database Setup (Optional - for persistent sessions)

```bash
# Install Redis for session management
# macOS:
brew install redis
brew services start redis

# Ubuntu/Debian:
sudo apt-get install redis-server
sudo systemctl start redis-server

# Windows: Download from https://github.com/microsoftarchive/redis/releases
```

## 🎯 Configuration Verification

### Test API Connections

```bash
# Test OpenAI connection
python -c "
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Test connection'}],
    max_tokens=5
)
print('✅ OpenAI connection successful:', response.choices[0].message.content)
"

# Test Google Cloud connection
python -c "
from google.cloud import speech
import os

client = speech.SpeechClient()
print('✅ Google Cloud Speech API connection successful')
"
```

## 🚀 Running the Enhanced Application

### 1. Standard Web Interface

```bash
# Start the enhanced web application
python web_app.py

# Open browser to:
# http://localhost:8080 - Main interface
# http://localhost:8080/live - Live sessions interface
```

### 2. Live Session Mode with ADK

```bash
# Start with ADK live session support
python adk_live_session.py

# This enables:
# - Real-time audio processing
# - Multi-agent orchestration
# - Live WebSocket connections
```

### 3. Production Deployment

```bash
# Using Gunicorn for production
gunicorn -w 4 -b 0.0.0.0:8080 --worker-class eventlet web_app:app

# Or with Docker (if Dockerfile is available)
docker build -t insightdeck-adk .
docker run -p 8080:8080 --env-file .env insightdeck-adk
```

## 🎛 Feature Configuration

### ADK Agent Configuration

Edit `adk_live_session.py` to customize agents:

```python
# Customize Research Analyst Agent
research_analyst = Agent(
    model='gemini-2.0-flash',
    name='ResearchAnalyst',
    instruction="""
    Customize your research analysis instructions here:
    - Focus on specific research methodologies
    - Adjust sensitivity for different research types
    - Configure real-time insight thresholds
    """,
    tools=[your_custom_tools]
)
```

### Audio Processing Settings

```python
# Configure in adk_live_session.py
AUDIO_CONFIG = {
    'sample_rate': 16000,
    'chunk_duration': 1.0,  # seconds
    'max_speakers': 8,
    'enable_diarization': True,
    'language_codes': ['en-US', 'es-US'],  # Multi-language support
    'real_time_threshold': 0.8  # Confidence threshold for real-time insights
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Google Cloud Authentication Error
```bash
# Solution: Verify credentials
export GOOGLE_APPLICATION_CREDENTIALS="./credentials.json"
gcloud auth application-default login
```

#### 2. WebSocket Connection Issues
```bash
# Solution: Check firewall and port availability
netstat -an | grep 8081
sudo ufw allow 8081  # Ubuntu/Debian
```

#### 3. Audio Processing Errors
```bash
# Solution: Install audio dependencies
# macOS:
brew install portaudio
# Ubuntu/Debian:
sudo apt-get install portaudio19-dev python3-pyaudio
```

#### 4. Memory Issues During Live Sessions
```bash
# Solution: Increase Python memory limits
export PYTHONMALLOC=malloc
export MALLOC_TRIM_THRESHOLD_=100000
```

### Performance Optimization

#### 1. Enable GPU Acceleration (if available)
```bash
# Install CUDA-enabled dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 2. Configure Redis for Better Session Management
```bash
# Edit redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
```

## 📊 Usage Examples

### 1. Start a Live User Interview Session

```python
from adk_live_session import create_adk_enhanced_session

# Create live session
session_id = create_adk_enhanced_session(
    session_name="Mobile App Usability Test",
    research_type="usability_test"
)

print(f"Session started: {session_id}")
# Access at: http://localhost:8080/live?session={session_id}
```

### 2. Process Batch Files with ADK Enhancement

```bash
# Process multiple files with enhanced ADK features
python main_enhanced.py --batch-mode \
    --input-dir ./research_files \
    --output-dir ./enhanced_outputs \
    --enable-adk-agents \
    --enable-speaker-diarization
```

### 3. API Integration Example

```python
import requests

# Start live session via API
response = requests.post('http://localhost:8080/api/live-session', json={
    'session_name': 'Focus Group - Product Features',
    'research_type': 'focus_group',
    'max_speakers': 6,
    'enable_diarization': True
})

session_data = response.json()
print(f"Session URL: {session_data['websocket_url']}")
```

## 🔒 Security Considerations

### API Key Security
- Store API keys in environment variables, never in code
- Use different API keys for development and production
- Regularly rotate API keys
- Monitor API usage for unusual activity

### Session Security
- Implement session timeouts for live sessions
- Use JWT tokens for WebSocket authentication
- Enable HTTPS in production
- Implement rate limiting for API endpoints

### Data Privacy
- Configure data retention policies
- Implement automatic transcript deletion
- Use encryption for sensitive research data
- Comply with GDPR/CCPA requirements

## 📈 Monitoring and Analytics

### Application Monitoring

```python
# Add to your application
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('insightdeck.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Metrics
- Monitor API response times
- Track WebSocket connection stability
- Monitor memory usage during live sessions
- Track insight generation accuracy

## 🆘 Support and Resources

### Documentation
- **ADK Documentation**: https://google.github.io/adk-docs/
- **OpenAI API Docs**: https://platform.openai.com/docs
- **Google Cloud Speech**: https://cloud.google.com/speech-to-text/docs

### Community
- **GitHub Issues**: Report bugs and feature requests
- **Discord**: Join our developer community
- **Stack Overflow**: Tag questions with `insightdeck-agent`

### Professional Support
- **Enterprise Setup**: Available for large organizations
- **Custom Agent Development**: Specialized research agents
- **Integration Consulting**: Help with existing tool integration

## 🎯 Next Steps

1. **Complete Setup**: Follow all installation steps
2. **Test Basic Features**: Try file upload and processing
3. **Explore Live Sessions**: Start with a simple user interview
4. **Customize Agents**: Modify agents for your research needs
5. **Integrate with Tools**: Connect to Slack, Teams, or research platforms
6. **Scale Up**: Deploy to production environment

---

**🚀 Ready to revolutionize your research workflow? Start with the basic setup and gradually enable advanced ADK features!**

For questions or support, reach out to: [Your contact information]