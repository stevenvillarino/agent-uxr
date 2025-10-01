# Product Features
# InsightDeck Agent - Feature Specifications

## 1. Feature Overview

InsightDeck Agent delivers AI-powered research-to-presentation automation through a phased feature rollout from POC to Enterprise.

## 2. POC Features (v0.1) - CURRENT IMPLEMENTATION

### F-01: Text File Input
**Priority:** P0 (Critical)  
**Status:** ✅ Implemented  

**Description:** Accept and validate research transcript text files via command-line interface.

**Specifications:**
- **Input Format:** `.txt` files only
- **File Size Limit:** 10MB maximum
- **Encoding:** UTF-8 support
- **Validation:** File existence and readability checks

**Usage:**
```bash
python main.py transcript.txt
```

**Acceptance Criteria:**
- [ ] Accept valid .txt files
- [ ] Display clear error messages for invalid files
- [ ] Handle files up to 10MB
- [ ] Support UTF-8 encoded text

---

### F-02: AI Insight Extraction
**Priority:** P0 (Critical)  
**Status:** ✅ Implemented  

**Description:** Use OpenAI GPT-4o to automatically extract summary and key themes from research transcripts.

**Specifications:**
- **AI Model:** GPT-4o via OpenAI API
- **Output Format:** JSON with `summary` and `themes` fields
- **Theme Count:** 3-5 key themes per transcript
- **Processing Time:** <5 minutes per file

**AI Prompt Strategy:**
```
You are an expert user research analyst. Extract:
1. A concise summary (2-3 sentences)
2. Top 3-5 key themes as bullet points
Return as JSON: {"summary": "...", "themes": ["..."]}
```

**Acceptance Criteria:**
- [ ] Generate coherent summary under 100 words
- [ ] Extract 3-5 distinct themes
- [ ] Return valid JSON format
- [ ] Handle API errors gracefully

---

### F-03: Marp Presentation Generation
**Priority:** P0 (Critical)  
**Status:** ✅ Implemented  

**Description:** Convert AI-extracted insights into a structured Markdown presentation file compatible with Marp.

**Specifications:**
- **Output Format:** Markdown (.md) with Marp front-matter
- **Slide Structure:** Title → Summary → Key Themes
- **Template:** Default Marp theme
- **File Output:** `presentation.md` in current directory

**Generated Structure:**
```markdown
---
marp: true
theme: default
---

# [Project Title]

---

## Executive Summary
[AI-generated summary]

---

## Key Themes
1. [Theme 1]
2. [Theme 2]
...
```

**Acceptance Criteria:**
- [ ] Generate valid Marp markdown
- [ ] Include proper front-matter
- [ ] Structure slides logically
- [ ] Output readable presentation file

## 3. MVP Features (v0.5) - NEXT PHASE

### F-10: Audio File Transcription
**Priority:** P0 (Critical)  
**Status:** ✅ Implemented (Dual Engine Support)

**Description:** Accept audio files and convert to text using OpenAI Whisper or ElevenLabs Speech-to-Text.

**Specifications:**
- **Input Formats:** MP3, WAV, M4A, MP4
- **File Size Limit:** 100MB maximum
- **Transcription Services:** 
  - OpenAI Whisper API (standard transcription)
  - ElevenLabs Speech-to-Text (with speaker diarization)
- **Language Support:** Auto-detect, 50+ languages
- **Processing Time:** <10 minutes per hour of audio

**Current Implementation:**
```python
# Dual transcription support in web_app.py
def transcribe_with_elevenlabs(audio_file_path, enable_diarization=True):
    # ElevenLabs API with speaker separation
    
def transcribe_audio_whisper(audio_file_path):
    # OpenAI Whisper transcription
```

**Service Selection:**
- Users can choose between Whisper and ElevenLabs via web interface
- ElevenLabs provides speaker diarization ("who said what")
- Whisper provides fast, accurate basic transcription

**Acceptance Criteria:**
- [x] Support major audio formats
- [x] Dual transcription engine support
- [x] Speaker diarization with ElevenLabs
- [x] Service selection in web interface
- [x] Error handling for both services

