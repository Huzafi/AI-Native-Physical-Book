# Search API Contract

## Endpoints

### POST /api/search
**Description**: Search for content within the book

**Request**:
```json
{
  "query": "string (search query, 1-500 characters)",
  "limit": "integer (optional, default: 10, max: 50)",
  "filters": {
    "tags": "array of strings (optional)",
    "chapter": "string (optional)"
  }
}
```

**Response (200 OK)**:
```json
{
  "results": [
    {
      "id": "string (content identifier)",
      "title": "string (content title)",
      "url_path": "string (path to content)",
      "preview": "string (content preview snippet)",
      "relevance_score": "number (0-1 score)",
      "tags": "array of strings"
    }
  ],
  "total_count": "integer",
  "query_time_ms": "integer"
}
```

**Error Responses**:
- 400: Invalid request parameters
- 500: Search service unavailable

### POST /api/ai-assistant
**Description**: Ask questions about book content

**Request**:
```json
{
  "question": "string (question text, 1-1000 characters)",
  "context_content_id": "string (optional, content ID for focused answers)",
  "include_sources": "boolean (optional, default: true)"
}
```

**Response (200 OK)**:
```json
{
  "answer": "string (AI-generated answer)",
  "sources": [
    {
      "content_id": "string",
      "title": "string",
      "url_path": "string",
      "relevance_score": "number (0-1)"
    }
  ],
  "response_time_ms": "integer",
  "confidence": "number (0-1)"
}
```

**Error Responses**:
- 400: Invalid request parameters
- 429: Rate limit exceeded (per IP)
- 500: AI service unavailable

### GET /api/health
**Description**: Check health status of backend services

**Response (200 OK)**:
```json
{
  "status": "string (overall status: 'healthy', 'degraded', 'unhealthy')",
  "services": {
    "database": "string (status)",
    "vector_db": "string (status)",
    "ai_service": "string (status)"
  },
  "timestamp": "string (ISO 8601 datetime)"
}
```

## Common Error Format
```json
{
  "error": {
    "code": "string (error code)",
    "message": "string (human-readable error message)",
    "details": "object (optional, additional error details)"
  }
}
```

## Rate Limiting
- Search endpoints: 100 requests per hour per IP
- AI Assistant endpoints: 20 requests per hour per IP
- Exceeding limits returns 429 status with retry-after header