# API Contract: Integrated RAG Chatbot for Published Book

## Overview
This document defines the API contracts for the RAG chatbot embedded in published books. The API provides endpoints for querying book content and handling user-selected text isolation mode.

## Base URL
`/api/v1`

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Authentication
No authentication required for basic querying functionality (as per clarification in spec).

## Endpoints

### 1. Query Full Book Content
**POST** `/query`

Query the entire book content for answers.

#### Request
```json
{
  "query": "What is the main theme of this book?",
  "book_id": "uuid-of-the-book",
  "include_citations": true
}
```

#### Response (200 OK)
```json
{
  "id": "uuid-of-the-response",
  "query": "What is the main theme of this book?",
  "response": "The main theme of this book is...",
  "citations": [
    {
      "section_title": "Chapter 1: Introduction",
      "page_number": 5,
      "text_snippet": "The main theme of this book is..."
    }
  ],
  "confidence_score": 0.92,
  "query_type": "FULL_BOOK"
}
```

#### Error Responses
- `400 Bad Request`: Invalid request format
- `404 Not Found`: Book ID not found
- `500 Internal Server Error`: Processing error

### 2. Query User-Selected Text (Isolation Mode)
**POST** `/query/selection`

Query only the user-selected text without referencing the broader book content.

#### Request
```json
{
  "query": "What does this paragraph mean?",
  "selected_text": "The paragraph of text the user has selected...",
  "include_citations": false
}
```

#### Response (200 OK)
```json
{
  "id": "uuid-of-the-response",
  "query": "What does this paragraph mean?",
  "response": "This paragraph means...",
  "citations": [],
  "confidence_score": 0.85,
  "query_type": "USER_SELECTION"
}
```

#### Error Responses
- `400 Bad Request`: Missing selected_text or query
- `500 Internal Server Error`: Processing error

### 3. Health Check
**GET** `/health`

Check the health status of the service.

#### Response (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2023-12-27T10:00:00Z",
  "dependencies": {
    "cohere_api": "connected",
    "qdrant": "connected",
    "neon_postgres": "connected"
  }
}
```

### 4. Get Book Information
**GET** `/books/{book_id}`

Retrieve information about a specific book.

#### Response (200 OK)
```json
{
  "id": "uuid-of-the-book",
  "title": "Book Title",
  "author": "Author Name",
  "isbn": "978-0-123456-78-9",
  "section_count": 12,
  "total_pages": 256,
  "created_at": "2023-12-01T00:00:00Z",
  "updated_at": "2023-12-01T00:00:00Z"
}
```

#### Error Responses
- `404 Not Found`: Book ID not found
- `500 Internal Server Error`: Database error

## Common Error Format
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

## Data Types
- UUID: String in standard UUID format (e.g., "f47ac10b-58cc-4372-a567-0e02b2c3d479")
- DateTime: ISO 8601 formatted string (e.g., "2023-12-27T10:00:00Z")