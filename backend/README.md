# Integrated RAG Chatbot for Published Book - Backend

This repository contains the backend implementation for an AI-powered chatbot that enables users to ask questions about published book content. The system uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on the book's content with citations to relevant sections.

## Features

- **Full Book Querying**: Ask questions about the entire book content and receive accurate answers with citations
- **User-Selected Text Isolation**: Query only specific text that the user has selected, without incorporating information from the rest of the book
- **Citation System**: Responses include citations to specific sections and page numbers for verification
- **High Accuracy**: Responses are grounded in book content with accuracy verification system
- **Scalable Architecture**: Built with serverless technologies for cost-effective scaling

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11
- **LLM Provider**: Cohere API (for generation and embeddings)
- **Vector Database**: Qdrant Cloud (Free Tier)
- **Relational Database**: Neon Serverless Postgres
- **Testing**: pytest

## API Endpoints

### Query Full Book Content
`POST /api/v1/query`

Query the entire book content for answers.

Request:
```json
{
  "query": "What is the main theme of this book?",
  "book_id": "uuid-of-the-book",
  "include_citations": true
}
```

Response:
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

### Query User-Selected Text (Isolation Mode)
`POST /api/v1/query/selection`

Query only the user-selected text without referencing the broader book content.

Request:
```json
{
  "query": "What does this paragraph mean?",
  "selected_text": "The paragraph of text the user has selected...",
  "include_citations": false
}
```

Response:
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

### Get Book Information
`GET /api/v1/books/{book_id}`

Retrieve information about a specific book.

Response:
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

### Health Check
`GET /api/v1/health`

Check the health status of the service.

## Architecture

The system follows a service-oriented architecture with the following key components:

- **Models**: Data models for book content, queries, responses, and citations
- **Services**: Business logic for RAG orchestration, embedding, generation, and content accuracy
- **API**: FastAPI endpoints with proper request/response handling
- **Configuration**: Settings for Cohere, Qdrant, and Neon Postgres
- **Utilities**: Helper functions for text processing and citation generation

## Setup

### Prerequisites
- Python 3.11+
- Access to Cohere API
- Access to Qdrant Cloud Free Tier
- Access to Neon Serverless Postgres

### Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the required environment variables

### Environment Variables
Create a `.env` file with the following variables:
```bash
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_database_url
```

### Running the Application
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Testing

Run the test suite:
```bash
pytest tests/
```

The project includes:
- Unit tests for individual components
- Integration tests for RAG pipeline and service interactions
- Contract tests for API endpoints

## Security & Privacy

- All user queries and data are handled securely
- User-selected text isolation prevents external context leakage
- API endpoints are rate-limited to prevent abuse
- No user data is stored permanently without consent