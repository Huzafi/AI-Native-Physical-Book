# AI-Native Book with Docusaurus

This project implements a book-first reading experience with Docusaurus as the primary frontend technology, providing structured book content with chapter navigation, search functionality, interactive elements, and an optional AI assistant.

## Features

### Core Reading Experience
- Book-like UI with clear chapter/section hierarchy and navigation controls
- Content organized using MDX format for rich, interactive documentation
- Fast static content rendering with efficient load times
- Responsive design across all device sizes
- Proper accessibility features for readers with disabilities
- SEO capabilities for book content discoverability

### Search Functionality
- Full-text search across all book content with proper ranking
- Search result highlighting in content display
- Search suggestions/auto-complete functionality
- Search result pagination and filtering
- Search performance optimizations

### AI Assistant
- Optional AI-powered question answering that sources responses only from book content
- AI feature remains invisible during normal reading unless explicitly activated
- Source citation functionality for AI responses with proper attribution
- Confidence scoring for AI responses
- Rate limiting for AI assistant API calls
- Graceful degradation when AI service is unavailable

### Translation Support
- Optional Urdu translations and summaries as reading aids
- Language selection functionality with RTL (right-to-left) layout support for Urdu
- Fallback mechanism for untranslated content
- Translation progress tracking
- Translation caching for performance

### Interactive Elements
- Expandable sections that enhance understanding without interrupting flow
- Visual diagrams and callouts
- Smooth navigation between chapters/sections
- Reading position tracking functionality

### Architecture & Performance
- Static-first architecture with minimal backend support (FastAPI + Qdrant + Neon)
- Horizontal scaling with load balancing to handle traffic spikes
- Graceful degradation to static content when backend services fail
- Rate limiting on API calls per IP with generous limits
- 99% uptime for static content delivery

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **Python** 3.11 (Python 3.14+ has compatibility issues with FastAPI/Pydantic v1, use Python 3.11 for full functionality)
- **npm** or **yarn** package manager
- **Docker** (optional, for containerized backend services)
- **PostgreSQL** (for Neon) and **Qdrant** (vector database)

### Important Note on Python Version Compatibility

The project currently uses FastAPI with Pydantic v1, which has compatibility issues with Python 3.14+. If you're using Python 3.14 or newer, you may encounter import errors related to pydantic's model field inference. To resolve this, either:

1. Downgrade to Python 3.11 (recommended)
2. Use Docker for containerized deployment (see Docker section below)

## Complete Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Setup Frontend (Docusaurus)

```bash
cd website
npm install
```

### 3. Setup Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` files in both directories with appropriate settings:

**website/.env:**
```
REACT_APP_API_URL=http://localhost:8000
```

**backend/.env:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_book
QDRANT_URL=http://localhost:6333
SECRET_KEY=your-super-secret-and-long-random-string
DEBUG=true
```

### 5. Initialize Database

```bash
cd backend
alembic upgrade head
```

### 6. Start Services

#### Option A: Development Mode (separate terminals)

**Terminal 1: Start backend**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2: Start frontend**
```bash
cd website
npm start
```

#### Option B: Using Docker

```bash
docker-compose up --build
```

### 7. Add Book Content

1. Create MDX files in `website/docs/` directory following the chapter structure
2. Update `website/sidebars.js` to include new content in navigation
3. Run `npm run build` to rebuild the site

### 8. Index Content for Search and AI

```bash
# After adding new content, run the indexing script
cd backend
python -m scripts.index_content
```

## API Endpoints

### Content API
- `GET /api/content/{content_id}` - Retrieve specific book content by ID
- `GET /api/content/` - List book content with pagination
- `GET /api/toc` - Retrieve table of contents structure
- `POST /api/content/reading-progress` - Save user's reading progress
- `GET /api/content/reading-progress/{session_id}` - Retrieve user's reading progress

### Search API
- `POST /api/search/` - Search for content within the book
- `GET /api/search/suggest` - Get search suggestions for auto-complete
- `GET /api/search/index-all` - Index all content for search (admin endpoint)

### AI Assistant API
- `POST /api/ai-assistant/` - Ask questions about book content

### Translation API
- `POST /api/translation/` - Create a translation for content
- `GET /api/translation/{content_id}/{language_code}` - Get specific translation
- `GET /api/translation/{content_id}` - Get all translations for content
- `GET /api/translation/progress/{language_code}` - Get translation progress
- `PUT /api/translation/{content_id}/{language_code}` - Update translation
- `DELETE /api/translation/{content_id}/{language_code}` - Delete translation

### Health Check
- `GET /api/health` - Health check endpoint to verify service status

## Development Workflow

### Adding New Content
1. Create new MDX files in `website/docs/`
2. Update `website/sidebars.js` to include new content in navigation
3. Run `python -m app.services.content_indexing` to index new content for search

### Adding Translations
1. Use the translation API endpoints to add translated content
2. Translations will be available through the language selector component

### Running Tests
Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd website
npm test
```

### Running End-to-End Tests
```bash
python test_e2e.py
```

### Performance Testing
```bash
python test_performance.py
python test_ai_response_time.py
```

## Configuration

### Frontend Configuration
- `website/docusaurus.config.js` - Main Docusaurus configuration
- `website/src/css/custom.css` - Custom styling for book-like experience
- `website/sidebars.js` - Navigation structure

### Backend Configuration
- `backend/app/main.py` - Main FastAPI application
- `backend/app/config.py` - Application configuration settings
- `backend/alembic.ini` - Database migration configuration

## Deployment

### Production Deployment

#### Frontend (Static Files)
1. Build the Docusaurus site:
   ```bash
   cd website
   npm run build
   ```
2. Deploy the `build/` folder to any static hosting service (Netlify, Vercel, S3, etc.)

#### Backend (API Services)
1. Deploy the FastAPI application to any Python-compatible hosting platform
2. Ensure environment variables are properly configured
3. Set up monitoring and logging

### Docker Deployment
Use the provided `docker-compose.yml` for containerized deployment:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Monitoring and Maintenance

### Health Checks
Monitor the health of your services using the health endpoint:
```
GET /api/health
```

### Performance Monitoring
- Check the performance metrics in `/docs/performance-benchmarks.md`
- Monitor response times and error rates
- Review application logs in the `logs/` directory

### Backup and Recovery
- Database backups should be configured based on your hosting solution
- Content files (MDX) should be version controlled in Git
- Configuration files should be backed up regularly

## Troubleshooting

### Common Issues

#### Frontend Issues
- **Content not loading**: Verify that MDX files are properly formatted and in the correct directory structure
- **Search not working**: Check that the backend API is accessible and search indexing is complete
- **AI assistant not responding**: Verify backend connectivity and check rate limiting

#### Backend Issues
- **Database connection errors**: Verify DATABASE_URL in environment configuration
- **Qdrant connection errors**: Check QDRANT_URL in environment configuration
- **Slow search responses**: Ensure proper database indexing is in place

#### Performance Issues
- **Slow page loads**: Check CDN configuration and asset optimization
- **High API response times**: Monitor database and vector database performance
- **Memory issues**: Review caching strategies and memory usage

### Getting Help
- Check application logs in `/logs/` directory
- Review the health check endpoint for service status
- Consult the comprehensive documentation in `/docs/`

## Performance Goals
- Page load times under 2 seconds for 95% of requests
- AI responses within 5 seconds with 95% accuracy
- Search results within 3 seconds of query submission
- 90% of users can successfully navigate between chapters and sections
- 99% uptime for static content delivery