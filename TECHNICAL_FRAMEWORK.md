# 🏗️ Technical Framework & Architecture Overview
## InsightDeck Agent - System Design Documentation

---

## 📋 **Technology Stack Overview**

### **Current Implementation (POC)**

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[HTML5 Interface]
        B[CSS3 Styling]
        C[Vanilla JavaScript]
        D[File Upload UI]
    end
    
    subgraph "Backend Layer"
        E[Python 3.8+]
        F[Flask Web Framework]
        G[OpenAI SDK]
        H[Whisper Integration]
    end
    
    subgraph "AI Services"
        I[OpenAI GPT-4o]
        J[OpenAI Whisper]
        K[ElevenLabs STT]
    end
    
    subgraph "Storage Layer"
        L[Local File System]
        M[Temporary Storage]
        N[Output Directory]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    F --> G
    F --> H
    
    G --> I
    H --> J
    H --> K
    
    F --> L
    F --> M
    F --> N
    
    style I fill:#f3e5f5
    style J fill:#f3e5f5
    style K fill:#f3e5f5
```

### **Technology Dependencies**

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Runtime** | Python | 3.8+ | Core language |
| **Web Framework** | Flask | 2.3.0+ | HTTP server & API |
| **AI Integration** | OpenAI SDK | 1.0.0+ | GPT-4o API access |
| **Audio Processing** | Whisper | Latest | Speech-to-text |
| **Environment** | python-dotenv | 1.0.0+ | Configuration |
| **Optional Services** | ElevenLabs API | - | Enhanced transcription |
| **Optional Services** | AWS Transcribe | - | Speaker diarization |

---

## 🔄 **System Architecture Evolution**

### **Phase 1: Current POC Architecture**

```mermaid
architecture-beta
    group client(logos:chrome)[Client Layer]
    group server(logos:python)[Server Layer]
    group ai(logos:openai)[AI Layer]
    group storage(logos:files)[Storage Layer]
    
    service browser(logos:html5)[Web Browser] in client
    service flask(logos:flask)[Flask App] in server
    service processor(logos:python)[Content Processor] in server
    service gpt(logos:openai)[GPT-4o] in ai
    service whisper(logos:openai)[Whisper] in ai
    service files(logos:folder)[File System] in storage
    
    browser:R --> L:flask
    flask:R --> L:processor
    processor:R --> L:gpt
    processor:R --> L:whisper
    processor:R --> L:files
```

**Characteristics:**
- **Deployment:** Single server instance
- **Scaling:** Vertical only
- **Storage:** Local file system
- **Processing:** Synchronous, single-threaded
- **Security:** Basic file validation

### **Phase 2: MVP Architecture**

```mermaid
architecture-beta
    group frontend(logos:react)[Frontend]
    group api(logos:fastapi)[API Gateway]
    group services(logos:docker)[Microservices]
    group ai(logos:openai)[AI Services]
    group data(logos:postgresql)[Data Layer]
    
    service react(logos:react)[React UI] in frontend
    service gateway(logos:kong)[API Gateway] in api
    service auth(logos:auth0)[Auth Service] in services
    service processor(logos:python)[Processing Service] in services
    service gpt(logos:openai)[OpenAI APIs] in ai
    service postgres(logos:postgresql)[PostgreSQL] in data
    service redis(logos:redis)[Redis Cache] in data
    
    react:R --> L:gateway
    gateway:R --> L:auth
    gateway:R --> L:processor
    processor:R --> L:gpt
    processor:R --> L:postgres
    auth:R --> L:redis
```

### **Phase 3: Enterprise Architecture**

```mermaid
architecture-beta
    group clients(logos:devices)[Client Applications]
    group edge(logos:cloudflare)[Edge Layer]
    group orchestration(logos:kubernetes)[Orchestration]
    group agents(logos:ai)[AI Agent Network]
    group data(logos:database)[Data Infrastructure]
    group monitoring(logos:grafana)[Observability]
    
    service web(logos:chrome)[Web App] in clients
    service mobile(logos:mobile)[Mobile App] in clients
    service cdn(logos:cloudflare)[CDN] in edge
    service k8s(logos:kubernetes)[Kubernetes] in orchestration
    service research(logos:ai)[Research Agent] in agents
    service viz(logos:chart)[Viz Agent] in agents
    service slides(logos:presentation)[Slide Agent] in agents
    service postgres(logos:postgresql)[PostgreSQL] in data
    service vector(logos:database)[Vector DB] in data
    service metrics(logos:prometheus)[Prometheus] in monitoring
    service logs(logos:elastic)[ELK Stack] in monitoring
    
    web:R --> L:cdn
    mobile:R --> L:cdn
    cdn:R --> L:k8s
    k8s:R --> L:research
    k8s:R --> L:viz
    k8s:R --> L:slides
    research:R --> L:postgres
    viz:R --> L:vector
    k8s:R --> L:metrics
    k8s:R --> L:logs
