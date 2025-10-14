# 🐳 Docker Quick Start Guide

## One-Command Demo Setup

**For people who just want to demo without installing anything:**

### Prerequisites
- Docker and Docker Compose installed ([Get Docker](https://docs.docker.com/get-docker/))
- OpenAI API Key (get from [OpenAI Platform](https://platform.openai.com/api-keys))

### Super Quick Start (3 steps)

1. **Clone and enter directory:**
   ```bash
   git clone https://github.com/stevenvillarino/agent-uxr.git
   cd agent-uxr
   ```

2. **Set your OpenAI API key:**
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

3. **Run the demo:**
   ```bash
   docker compose up
   ```

   That's it! 🎉 Open http://localhost:8080

### Alternative Docker Commands

**Build and run manually:**
```bash
# Build the image
docker build -t insightdeck-agent .

# Run with environment file
docker run -p 8080:8080 --env-file .env insightdeck-agent

# Or run with inline environment variable
docker run -p 8080:8080 -e OPENAI_API_KEY=your_key_here insightdeck-agent
```

### Features Available in Docker

✅ **Full Web Interface** - Upload files, get analysis  
✅ **Audio Transcription** - OpenAI Whisper integration  
✅ **AI Analysis** - GPT-4 powered insights  
✅ **Presentation Generation** - Download ready presentations  
✅ **Sample Data** - Pre-loaded demo files  

### Demo Files Included

The Docker container includes sample files in `/app/sample_data/`:
- `customer_support_call.txt`
- `focus_group_mobile_app.txt` 
- `user_interview_dashboard.txt`
- `team_standup_meeting.txt`

### Stopping the Demo

```bash
# Stop the container
docker compose down

# Or if running manually
docker stop $(docker ps -q --filter ancestor=insightdeck-agent)
```

### Troubleshooting

**Port already in use?**
```bash
# Use a different port
docker run -p 3000:8080 --env-file .env insightdeck-agent
# Then open http://localhost:3000
```

**Missing API key?**
```bash
# Check your .env file
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

---

## Why Docker?

- ✅ **Zero dependency installation** - No Python, no packages
- ✅ **Works everywhere** - Mac, Windows, Linux
- ✅ **Clean environment** - No conflicts with existing setup
- ✅ **Easy cleanup** - Remove with one command
- ✅ **Consistent demo** - Same experience for everyone

Perfect for demos, client presentations, and quick testing!