# Content API Contract

## Endpoints

### GET /api/content/{content_id}
**Description**: Retrieve specific book content by ID

**Path Parameters**:
- `content_id`: string (content identifier)

**Response (200 OK)**:
```json
{
  "id": "string (content identifier)",
  "title": "string (content title)",
  "slug": "string (URL-friendly identifier)",
  "content": "string (MDX content)",
  "chapter_number": "integer",
  "section_number": "integer",
  "parent_id": "string (optional, parent content ID)",
  "metadata": {
    "tags": "array of strings",
    "reading_time": "integer (estimated minutes)",
    "language": "string (default: 'en')"
  },
  "translations": [
    {
      "language_code": "string (e.g., 'ur' for Urdu)",
      "title": "string (translated title)",
      "content": "string (translated content)",
      "summary": "string (optional summary)"
    }
  ],
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

**Error Responses**:
- 404: Content not found
- 500: Internal server error

### GET /api/content
**Description**: List book content with pagination

**Query Parameters**:
- `page`: integer (optional, default: 1)
- `limit`: integer (optional, default: 20, max: 100)
- `chapter`: integer (optional, filter by chapter)
- `tags`: string (optional, comma-separated tags)

**Response (200 OK)**:
```json
{
  "items": [
    {
      "id": "string",
      "title": "string",
      "slug": "string",
      "chapter_number": "integer",
      "section_number": "integer",
      "url_path": "string",
      "preview": "string (content preview)",
      "tags": "array of strings",
      "reading_time": "integer"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "total_pages": "integer"
  }
}
```

### GET /api/toc
**Description**: Retrieve table of contents structure

**Response (200 OK)**:
```json
{
  "title": "string (book title)",
  "chapters": [
    {
      "id": "string",
      "number": "integer",
      "title": "string",
      "sections": [
        {
          "id": "string",
          "number": "integer",
          "title": "string",
          "url_path": "string"
        }
      ],
      "url_path": "string"
    }
  ]
}
```

### POST /api/content/reading-progress
**Description**: Save user's reading progress (temporary session)

**Request**:
```json
{
  "session_id": "string (temporary session identifier)",
  "content_id": "string (current content being read)",
  "position": {
    "chapter": "integer",
    "section": "integer",
    "paragraph": "integer (optional)",
    "percent": "number (0-100)"
  }
}
```

**Response (200 OK)**:
```json
{
  "status": "string ('saved')",
  "expires_at": "string (ISO 8601 datetime)"
}
```

### GET /api/content/reading-progress/{session_id}
**Description**: Retrieve user's reading progress

**Response (200 OK)**:
```json
{
  "position": {
    "content_id": "string",
    "chapter": "integer",
    "section": "integer",
    "paragraph": "integer (optional)",
    "percent": "number (0-100)"
  },
  "preferences": {
    "language": "string (selected language code)"
  }
}
```