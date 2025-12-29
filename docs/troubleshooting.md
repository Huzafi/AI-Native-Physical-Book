# Troubleshooting Guide

This guide provides solutions for common issues you may encounter while running the AI-Native Book with Docusaurus application.

## Backend Issues

### API Server Won't Start
**Problem**: The backend server fails to start with a database connection error.

**Solution**:
1. Check that your PostgreSQL database (Neon) is running and accessible
2. Verify your database connection string in the `.env` file
3. Ensure the database credentials are correct
4. Run database migrations: `cd backend && alembic upgrade head`

### Search Service Unavailable
**Problem**: Search functionality returns 500 errors.

**Solution**:
1. Verify that Qdrant vector database is running
2. Check the Qdrant connection settings in your `.env` file
3. Re-index all content: `GET /api/search/index-all` endpoint
4. Check the backend logs for specific error messages

### AI Assistant Service Unavailable
**Problem**: AI assistant returns 500 errors or timeout.

**Solution**:
1. Check if your AI model service (OpenAI, etc.) credentials are valid
2. Verify rate limits haven't been exceeded
3. Check the backend logs for specific error messages
4. Ensure the RAG service has properly indexed content

## Frontend Issues

### Page Won't Load
**Problem**: The Docusaurus site fails to load or shows blank pages.

**Solution**:
1. Check that the backend API server is running
2. Verify the API URL in your frontend environment variables
3. Clear browser cache and try again
4. Check browser console for specific error messages

### Translation Content Not Loading
**Problem**: Translation content is not displaying when language is changed.

**Solution**:
1. Verify that translations exist for the requested content and language
2. Check the API endpoint `/api/translation/{content_id}/{language_code}` directly
3. Ensure the translation service is working properly
4. Check for CORS issues if frontend and backend are on different ports

### Search Not Working
**Problem**: Search returns no results or errors.

**Solution**:
1. Verify that content has been indexed by calling `/api/search/index-all`
2. Check that the search index is properly populated
3. Ensure the search API endpoint is accessible
4. Check browser console for network errors

## Performance Issues

### Slow Page Load Times
**Problem**: Pages take longer than 2 seconds to load.

**Solution**:
1. Check if backend services are responding slowly
2. Verify database connection performance
3. Ensure static assets are properly cached
4. Consider CDN setup for static content delivery

### Slow Search Results
**Problem**: Search queries take longer than 3 seconds.

**Solution**:
1. Optimize database queries
2. Ensure proper indexing on search fields
3. Check Qdrant performance if using vector search
4. Consider caching frequently searched terms

### Slow AI Responses
**Problem**: AI assistant responses take longer than 5 seconds.

**Solution**:
1. Check AI model service response times
2. Verify that content chunks are properly sized
3. Consider implementing response caching for common questions
4. Check rate limits on the AI service

## Common Error Messages

### 404 Errors
- **Content not found**: Verify the content exists in the database
- **API endpoint not found**: Check that the backend server is running and the endpoint is correct

### 429 Errors (Rate Limiting)
- **Too many requests**: The application implements rate limiting per IP
- **AI assistant rate limit**: Requests are limited to prevent abuse
- **Solution**: Wait for the rate limit to reset or adjust the limits in configuration

### 500 Errors (Internal Server Error)
- **Database connection issues**: Check database availability and credentials
- **External service errors**: Verify third-party service availability (AI models, etc.)
- **Check logs**: Look at backend logs for specific error details

## Debugging Tips

### Enable Detailed Logging
Set the logging level to DEBUG in your `.env` file:
```
LOG_LEVEL=DEBUG
```

### Check API Endpoints Directly
Use tools like curl or Postman to test API endpoints directly:
```bash
curl -X GET http://localhost:8000/api/content/toc
curl -X POST http://localhost:8000/api/search -d '{"query": "test"}'
```

### Frontend Console
Check the browser developer tools console for JavaScript errors and network issues.

### Backend Logs
Monitor backend logs for errors and performance issues:
```bash
cd backend
uvicorn app.main:app --reload --log-level debug
```

## Environment-Specific Issues

### Development Environment
- Ensure both frontend and backend are running simultaneously
- Check port conflicts (frontend: 3000, backend: 8000 by default)
- Clear browser cache frequently during development

### Production Environment
- Ensure proper SSL certificates for HTTPS
- Verify CDN configuration for static assets
- Monitor resource usage and scale as needed
- Check firewall and security group settings

## When to Seek Help

Contact the development team if you encounter:
- Persistent database connection issues
- Problems with deployment configuration
- Performance issues that can't be resolved with optimization
- Security-related concerns