---

### F-11: Enhanced Presentation Templates
**Priority:** P1 (High)  
**Status:** 🔄 Planned  

**Description:** Multiple presentation template options with improved styling and layout.

**Specifications:**
- **Template Options:** Professional, Academic, Creative, Minimal
- **Customization:** Logo insertion, color schemes, fonts
- **Export Formats:** Marp MD, HTML, PDF preview
- **Brand Guidelines:** Template compliance checking

**Template Structure:**
- Executive Summary slide
- Individual theme slides with supporting quotes
- Conclusion and recommendations slide
- Appendix with full transcript (optional)

---

### F-12: Web Interface
**Priority:** P1 (High)  
**Status:** ✅ Implemented  

**Description:** Full-featured web-based interface for file upload, service selection, and presentation generation.

**Current Implementation:**
- **Technology:** Flask + HTML/CSS/JavaScript
- **Features:** 
  - Drag-and-drop file upload (text and audio files)
  - Service selection (Whisper vs ElevenLabs)
  - Speaker diarization toggle
  - Real-time processing status
  - Download results functionality
  - API key configuration panel
  - Live session support with WebSocket
- **Responsive Design:** Mobile-friendly interface
- **Built-in Settings:** OpenAI and ElevenLabs API key management

**Available Features:**
- File upload interface with format validation
- Dual transcription engine selection
- Progress tracking during processing
- Downloadable presentation and transcript results
- Settings panel for API configuration
- Demo mode for testing without API keys
- Live audio session interface

**File Structure:**
```
templates/
├── index.html          # Main upload interface
├── settings.html       # API configuration
├── live_session.html   # Real-time audio processing
```

## 4. Enterprise Features (v1.0) - FUTURE VISION

### F-20: Multi-Agent Orchestration System
**Priority:** P0 (Critical)  
**Status:** 📋 Backlog  

**Description:** Coordinated AI agents working together to process research data through specialized workflows.

**Agent Architecture:**
- **Research Analyst Agent:** Insight extraction, theme clustering
- **Data Visualization Agent:** Chart generation, infographic creation  
- **Slide Builder Agent:** Template application, layout optimization
- **Quality Validator Agent:** Accuracy checking, compliance verification

**Orchestration Features:**
- **Parallel Processing:** Multiple agents working simultaneously
- **State Management:** Shared context and progress tracking
- **Error Recovery:** Automatic retry and fallback mechanisms
- **Human-in-the-Loop:** Approval gates and manual overrides

---

### F-21: Advanced Data Visualization
**Priority:** P0 (Critical)  
**Status:** 📋 Backlog  

**Description:** Automatically generate data visualizations based on research insights and themes.

**Visualization Types:**
- **Theme Clustering:** Network diagrams showing theme relationships
- **Sentiment Analysis:** Emotional journey maps and sentiment trends
- **Participant Journey:** Flow diagrams and user story maps
- **Quantitative Charts:** Bar charts, pie charts for coded responses

**Technology Stack:**
- **Chart Libraries:** Chart.js, Highcharts, D3.js
- **AI-Powered Selection:** Automatic chart type recommendation
- **Interactive Elements:** Hover states, filtering, drill-down
- **Export Options:** PNG, SVG, interactive HTML

---

### F-22: Speaker Diarization & Attribution
**Priority:** P1 (High)  
**Status:** ✅ Partially Implemented (ElevenLabs) / 📋 Enhanced Features Backlog

**Description:** Identify and separate different speakers in research sessions, attributing quotes and insights to specific participants.

**Current Implementation:**
- ✅ **ElevenLabs Integration:** Speaker diarization available through ElevenLabs Speech-to-Text API
- ✅ **Service Selection:** Users can choose ElevenLabs for speaker separation in web interface
- ✅ **API Integration:** Built-in support for ElevenLabs eleven_turbo_v2_5 model with diarization

**Current Capabilities:**
```python
# Already implemented in web_app.py
def transcribe_with_elevenlabs(audio_file_path, enable_diarization=True):
    # Uses ElevenLabs API with speaker diarization
    # Returns transcript with speaker labels
```

