# InsightDeck Agent

An AI-powered system that transforms user research transcripts into professional presentation decks automatically.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd OpenAI-Whisper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

### Usage

Run the POC with a transcript file:
```bash
python main.py transcript.txt
```

This will generate a `presentation.md` file that you can view with the Marp VS Code extension.

### Example Output

The system will create a presentation with:
- Title slide
- Executive summary
- Key themes identified from the transcript

## 📋 What This Project Does

InsightDeck Agent automates the research-to-presentation workflow that typically takes hours of manual work:

1. **Input:** Research transcript (text file)
2. **AI Processing:** Extracts key insights and themes using GPT-4o
3. **Output:** Structured presentation in Markdown format

### Current POC Features

- ✅ Text file input processing
- ✅ AI-powered insight extraction
- ✅ Marp presentation generation
- ✅ Command-line interface

## 🎯 Project Vision

This POC is the foundation for a comprehensive enterprise solution that will include:

- **Audio Transcription:** Direct processing of interview recordings
- **Multi-Agent System:** Specialized AI agents for analysis, visualization, and presentation
- **Data Visualization:** Automatic chart and infographic generation  
- **Enterprise Features:** SSO, collaboration, brand templates, API access
- **Workflow Integration:** Slack, Teams, SharePoint, and more

## 📚 Documentation

Comprehensive documentation is available:

- **[Product Requirements Document (PRD.md)](./PRD.md)** - Full product vision and requirements
- **[System Architecture (ARCHITECTURE.md)](./ARCHITECTURE.md)** - Technical architecture and scaling plans  
- **[Feature Specifications (FEATURES.md)](./FEATURES.md)** - Detailed feature descriptions and roadmap

## 🛠 Development

### Project Structure

```
├── main.py              # POC implementation
├── transcript.txt       # Sample input file
├── presentation.md      # Generated output (after running)
├── requirements.txt     # Python dependencies
├── PRD.md              # Product Requirements Document
├── ARCHITECTURE.md     # System Architecture
├── FEATURES.md         # Feature Specifications
└── README.md           # This file
```

### Tech Stack

**Current POC:**
- Python 3.8+
- OpenAI GPT-4o API
- Marp (Markdown presentations)

**Future Enterprise Stack:**
- FastAPI/Flask (Backend)
- React/Vue.js (Frontend)
- PostgreSQL (Database)
- Redis (Caching)
- Docker/Kubernetes (Infrastructure)
- Multiple AI services (OpenAI, Cohere, Whisper)

## 🧪 Testing

Run the POC with the provided sample transcript:
```bash
python main.py transcript.txt
```

Expected output: `presentation.md` file with structured research insights.

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (default: "gpt-4o")

### Customization

The POC can be customized by modifying:
- AI prompt in `get_insights_from_llm()` function
- Presentation template in `format_marp_presentation()` function
- Processing parameters and error handling

## 📈 Roadmap

### Phase 1: POC (Current) ✅
- Basic text processing and presentation generation
- OpenAI integration
- Marp output format

### Phase 2: MVP (Q1 2026)
- Audio file support (Whisper integration)
- Web interface
- Enhanced templates
- Error handling improvements

### Phase 3: Enterprise (Q2-Q4 2026)
- Multi-agent orchestration
- Data visualization
- Speaker diarization
- Enterprise security and compliance
- Collaboration features

## 🤝 Contributing

This is currently a POC project. For enterprise development inquiries or collaboration opportunities, please reach out through the repository issues.

## 📄 License

[Add appropriate license]

## 🆘 Support

### Common Issues

1. **"Import 'openai' could not be resolved"**
   - Install dependencies: `pip install -r requirements.txt`

2. **"Error calling LLM API"**
   - Verify OpenAI API key is set: `echo $OPENAI_API_KEY`
   - Check API key permissions and billing

3. **"File not found"**
   - Ensure transcript file exists and path is correct
   - Try with the provided `transcript.txt` sample

### Getting Help

- Check the documentation files for detailed information
- Review the sample transcript and expected output
- Verify all prerequisites are installed correctly

## 🌟 Key Benefits

- **Time Savings:** Reduce research synthesis time from hours to minutes
- **Consistency:** Standardized presentation format and structure
- **Scalability:** Process multiple transcripts efficiently
- **Quality:** AI-powered insight extraction and theme identification
- **Integration Ready:** Foundation for enterprise-scale deployment

---

**Built for user researchers who want to focus on insights, not formatting.**