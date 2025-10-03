# System Architecture
# InsightDeck Agent - Enterprise User Research Insights-to-Presentation System

## 1. Architecture Overview

InsightDeck Agent follows a modular, multi-phase architecture that evolves from a simple POC to a scalable enterprise system.

### Architecture Evolution Path
```
POC (v0.1) → MVP (v0.5) → Enterprise (v1.0)
Monolithic → Microservices → Multi-Agent Orchestration
```

## 2. POC Architecture (v0.1) - CURRENT

### System Diagram
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│ Input File  │───▶│   main.py    │───▶│ OpenAI API  │───▶│ Output File  │
│ (txt)       │    │ (Orchestrator)│    │ (GPT-4o)    │    │ (markdown)   │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Marp Formatter  │
                   │ (Local Module)  │
                   └─────────────────┘
```

### Component Details

#### Core Components
| Component | Responsibility | Technology | Location |
|-----------|---------------|------------|----------|
| **Orchestrator** | Main workflow control | Python script | `main.py` |
| **File I/O Handler** | Read input, write output | Python built-ins | `main.py` |
| **LLM Service** | AI insight extraction | OpenAI API | External service |
| **Presentation Formatter** | Marp markdown generation | Python string formatting | `main.py` |

#### Data Flow
1. **Input:** User provides transcript file path via CLI argument
2. **Processing:** Script reads file, sends content to OpenAI API
3. **Analysis:** GPT-4o extracts summary and key themes (JSON format)
4. **Formatting:** Python script converts JSON to Marp-compatible markdown
5. **Output:** Writes `presentation.md` file to local directory

### POC Limitations
- Single-threaded, synchronous processing
- No error recovery or retry logic
- Limited input validation
- No logging or monitoring
- Local file system only
- No user authentication
- No configuration management

## 3. Enterprise Architecture (v1.0) - FUTURE

### High-Level System Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   Mobile App    │    │   API Clients   │
│   (React/Vue)   │    │   (Optional)    │    │   (3rd party)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    API Gateway          │
                    │    (Auth, Rate Limit)   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Orchestration Engine  │
                    │   (Multi-Agent System)  │
                    └────────────┬────────────┘
                                 │
    ┌────────────────────────────┼────────────────────────────┐
    │                           │                           │
    ▼                           ▼                           ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Research Agent  │    │Visualization    │    │ Slide Builder   │
│ (Analysis & AI) │    │ Agent           │    │ Agent           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
    │                           │                           │
    ▼                           ▼                           ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Services   │    │  Chart Services │    │Template Services│
│ (GPT, Cohere)   │    │(Chart.js, etc) │    │ (Presenton)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Enterprise Components

#### Frontend Layer
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Web Dashboard** | React/Vue.js + TypeScript | Primary user interface |
| **Mobile App** | React Native (Optional) | Mobile access |
| **VS Code Extension** | TypeScript + VS Code API | Developer integration |

#### API Layer
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **API Gateway** | AWS API Gateway / Kong | Authentication, rate limiting, routing |
| **Authentication Service** | Auth0 / AWS Cognito | SSO, RBAC, session management |
| **File Upload Service** | AWS S3 / Azure Blob | Secure file handling |

#### Core Processing Layer
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Orchestration Engine** | Python/FastAPI + Celery | Multi-agent workflow coordination |
| **Research Agent** | Python + OpenAI/Cohere APIs | Insight extraction, analysis |
| **Visualization Agent** | Python + Chart.js/Highcharts | Data visualization generation |
| **Slide Builder Agent** | Python + Presenton API | Presentation assembly |
| **Validation Agent** | Python + Custom Rules | Quality assurance, compliance |

#### Data Layer
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Metadata Database** | PostgreSQL | User data, project metadata |
| **File Storage** | AWS S3 / Azure Blob | Document and asset storage |
| **Cache Layer** | Redis | Session data, API response caching |
| **Vector Database** | Pinecone / Weaviate | Semantic search, insight clustering |

#### Infrastructure Layer
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Container Orchestration** | Kubernetes / Docker Swarm | Service deployment, scaling |
| **Message Queue** | RabbitMQ / AWS SQS | Inter-service communication |
| **Monitoring** | Prometheus + Grafana | System monitoring, alerting |
| **Logging** | ELK Stack / Splunk | Centralized logging, audit trails |

## 4. Multi-Agent Orchestration Design

### Agent Communication Pattern
```
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Engine                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Agent Manager  │  │  State Manager  │  │  Event Bus      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
                    ▼           ▼           ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │ Research Agent  │ │Visualization    │ │ Slide Builder   │
        │                 │ │ Agent           │ │ Agent           │
        │ • Text Analysis │ │ • Chart Creation│ │ • Template Mgmt │
        │ • Theme Extract │ │ • Data Binding  │ │ • Layout Design │
        │ • Summarization │ │ • Style Config  │ │ • Export Control│
        └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Agent Workflow States
