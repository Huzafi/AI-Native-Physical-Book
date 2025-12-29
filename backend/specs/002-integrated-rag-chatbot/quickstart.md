# Quickstart Guide: Integrated RAG Chatbot for Published Book

## Overview
This guide provides a quick setup and usage guide for the RAG chatbot API. The system allows querying book content with high accuracy and supports both full-book queries and user-selected text isolation mode.

## Prerequisites
- Python 3.11+
- Access to Cohere API (API key: provided in configuration)
- Access to Qdrant Cloud Free Tier (URL and API key provided in configuration)
- Access to Neon Serverless Postgres (connection details in configuration)

## Setup

### 1. Environment Configuration
Create a `.env` file with the following variables:
```bash
COHERE_API_KEY=hQjHRK5mE09ZcE2SkBZuXO6R1EzgjDZ4W1uoxG1a
QDRANT_URL=https://1e2951c0-86cd-480e-9cca-b040c24f65e6.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ppIAgtT0Fo6dN40_a8dpTnb6I7_qGRj6_tBs0zZts5M
NEON_DATABASE_URL=your_neon_database_url
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Usage Examples

### 1. Query Full Book Content
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main theme of this book?",
    "book_id": "book-uuid-here",
    "include_citations": true
  }'
```

### 2. Query User-Selected Text (Isolation Mode)
```bash
curl -X POST http://localhost:8000/api/v1/query/selection \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this paragraph mean?",
    "selected_text": "The paragraph of text the user has selected...",
    "include_citations": false
  }'
```

### 3. Check Health Status
```bash
curl -X GET http://localhost:8000/api/v1/health
```

## API Response Format
All successful API responses follow this structure:
```json
{
  "id": "response-uuid",
  "query": "user query text",
  "response": "generated response text",
  "citations": [
    {
      "section_title": "Chapter title",
      "page_number": 123,
      "text_snippet": "Relevant text snippet"
    }
  ],
  "confidence_score": 0.92,
  "query_type": "FULL_BOOK or USER_SELECTION"
}
```

## Error Handling
The API returns appropriate HTTP status codes and follows this error format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

## Rate Limiting
- API endpoints are rate-limited to 100 requests per minute per IP address
- Exceeding the limit returns a 429 status code

## Testing
Run the test suite to verify the installation:
```bash
pytest tests/
```

## Next Steps
1. Ingest your book content using the ingestion scripts in `scripts/`
2. Verify the API is working with the health check endpoint
3. Begin querying your book content