**Available Now:**
- **ElevenLabs STT:** Commercial API with built-in speaker diarization
- **Speaker Labels:** Automatic speaker detection and labeling
- **Web Interface:** Toggle diarization on/off in settings
- **API Configuration:** Built-in ElevenLabs API key management

**Future Enhancements (Backlog):**
- **Multi-Service Support:** AWS Transcribe, Azure Speech Services integration
- **Advanced Attribution:** Link insights back to specific speakers
- **Privacy Controls:** Speaker anonymization options
- **Enhanced Analysis:** Speaker-specific sentiment and theme analysis

**Additional Service Options (Future):**
- **AWS Transcribe:** Built-in speaker diarization, identifies speakers as "Speaker 1", "Speaker 2", etc.
- **Azure Speech Services:** Similar speaker separation capabilities
- **pyannote-audio:** Open-source diarization library (requires additional setup)
- **AssemblyAI:** Commercial API with speaker diarization

**Implementation Approach:**
```python
# AWS Transcribe example
import boto3

def transcribe_with_diarization(audio_file):
    transcribe = boto3.client('transcribe')
    # Configure job with speaker_identification=True
    # Returns transcript with speaker labels
    return diarized_transcript
```

**Specifications:**
- **Service Integration:** AWS Transcribe, Azure Speech Services
- **Speaker Identification:** Automatic speaker detection and labeling
- **Quote Attribution:** Link insights back to specific speakers
- **Privacy Controls:** Speaker anonymization options

**Current Limitation:**
OpenAI Whisper (our current transcription service) only provides:
- ✅ Excellent speech-to-text transcription
- ❌ No speaker separation/identification

**Output Enhancements (Future):**
- Speaker-specific insight extraction
- Participant journey mapping
- Demographic-based theme clustering
- Individual vs. group sentiment analysis

**Technical Requirements:**
```
AWS Configuration:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY  
- AWS_REGION

Azure Configuration:
- AZURE_SPEECH_KEY
- AZURE_SPEECH_REGION
```

---

### F-23: Enterprise Template Management
**Priority:** P1 (High)  
**Status:** 📋 Backlog  

**Description:** Corporate branding and template management system for standardized presentation outputs.

**Features:**
- **Brand Asset Management:** Logo, colors, fonts, layouts
- **Template Library:** Departmental and project-specific templates
- **Compliance Checking:** Brand guideline enforcement
- **Version Control:** Template versioning and rollback capabilities

---

### F-24: Collaboration & Workflow Integration
**Priority:** P1 (High)  
**Status:** 📋 Backlog  

**Description:** Multi-user collaboration features and integration with enterprise workflow tools.

**Collaboration Features:**
- **Real-time Editing:** Multiple users editing presentations simultaneously
- **Comment & Review:** Stakeholder feedback and approval workflows
- **Version History:** Track changes and revert to previous versions
- **Role-based Access:** Viewer, Editor, Admin permission levels

**Workflow Integrations:**
- **Slack/Teams:** Notification delivery and bot commands
- **Jira/Azure DevOps:** Project tracking and task management
- **SharePoint/Confluence:** Document management and publishing
- **Calendar Integration:** Automated presentation scheduling

---

### F-25: Advanced AI Capabilities
**Priority:** P2 (Medium)  
**Status:** 📋 Backlog  

**Description:** Enhanced AI features using multiple models and specialized capabilities.

**AI Enhancements:**
- **Emotional Intelligence:** Cohere AI for sentiment and emotion analysis
- **Multi-language Support:** Translation and cross-language analysis
- **Bias Detection:** Identify and flag potential research biases
- **Recommendation Engine:** Suggest follow-up research questions

**Model Integration:**
- **OpenAI GPT-4:** Primary text analysis and summarization
- **Cohere:** Emotional intelligence and sentiment analysis
- **Anthropic Claude:** Alternative analysis and fact-checking
- **Open-source Models:** Local deployment options for sensitive data

---