```
[Input Received] → [Research Analysis] → [Data Visualization] → [Slide Assembly] → [Validation] → [Export]
      │                    │                     │                   │              │           │
      ▼                    ▼                     ▼                   ▼              ▼           ▼
   Queued              Processing            Processing         Processing      Reviewing    Complete
```

## 5. Data Models & APIs

### Core Data Models

#### Research Project
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "user_id": "uuid",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "status": "draft|processing|completed|failed",
  "input_files": ["file_id"],
  "output_files": ["file_id"],
  "insights": {
    "summary": "string",
    "themes": ["string"],
    "sentiment": "object",
    "metadata": "object"
  }
}
```

#### Processing Job
```json
{
  "id": "uuid",
  "project_id": "uuid",
  "type": "transcription|analysis|visualization|presentation",
  "status": "queued|running|completed|failed",
  "agent": "string",
  "input": "object",
  "output": "object",
  "error": "string",
  "started_at": "timestamp",
  "completed_at": "timestamp"
}
```

### RESTful API Endpoints

#### Core Endpoints
```
POST   /api/v1/projects                 # Create new project
GET    /api/v1/projects                 # List user projects
GET    /api/v1/projects/{id}            # Get project details
PUT    /api/v1/projects/{id}            # Update project
DELETE /api/v1/projects/{id}            # Delete project

POST   /api/v1/projects/{id}/upload     # Upload input files
POST   /api/v1/projects/{id}/process    # Start processing
GET    /api/v1/projects/{id}/status     # Get processing status
GET    /api/v1/projects/{id}/output     # Download results

GET    /api/v1/templates                # List presentation templates
POST   /api/v1/templates                # Create custom template
```

## 6. Security Architecture

### Authentication & Authorization
- **SSO Integration:** SAML 2.0, OIDC support
- **RBAC:** Role-based access control (Admin, User, Viewer)
- **API Security:** JWT tokens, API key management
- **Session Management:** Secure session handling, timeout controls

### Data Protection
- **Encryption at Rest:** AES-256 for stored files and database
- **Encryption in Transit:** TLS 1.3 for all API communications
- **Data Anonymization:** PII detection and redaction capabilities
- **Audit Logging:** Comprehensive activity tracking

### Compliance
- **GDPR Compliance:** Data deletion, export capabilities
- **SOC 2 Type II:** Security controls and monitoring
- **HIPAA Ready:** Enhanced data protection for healthcare clients

## 7. Scalability & Performance

### Performance Targets
| Metric | POC | Enterprise |
|--------|-----|------------|
| Processing Time | <5 min | <2 min |
| Concurrent Users | 1 | 1,000+ |
| File Size Limit | 10 MB | 100 MB |
| API Response Time | N/A | <500ms |
| Uptime SLA | N/A | 99.9% |

### Scaling Strategy
- **Horizontal Scaling:** Kubernetes auto-scaling
- **Database Sharding:** User-based data partitioning
- **CDN Integration:** Global content delivery
- **Caching Strategy:** Multi-layer caching (Redis, CDN, Browser)

## 8. Deployment Architecture

### Development Environment
```
Local Development → Docker Compose → Local Testing
```

### Production Environment
```
GitHub → CI/CD Pipeline → Staging → Production
   │         │              │          │
   │         ▼              ▼          ▼
   │    Docker Build    K8s Deploy   K8s Deploy
   │    Unit Tests      Integration  Production
   │    Linting         Tests        Monitoring
```

### Infrastructure as Code
- **Terraform:** Infrastructure provisioning
- **Helm Charts:** Kubernetes application deployment
- **Ansible:** Configuration management
- **GitOps:** ArgoCD for deployment automation

## 9. Integration Points

### External Services
| Service Type | Options | Purpose |
|--------------|---------|---------|
| **AI Services** | OpenAI, Cohere, AWS Bedrock | Natural language processing |
| **Transcription** | Whisper, AWS Transcribe, Azure Speech | Audio to text conversion |
| **Visualization** | Chart.js, Highcharts, D3.js | Data visualization generation |
| **Presentations** | Presenton, reveal.js, Marp | Slide deck creation |
| **Storage** | AWS S3, Azure Blob, GCS | File and asset storage |
| **Monitoring** | DataDog, New Relic, Prometheus | Application monitoring |

### Enterprise Integrations
- **LDAP/Active Directory:** User management
- **SharePoint/Confluence:** Document management
- **Slack/Teams:** Notification delivery
- **Jira/Azure DevOps:** Project management

## 10. Disaster Recovery & Business Continuity

### Backup Strategy
- **Database Backups:** Daily automated backups with point-in-time recovery
- **File Backups:** Cross-region replication for uploaded files
- **Configuration Backups:** Infrastructure and application configuration versioning

### Disaster Recovery
- **RTO (Recovery Time Objective):** 4 hours
- **RPO (Recovery Point Objective):** 1 hour
- **Multi-Region Deployment:** Active-passive setup across regions
- **Automated Failover:** Health checks and automated traffic routing

This architecture provides a clear evolution path from the current POC to a fully-featured enterprise solution, maintaining modularity and scalability at each phase.