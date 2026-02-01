# AI Practice Platform API Documentation

## Base URL

```
http://localhost:3847
```

## Authentication

Currently uses session-based authentication. CSRF protection is enabled for form submissions.

---

## Endpoints

### Health & Status

#### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "version": "1.0.0",
  "services": {
    "claude_api": "available",
    "database": "connected"
  },
  "stats": {
    "assessments_total": 150,
    "assessments_completed": 120,
    "assessments_in_progress": 30,
    "active_chat_sessions": 5,
    "leads_count": 200,
    "documents_generated": 450
  }
}
```

#### GET /api/status
API operational status.

**Response:**
```json
{
  "status": "operational",
  "api_version": "1.0",
  "endpoints": {
    "assessment": "/api/assessment",
    "chat": "/api/chat",
    "frameworks": "/api/frameworks",
    "documents": "/api/documents",
    "roadmap": "/api/roadmap"
  }
}
```

---

### Assessment

#### POST /start
Start a new assessment after lead capture.

**Request Body (form-data):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Contact name |
| email | string | Yes | Email address |
| organization | string | Yes | Organization name |
| title | string | No | Job title |
| sector | string | Yes | Industry sector |

**Valid Sectors:**
- general, healthcare, financial, retail, manufacturing
- technology, government, education, energy, transportation

**Response:** Redirects to `/assessment`

#### POST /submit_dimension
Submit responses for a dimension.

**Request Body (JSON):**
```json
{
  "responses": {
    "question_id_1": 4,
    "question_id_2": 3,
    "question_id_3": 5
  }
}
```

**Response:**
```json
{
  "redirect": "/assessment"  // or "/results" when complete
}
```

#### GET /api/assessment/{assessment_id}
Get assessment results by ID.

**Response:**
```json
{
  "id": "uuid",
  "lead_id": "uuid",
  "result": {
    "overall_score": 65,
    "maturity_level": "Experimenting",
    "dimension_scores": {...}
  },
  "benchmark_comparison": {...},
  "completed_at": "2024-01-15T10:30:00"
}
```

#### GET /api/questions/{sector}
Get assessment questions for a sector.

#### GET /api/benchmarks/{sector}
Get benchmark data for a sector.

---

### Chat

#### POST /api/chat/start
Start a new chat session.

**Request Body (JSON):**
```json
{
  "mode": "general"  // Options: general, assessment_guide, results_discussion, roadmap_planning, framework_builder, use_case_discovery
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "mode": "general",
  "suggested_prompts": [
    "What are the key steps to implement AI?",
    "How do I improve my data infrastructure?"
  ]
}
```

#### POST /api/chat/message
Send a chat message.

**Rate Limit:** 20 per minute

**Request Body (JSON):**
```json
{
  "message": "How should we approach AI governance?"
}
```

**Response:**
```json
{
  "response": "Based on your assessment results...",
  "suggestions": ["Follow-up question 1", "Follow-up question 2"]
}
```

#### POST /api/chat/mode
Change conversation mode.

**Request Body (JSON):**
```json
{
  "mode": "roadmap_planning"
}
```

---

### Frameworks

#### POST /api/frameworks/strategy
Generate AI Strategy Framework.

**Rate Limit:** 10 per minute

**Response:**
```json
{
  "executive_summary": "...",
  "vision": "...",
  "pillars": [...],
  "business_case": {...},
  "implementation_roadmap": {...}
}
```

#### POST /api/frameworks/governance
Generate AI Governance Framework.

#### POST /api/frameworks/ethics
Generate AI Ethics Framework.

#### POST /api/frameworks/mlops
Generate MLOps Framework.

**Request Body (JSON):**
```json
{
  "infrastructure_type": "hybrid",  // cloud, on-premise, hybrid
  "primary_cloud": "aws"  // aws, azure, gcp
}
```

#### POST /api/frameworks/data-strategy
Generate Data Strategy Framework.

**Request Body (JSON):**
```json
{
  "primary_cloud": "aws"
}
```

---

### Documents

#### POST /api/documents/generate
Generate a document.

**Rate Limit:** 5 per minute

**Request Body (JSON):**
```json
{
  "type": "executive_summary",
  "custom_requirements": "Focus on healthcare compliance"
}
```

**Document Types:**
- executive_summary
- ai_strategy
- governance_framework
- ethics_policy
- implementation_roadmap
- business_case
- use_case_portfolio
- data_strategy
- mlops_framework
- change_management

**Response:**
```json
{
  "id": "uuid",
  "title": "AI Strategy Executive Summary",
  "content": "## Executive Summary...",
  "word_count": 1500,
  "sections": ["Introduction", "Key Findings", "Recommendations"],
  "generated_at": "2024-01-15T10:30:00"
}
```

#### GET /api/documents/{doc_id}/download
Download a document.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| format | string | markdown | Export format: markdown, pdf, docx |

**Response:** File download with appropriate content type.

#### GET /api/documents/{doc_id}/export/{format}
Export document to specific format.

**Formats:** pdf, docx, markdown

---

### Roadmap

#### POST /api/roadmap/generate
Generate an AI implementation roadmap.

**Rate Limit:** 10 per minute

**Request Body (JSON):**
```json
{
  "horizon": "18 months"  // Options: 6, 12, 18, 24, 36 months
}
```

**Response:**
```json
{
  "phases": [...],
  "milestones": [...],
  "initiatives": [...],
  "dependencies": {...}
}
```

#### GET /api/roadmap/gantt
Get roadmap data in Gantt chart format.

---

### Use Cases

#### POST /api/use-cases/prioritize
Prioritize AI use cases.

**Response:**
```json
{
  "portfolio": [...],
  "prioritization_matrix": {...},
  "recommendations": [...]
}
```

---

## Error Responses

All errors return JSON with the following structure:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

**Common Error Codes:**
| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid input data |
| NO_ACTIVE_ASSESSMENT | 400 | No assessment session found |
| NO_CHAT_SESSION | 400 | No chat session found |
| NOT_FOUND | 404 | Resource not found |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| SERVER_ERROR | 500 | Internal server error |

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Default | 200/day, 50/hour |
| /start | 10/minute |
| /api/chat/message | 20/minute |
| /api/documents/generate | 5/minute |
| /api/frameworks/* | 10/minute |
| /api/analysis/ai | 10/minute |

---

## CORS

CORS is enabled for:
- Origins: `http://localhost:*`, `http://127.0.0.1:*`
- Methods: GET, POST, OPTIONS
- Headers: Content-Type, X-CSRFToken