```

---

## 🔧 **Core Components Deep Dive**

### **1. Web Application Layer (`web_app.py`)**

```mermaid
graph TB
    subgraph "Flask Application"
        A[Route Handlers]
        B[File Upload Manager]
        C[Processing Coordinator]
        D[Response Builder]
    end
    
    subgraph "API Endpoints"
        E[/process - Main processing]
        F[/transcribe_only - Transcription only]
        G[/export - Export presentations]
        H[/api/config - Configuration]
        I[/download/&lt;file&gt; - File serving]
    end
    
    subgraph "Processing Functions"
        J[transcribe_with_whisper]
        K[transcribe_with_elevenlabs]
        L[generate_markdown_content]
        M[combine_multiple_insights]
    end
    
    A --> E
    A --> F
    A --> G
    A --> H
    A --> I
    
    E --> J
    E --> K
    F --> J
    F --> K
    G --> L
    G --> M
    
    style A fill:#e1f5fe
    style J fill:#f3e5f5
    style K fill:#f3e5f5
```

### **2. Core Processing Engine (`main.py`)**

```mermaid
flowchart LR
    A[Input Validation] --> B[Content Reading]
    B --> C[LLM Processing]
    C --> D[Insight Extraction]
    D --> E[Presentation Formatting]
    E --> F[Output Generation]
    
    subgraph "AI Integration"
        G[OpenAI Client]
        H[GPT-4o Model]
        I[JSON Response Parser]
    end
    
    C --> G
    G --> H
    H --> I
    I --> D
    
    style C fill:#f3e5f5
    style D fill:#e8f5e8
```

### **3. AI Processing Pipeline**

```mermaid
sequenceDiagram
    participant User
    participant WebApp
    participant Processor
    participant OpenAI
    participant FileSystem
    
    User->>WebApp: Upload file
    WebApp->>Processor: Process request
    
    alt Audio File
        Processor->>OpenAI: Whisper transcription
        OpenAI->>Processor: Transcript text
    else Text File
        Processor->>Processor: Direct processing
    end
    
    Processor->>OpenAI: GPT-4o analysis
    OpenAI->>Processor: Insights JSON
    Processor->>Processor: Format presentation
    Processor->>FileSystem: Save output
    FileSystem->>WebApp: File path
    WebApp->>User: Download link
```

---

## 📊 **Data Flow Architecture**

### **Request Processing Flow**

```mermaid
flowchart TD
    A[User Upload] --> B{File Type Detection}
    
    B -->|Audio| C[Audio Processing Pipeline]
    B -->|Text| D[Text Processing Pipeline]
    
    subgraph "Audio Pipeline"
        C --> E[File Validation]
        E --> F{Service Selection}
        F -->|Whisper| G[Local Transcription]
        F -->|ElevenLabs| H[API Transcription]
        G --> I[Text Normalization]
        H --> I
    end
    
    subgraph "Text Pipeline"
        D --> J[Content Validation]
        J --> K[Encoding Check]
        K --> L[Format Standardization]
    end
    
    subgraph "AI Analysis"
        I --> M[GPT-4o Processing]
        L --> M
        M --> N[Theme Extraction]
        M --> O[Summary Generation]
        N --> P[Insight Validation]
        O --> P
    end
    
    subgraph "Output Generation"
        P --> Q[Presentation Builder]
        Q --> R[Format Selection]
        R --> S[File Generation]
        S --> T[Download Preparation]
    end
    
    style M fill:#f3e5f5
    style Q fill:#e8f5e8