### F-26: Enterprise Security & Compliance
**Priority:** P0 (Critical)  
**Status:** 📋 Backlog  

**Description:** Enterprise-grade security, audit trails, and compliance features.

**Security Features:**
- **SSO Integration:** SAML, OIDC, Active Directory
- **Data Encryption:** End-to-end encryption for files and communications
- **Access Controls:** Fine-grained permissions and data governance
- **Audit Logging:** Comprehensive activity tracking and reporting

**Compliance Support:**
- **GDPR:** Data deletion, export, and consent management
- **HIPAA:** Healthcare data protection and controls
- **SOC 2:** Security controls and monitoring
- **Industry Standards:** Configurable compliance frameworks

## 5. Integration Features

### F-30: API & Webhook System
**Priority:** P1 (High)  
**Status:** 📋 Backlog  

**Description:** RESTful API and webhook system for third-party integrations.

**API Features:**
- **RESTful Endpoints:** Full CRUD operations for projects and presentations
- **Webhook Support:** Real-time notifications for processing events
- **Rate Limiting:** API usage controls and quotas
- **Documentation:** Interactive API documentation (Swagger/OpenAPI)

**Integration Examples:**
- Automated processing from research tools (Maze, UserTesting)
- CRM integration for stakeholder presentation delivery
- Analytics platform data enrichment
- Custom workflow automation

---

### F-31: Analytics & Reporting Dashboard
**Priority:** P2 (Medium)  
**Status:** 📋 Backlog  

**Description:** Usage analytics and research insights reporting for research operations teams.

**Analytics Features:**
- **Usage Metrics:** Processing volume, user adoption, feature usage
- **Quality Metrics:** Accuracy scores, user satisfaction ratings
- **Research Insights:** Cross-project theme clustering, trend analysis
- **Performance Monitoring:** Processing times, error rates, system health

**Reporting Capabilities:**
- **Executive Dashboards:** High-level KPIs and success metrics
- **Operational Reports:** Detailed usage and performance analytics
- **Research Insights:** Meta-analysis across all research projects
- **Custom Reports:** Configurable reporting for specific needs

## 6. Feature Roadmap Timeline

### Phase 1: POC (Q4 2025) ✅ Complete
- [x] Text file input processing
- [x] OpenAI GPT-4o insight extraction
- [x] Marp presentation generation
- [x] Basic error handling and CLI interface
- [x] Web-based interface with file upload
- [x] Audio transcription (Whisper + ElevenLabs)
- [x] Speaker diarization (ElevenLabs)
- [x] Service selection and API key management
- [x] Live session support with WebSocket

### Phase 2: MVP (Q1 2026)
- [x] Audio transcription (Whisper integration) ✅ Already Complete
- [ ] Enhanced presentation templates
- [x] Web interface ✅ Already Complete
- [ ] Improved error handling and logging
- [ ] User authentication and session management

### Phase 3: Enterprise Core (Q2 2026)
- [ ] Multi-agent orchestration system
- [ ] Advanced data visualization
- [ ] Speaker diarization and attribution
- [ ] Enterprise template management

### Phase 4: Enterprise Complete (Q3-Q4 2026)
- [ ] Collaboration and workflow integration
- [ ] Advanced AI capabilities (Cohere, multi-model)
- [ ] Enterprise security and compliance
- [ ] API and webhook system
- [ ] Analytics and reporting dashboard

## 7. Success Metrics

### POC Metrics
- **Functionality:** 100% successful processing of test transcripts
- **Quality:** Generated presentations require <20% manual editing
- **Performance:** <5 minute processing time per transcript
- **Usability:** <5 minute setup and first-use experience

### Enterprise Metrics
- **Adoption:** 80% of research team actively using the system
- **Efficiency:** 75% reduction in research-to-presentation time
- **Quality:** 90% user satisfaction with generated presentations
- **Scale:** Support for 1000+ concurrent users
- **Reliability:** 99.9% uptime SLA compliance

This feature specification provides a comprehensive roadmap from the current POC to a full enterprise solution, with clear priorities and implementation phases.