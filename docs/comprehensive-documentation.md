# Comprehensive Documentation: AI-Native Book with Docusaurus

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Frontend Components](#frontend-components)
4. [Backend Services](#backend-services)
5. [API Endpoints](#api-endpoints)
6. [Deployment](#deployment)
7. [Monitoring & Metrics](#monitoring--metrics)
8. [Performance](#performance)
9. [Security](#security)
10. [Troubleshooting](#troubleshooting)

## Overview

The AI-Native Book with Docusaurus is a book-first reading experience that combines static content delivery with intelligent backend services. The system provides structured book content with chapter navigation, search functionality, interactive elements, and an optional AI assistant that answers questions based only on book content.

### Key Features
- Book-like reading experience with structured navigation
- Full-text search across all content
- AI assistant for answering content-based questions
- Multi-language support (starting with Urdu)
- Responsive design for all device sizes
- Static-first architecture with optional backend intelligence

## Architecture

### Technology Stack
- **Frontend**: Docusaurus, React, JavaScript/TypeScript
- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL (Neon)
- **Vector Database**: Qdrant for semantic search
- **Content Storage**: Markdown/MDX files
- **Caching**: In-memory and browser caching

### Architecture Pattern
The system follows a static-first architecture:
- Static content delivered directly from Docusaurus
- Backend services (FastAPI) provide search, AI, and translation features
- Optional backend intelligence doesn't affect core reading experience
- Graceful degradation when backend services are unavailable

## Frontend Components

### Core Components
- `ExpandableSection`: Toggle detailed content without disrupting flow
- `VisualDiagrams`: Interactive visual representations
- `Callouts`: Highlighted information blocks
- `ContentPage`: Enhanced MDX content display
- `Search`: Full-featured search with suggestions and highlighting
- `AIAssistant`: Context-aware question answering
- `LanguageSelector`: Multi-language support

### Theme Components
- Custom Docusaurus theme for book-like UI
- Responsive design for all screen sizes
- Accessibility features
- SEO capabilities

### Performance Optimizations
- Client-side caching for search results
- Debounced search requests
- Lazy loading for AI assistant
- Preloading for navigation

## Backend Services

### Content Service
- CRUD operations for book content
- Content retrieval with metadata
- Reading progress tracking
- Content indexing for search and AI

### Search Service
- Full-text search across all content
- Relevance scoring and ranking
- Search suggestions/auto-complete
- Result highlighting
- Pagination support

### AI Assistant Service (RAG)
- Retrieval Augmented Generation for content-based answers
- Vector database integration (Qdrant)
- Source attribution for answers
- Confidence scoring
- Rate limiting (20 requests/hour per IP)

### Translation Service
- Multi-language content management
- Translation caching
- Fallback mechanisms
- RTL (right-to-left) support for Urdu

## API Endpoints

### Content API
```
GET /api/content/{content_id}     # Retrieve specific content
GET /api/content                 # List content with pagination
GET /api/toc                     # Table of contents structure
POST /api/content/reading-progress    # Save reading progress
GET /api/content/reading-progress/{session_id}  # Retrieve reading progress
```

### Search API
```
POST /api/search                 # Search across all content
```

### AI Assistant API
```
POST /api/ai-assistant           # Ask questions about book content
```

### Translation API
```
GET /api/translation/{content_id} # Get translated content
POST /api/translation            # Manage translations
```

### Health API
```
GET /api/health                  # Health check for all services
```

## Deployment

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker (for containerized deployment)
- PostgreSQL database (Neon recommended)
- Qdrant vector database

### Environment Configuration
Create `.env` files for both frontend and backend with appropriate settings:

**backend/.env:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_book
QDRANT_URL=http://localhost:6333
SECRET_KEY=your-secret-key
DEBUG=false
```

**website/.env:**
```
REACT_APP_API_URL=http://your-domain.com
```

### Deployment Options

#### Option 1: Separate Services
1. Build Docusaurus site: `npm run build` in website/
2. Deploy static files to CDN/web server
3. Deploy FastAPI backend to Python-compatible hosting

#### Option 2: Docker Compose
Use provided docker-compose.yml for containerized deployment

## Monitoring & Metrics

### Built-in Metrics
- Request rates and response times
- Error rates and types
- Cache hit/miss ratios
- Search query performance
- AI assistant usage and performance

### Health Checks
- Service connectivity verification
- Performance threshold monitoring
- Error rate tracking

### Logging
- Structured logging for all components
- Performance event logging
- Security event monitoring
- Debug information for troubleshooting

## Performance

### Performance Goals
- Page load < 2 seconds for 95% of requests
- AI responses within 5 seconds
- Search results within 3 seconds
- 99% uptime for static content delivery

### Optimization Strategies
- Static-first architecture minimizes backend dependencies
- Client-side caching reduces API calls
- CDN delivery for static assets
- Database indexing for content retrieval
- Vector database optimization for semantic search

### Performance Monitoring
- Response time tracking
- Error rate monitoring
- Resource utilization metrics
- Database query optimization

## Security

### Authentication & Authorization
- No user authentication required for core reading experience
- Rate limiting to prevent abuse
- Input validation for all API endpoints
- Secure API key management

### Data Protection
- Content-based AI responses (no external data)
- Session-based reading progress (temporary)
- Secure database connections
- Environment variable management

### API Security
- Rate limiting for search and AI endpoints
- Input sanitization
- SQL injection prevention
- XSS protection

## Troubleshooting

### Common Issues

#### Frontend Issues
- **Content not loading**: Check that MDX files are properly formatted and in the correct directory structure
- **Search not working**: Verify backend API endpoint is accessible and search index is populated
- **AI assistant not responding**: Check backend connectivity and rate limiting

#### Backend Issues
- **Database connection errors**: Verify DATABASE_URL in environment configuration
- **Qdrant connection errors**: Check QDRANT_URL in environment configuration
- **Slow search responses**: Ensure proper database indexing is in place

#### Performance Issues
- **Slow page loads**: Check CDN configuration and asset optimization
- **High API response times**: Monitor database and vector database performance
- **Memory issues**: Review caching strategies and memory usage

### Debugging Steps
1. Check application logs for error messages
2. Verify all environment variables are correctly set
3. Test API endpoints individually
4. Review performance metrics for bottlenecks
5. Check external service connectivity (database, vector DB)

### Support Resources
- Application logs in `/logs/` directory
- Performance metrics endpoint
- Health check endpoint for service status
- Configuration validation tools

## Development

### Local Development Setup
1. Clone the repository
2. Install frontend dependencies: `npm install` in website/
3. Install backend dependencies: `pip install -r requirements.txt` in backend/
4. Set up environment variables
5. Start services: backend with `uvicorn app.main:app --reload` and frontend with `npm start`

### Testing
- Frontend: Jest for unit and integration tests
- Backend: Pytest for API and service tests
- End-to-end: Integration testing for complete workflows

### Contributing
- Follow existing code patterns and style
- Update documentation for new features
- Add tests for all functionality
- Follow security best practices