```

### **Data Models & Schema**

```mermaid
erDiagram
    UPLOAD_SESSION {
        string session_id PK
        timestamp created_at
        string file_name
        string file_type
        integer file_size
        string processing_status
    }
    
    TRANSCRIPTION_RESULT {
        string session_id FK
        string service_used
        string language_detected
        boolean has_speakers
        integer speaker_count
        text transcript_content
        timestamp processed_at
    }
    
    AI_INSIGHTS {
        string session_id FK
        text summary
        json themes
        json metadata
        float confidence_score
        timestamp generated_at
    }
    
    PRESENTATION_OUTPUT {
        string session_id FK
        string format_type
        string file_path
        integer file_size
        string download_url
        timestamp created_at
    }
    
    UPLOAD_SESSION ||--|| TRANSCRIPTION_RESULT : contains
    UPLOAD_SESSION ||--|| AI_INSIGHTS : generates
    UPLOAD_SESSION ||--o{ PRESENTATION_OUTPUT : produces
```

---

## 🛡️ **Security & Privacy Framework**

### **Security Architecture**

```mermaid
graph TB
    subgraph "Input Security"
        A[File Type Validation]
        B[Size Limits]
        C[Malware Scanning]
        D[Content Sanitization]
    end
    
    subgraph "Processing Security"
        E[API Key Management]
        F[Request Rate Limiting]
        G[Process Isolation]
        H[Memory Management]
    end
    
    subgraph "Data Security"
        I[Temporary Storage]
        J[Auto-Deletion]
        K[Encryption at Rest]
        L[Secure Transmission]
    end
    
    subgraph "Output Security"
        M[Content Filtering]
        N[Download Tokens]
        O[Access Logging]
        P[Retention Policies]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    style A fill:#ffebee
    style E fill:#ffebee
    style I fill:#ffebee
    style M fill:#ffebee
```

### **Privacy Controls**

| Layer | Control | Implementation |
|-------|---------|---------------|
| **Input** | File validation | Whitelist file types, size limits |
| **Processing** | Data isolation | Temporary directories, process separation |
| **Storage** | Automatic cleanup | 1-hour retention, secure deletion |
| **Transmission** | Encryption | TLS 1.3 for all API calls |
| **Logging** | Minimal data | No content logging, metadata only |

---

## ⚡ **Performance Architecture**

### **Processing Performance Profile**

```mermaid
gantt
    title Processing Time Breakdown (Average 5MB audio file)
    dateFormat  SS
    axisFormat %Ss
    
    section File Upload
    Upload & Validation    :upload, 00, 10s
    
    section Transcription
    Whisper Processing     :whisper, after upload, 60s
    ElevenLabs API         :elevenlabs, after upload, 30s
    
    section AI Analysis
    GPT-4o Processing      :gpt, after whisper, 45s
    Insight Extraction     :insights, after gpt, 15s
    
    section Output
    Presentation Building  :slides, after insights, 10s
    File Generation       :files, after slides, 5s
```

### **Optimization Strategies**

```mermaid
mindmap
  root((Performance))
    Input Optimization
      File Compression
      Parallel Upload
      Progressive Processing
    Processing Optimization
      Async Operations
      Connection Pooling
      Response Caching
    AI Optimization
      Model Selection
      Prompt Engineering
      Batch Processing
    Output Optimization
      Template Caching
      CDN Distribution
      Compressed Downloads
```

---

## 🚀 **Deployment Architecture**

### **Development Environment**

```mermaid
flowchart LR
    A[Local Development] --> B[Docker Container]
    B --> C[Local Testing]
    C --> D[Git Commit]
    D --> E[CI/CD Pipeline]
    E --> F[Staging Deploy]
    F --> G[Production Deploy]
    
    subgraph "Local Setup"
        H[Python Environment]
        I[Flask Dev Server]
        J[Environment Variables]
        K[Sample Data]
    end
    
    A --> H
    A --> I
    A --> J
    A --> K
    
    style A fill:#e1f5fe
    style F fill:#fff3e0
    style G fill:#e8f5e8
```

### **Production Deployment Options**

| Environment | Technology | Pros | Cons |
|-------------|------------|------|------|
| **Local/Desktop** | Python + Flask | Simple setup, no cloud costs | Limited scaling, single user |
| **Cloud VM** | AWS EC2/GCP Compute | Easy deployment, moderate scaling | Manual management required |
| **Container Platform** | Docker + K8s | Auto-scaling, high availability | Complex setup, higher costs |
| **Serverless** | AWS Lambda/GCP Functions | Zero maintenance, pay-per-use | Cold starts, limited processing time |

---

## 📈 **Scalability Planning**

### **Scaling Dimensions**

```mermaid
radar
    title Scalability Requirements
    "Concurrent Users" : [3, 7, 9]
    "File Size" : [6, 8, 9]
    "Processing Speed" : [7, 8, 9]
    "Storage Capacity" : [4, 6, 8]
    "AI API Limits" : [5, 7, 8]
    "Geographic Distribution" : [2, 5, 8]
```

**Legend:**
- Inner ring: Current POC capabilities
- Middle ring: MVP requirements
- Outer ring: Enterprise requirements

### **Enterprise Scaling Strategy**

```mermaid
flowchart TB
    subgraph "Load Balancing"
        A[Application Load Balancer]
        B[Geographic Distribution]
        C[Auto-Scaling Groups]
    end
    
    subgraph "Microservices"
        D[Authentication Service]
        E[File Processing Service]
        F[AI Processing Service]
        G[Presentation Service]
    end
    
    subgraph "Data Layer"
        H[Primary Database]
        I[Read Replicas]
        J[Cache Layer]
        K[File Storage]
    end
    
    A --> D
    A --> E
    A --> F
    A --> G
    
    D --> H
    E --> H
    F --> I
    G --> I
    
    E --> J
    F --> J
    G --> K
    
    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
```

---

## 🔧 **Configuration Management**

### **Environment Configuration**

```yaml
# config/development.yaml
app:
  name: "InsightDeck Agent"
  version: "0.1.0"
  debug: true
  host: "127.0.0.1"
  port: 8080

ai_services:
  openai:
    model: "gpt-4o"
    max_tokens: 4000
    temperature: 0.3
  whisper:
    model: "base"
    language: "auto"
  elevenlabs:
    model: "eleven_turbo_v2_5"
    speakers: 8

storage:
  temp_dir: "/tmp/insightdeck"
  retention_hours: 1
  max_file_size: "100MB"

security:
  allowed_file_types: [".txt", ".mp3", ".wav", ".m4a"]
  max_upload_size: "100MB"
  rate_limit: "10/minute"
```

### **Feature Flags System**

```mermaid
flowchart LR
    A[User Request] --> B{Feature Flag Check}
    
    B -->|Enabled| C[New Feature Path]
    B -->|Disabled| D[Legacy Feature Path]
    B -->|Canary| E[Percentage-based Routing]
    
    E --> C
    E --> D
    
    C --> F[Feature Analytics]
    D --> G[Legacy Analytics]
    
    style B fill:#fff3e0
    style F fill:#e8f5e8
    style G fill:#e8f5e8
```

---

## 🔍 **Monitoring & Observability**

### **Monitoring Stack**

```mermaid
graph TB
    subgraph "Application Metrics"
        A[Request Count]
        B[Response Time]
        C[Error Rate]
        D[Processing Success Rate]
    end
    
    subgraph "Infrastructure Metrics"
        E[CPU Usage]
        F[Memory Usage]
        G[Disk I/O]
        H[Network Traffic]
    end
    
    subgraph "Business Metrics"
        I[Files Processed]
        J[User Satisfaction]
        K[Feature Usage]
        L[Cost per Processing]
    end
    
    subgraph "Monitoring Tools"
        M[Prometheus]
        N[Grafana]
        O[ELK Stack]
        P[AlertManager]
    end
    
    A --> M
    B --> M
    C --> M
    D --> M
    
    E --> M
    F --> M
    G --> M
    H --> M
    
    I --> O
    J --> O
    K --> O
    L --> O
    
    M --> N
    O --> N
    M --> P
    
    style M fill:#f3e5f5
    style N fill:#e8f5e8
    style O fill:#e1f5fe
    style P fill:#fff3e0
```

### **Health Check Strategy**

```mermaid
sequenceDiagram
    participant Monitor
    participant App
    participant AI_Service
    participant Storage
    
    Monitor->>App: Health check request
    App->>AI_Service: Service availability
    AI_Service->>App: Status response
    App->>Storage: Storage check
    Storage->>App: Storage status
    App->>Monitor: Overall health status
    
    alt Healthy
        Monitor->>Monitor: Continue monitoring
    else Unhealthy
        Monitor->>App: Restart/Scale
        Monitor->>Alert: Send notification
    end
```

---

## 🔄 **API Design & Integration**

### **RESTful API Structure**

```mermaid
graph LR
    subgraph "Core APIs"
        A[POST /api/v1/process]
        B[GET /api/v1/status/:id]
        C[GET /api/v1/results/:id]
        D[POST /api/v1/batch]
    end
    
    subgraph "Configuration APIs"
        E[GET /api/v1/config]
        F[POST /api/v1/config]
        G[POST /api/v1/test-services]
    end
    
    subgraph "File Management APIs"
        H[POST /api/v1/upload]
        I[GET /api/v1/download/:file]
        J[DELETE /api/v1/cleanup]
    end
    
    A --> K[Processing Engine]
    B --> L[Status Tracker]
    C --> M[Result Formatter]
    D --> N[Batch Processor]
    
    style A fill:#e1f5fe
    style K fill:#f3e5f5
```

### **Integration Patterns**

```mermaid
flowchart TB
    subgraph "Webhook Integration"
        A[External System] --> B[Webhook Endpoint]
        B --> C[Process File]
        C --> D[Send Results]
        D --> A
    end
    
    subgraph "API Integration"
        E[Client Application] --> F[REST API]
        F --> G[Authentication]
        G --> H[Processing]
        H --> I[JSON Response]
        I --> E
    end
    
    subgraph "Batch Integration"
        J[Scheduled Job] --> K[Batch Endpoint]
        K --> L[Multi-file Processing]
        L --> M[Aggregate Results]
        M --> N[Report Generation]
    end
    
    style B fill:#e8f5e8
    style F fill:#e8f5e8
    style K fill:#e8f5e8
```

---

This technical framework documentation provides comprehensive coverage of the system architecture, technology stack, and implementation details needed for UXR team presentations and technical discussions.