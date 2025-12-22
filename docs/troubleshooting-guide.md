# Troubleshooting Guide for AI-Native Book with Docusaurus

## Overview
This guide provides solutions to common issues that may arise when setting up, running, or maintaining the AI-Native Book application.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Frontend Issues](#frontend-issues)
3. [Backend Issues](#backend-issues)
4. [Database Issues](#database-issues)
5. [Search Functionality Issues](#search-functionality-issues)
6. [AI Assistant Issues](#ai-assistant-issues)
7. [Translation Issues](#translation-issues)
8. [Performance Issues](#performance-issues)
9. [Deployment Issues](#deployment-issues)
10. [Monitoring and Logging](#monitoring-and-logging)

## Installation Issues

### Node.js Dependencies Not Installing
**Problem**: `npm install` fails in the website directory
**Solution**:
1. Check Node.js version: `node --version` (should be v18 or higher)
2. Clear npm cache: `npm cache clean --force`
3. Delete `node_modules` and `package-lock.json`, then reinstall
4. Try using a different registry: `npm install --registry https://registry.npmjs.org/`

### Python Dependencies Not Installing
**Problem**: `pip install -r requirements.txt` fails in the backend directory
**Solution**:
1. Ensure Python 3.11 is installed: `python --version`
2. Upgrade pip: `pip install --upgrade pip`
3. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
4. Install with: `pip install --no-cache-dir -r requirements.txt`

### Environment Variables Not Loading
**Problem**: Application fails to start due to missing environment variables
**Solution**:
1. Ensure `.env` files are created in both `website/` and `backend/` directories
2. Check that file names are exactly `.env` (not `.env.txt` or similar)
3. Verify that environment variables are correctly formatted
4. Restart the application after making changes

## Frontend Issues

### Docusaurus Development Server Not Starting
**Problem**: `npm start` in website directory fails
**Solution**:
1. Check for port conflicts: `lsof -i :3000` (macOS/Linux) or `netstat -ano | findstr :3000` (Windows)
2. Kill processes using port 3000 if needed
3. Clear Docusaurus cache: `npx docusaurus clear`
4. Check `docusaurus.config.js` for syntax errors

### Content Not Loading or 404 Errors
**Problem**: Book content pages return 404 or don't load properly
**Solution**:
1. Verify MDX files are in `website/docs/` directory
2. Check that `website/sidebars.js` includes the content in navigation
3. Ensure file names and paths match the sidebar configuration
4. Restart the development server after adding new content

### Search Not Working
**Problem**: Search functionality returns no results or errors
**Solution**:
1. Verify backend server is running on port 8000
2. Check that `REACT_APP_API_URL` is set correctly in `.env`
3. Verify the search API endpoint is accessible: `GET /api/search`
4. Check browser console for CORS or network errors

### AI Assistant Not Responding
**Problem**: AI assistant interface doesn't respond or shows errors
**Solution**:
1. Verify backend server is running and AI endpoints are accessible
2. Check rate limiting - AI assistant may be temporarily unavailable
3. Verify network connectivity between frontend and backend
4. Check browser console for JavaScript errors

## Backend Issues

### FastAPI Server Not Starting
**Problem**: `uvicorn app.main:app --reload --port 8000` fails
**Solution**:
1. Check for port conflicts: `lsof -i :8000` or `netstat -ano | findstr :8000`
2. Verify Python dependencies are installed
3. Check `app/main.py` for syntax errors
4. Ensure all required environment variables are set

### Database Connection Errors
**Problem**: Application fails to connect to PostgreSQL database
**Solution**:
1. Verify `DATABASE_URL` in backend `.env` file is correct
2. Check that PostgreSQL server is running
3. Verify database credentials and permissions
4. Test connection with: `psql postgresql://user:password@host:port/dbname`

### Qdrant Connection Errors
**Problem**: Vector database operations fail with connection errors
**Solution**:
1. Verify `QDRANT_URL` in backend `.env` file
2. Check that Qdrant server is running: `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`
3. Verify network connectivity to Qdrant server
4. Check Qdrant logs for specific error messages

### API Endpoints Returning 404
**Problem**: API calls return 404 errors
**Solution**:
1. Check that the correct URL prefix is used (e.g., `/api/content/` not `/content/`)
2. Verify the application is running and endpoints are registered
3. Check for typos in endpoint URLs
4. Review the API documentation for correct endpoints

## Database Issues

### Alembic Migration Errors
**Problem**: `alembic upgrade head` fails during database setup
**Solution**:
1. Check database connection in `alembic.ini` and environment variables
2. Verify database permissions and that the database exists
3. Check if migrations are already applied: `alembic current`
4. Try running with verbose output: `alembic upgrade head --sql`

### Data Not Persisting
**Problem**: Added content or translations are lost after restart
**Solution**:
1. Verify database connection string and permissions
2. Check that transactions are being committed properly
3. Verify that the database is not in-memory only
4. Review application logs for database errors

### Slow Database Queries
**Problem**: API responses are slow due to database performance
**Solution**:
1. Check that appropriate indexes exist on frequently queried fields
2. Review slow query logs for problematic queries
3. Consider connection pooling configuration
4. Optimize queries using database explain plans

## Search Functionality Issues

### No Search Results Found
**Problem**: Search returns empty results despite content existing
**Solution**:
1. Verify content indexing is complete: check if content is in the search index
2. Check that search indexing service has run properly
3. Verify search API endpoint is receiving and processing queries
4. Check for special characters or encoding issues in content

### Search Performance Issues
**Problem**: Search queries take too long to return results
**Solution**:
1. Verify proper database indexes are in place for search fields
2. Check that search indexing is optimized
3. Consider implementing search result caching
4. Review the search algorithm and relevance scoring

### Search Suggestions Not Working
**Problem**: Auto-complete or suggestion functionality doesn't work
**Solution**:
1. Verify the suggestion endpoint is implemented and accessible
2. Check that search index includes data needed for suggestions
3. Verify frontend is making correct API calls for suggestions
4. Check for rate limiting on suggestion endpoints

## AI Assistant Issues

### AI Responses Taking Too Long
**Problem**: AI assistant responses exceed 5-second target
**Solution**:
1. Check vector database performance and indexing
2. Verify AI service connectivity and performance
3. Review prompt engineering and context window management
4. Check for rate limiting or resource constraints

### AI Responses Not Sourced Properly
**Problem**: AI responses don't include proper source attribution
**Solution**:
1. Verify RAG (Retrieval Augmented Generation) implementation
2. Check that content vectors are properly indexed in Qdrant
3. Verify source tracking in the AI response generation
4. Review the retrieval and generation pipeline

### Rate Limiting Blocking Requests
**Problem**: AI assistant returns rate limit errors
**Solution**:
1. Check the rate limit configuration in `error_handlers.py`
2. Verify the rate limit reset period
3. Consider adjusting rate limits for development vs production
4. Check if multiple requests are coming from the same IP

## Translation Issues

### Translation Not Available
**Problem**: Urdu or other translations don't appear in UI
**Solution**:
1. Verify translation API endpoints are working
2. Check that translation data exists in the database
3. Verify language selector component is properly configured
4. Check RTL (right-to-left) CSS styling for Urdu support

### RTL Layout Issues
**Problem**: Urdu content doesn't display with proper RTL layout
**Solution**:
1. Verify CSS includes RTL-specific styles
2. Check that HTML direction attributes are set correctly
3. Verify font and text rendering for Arabic/Urdu characters
4. Test layout with various text lengths and structures

### Translation Caching Problems
**Problem**: Updated translations don't appear due to caching
**Solution**:
1. Clear translation cache if using caching mechanisms
2. Verify cache invalidation logic after translation updates
3. Check cache TTL settings for translations
4. Test with cache disabled to isolate the issue

## Performance Issues

### Slow Page Load Times
**Problem**: Pages take longer than 2 seconds to load
**Solution**:
1. Enable and verify CDN configuration for static assets
2. Optimize image sizes and formats
3. Minimize and compress CSS/JS bundles
4. Check network latency between frontend and backend

### High Memory Usage
**Problem**: Application consumes excessive memory
**Solution**:
1. Review caching strategies and limits
2. Check for memory leaks in long-running processes
3. Monitor garbage collection and object lifecycle
4. Optimize data structures and algorithms

### API Response Times
**Problem**: API endpoints respond slower than expected
**Solution**:
1. Profile slow endpoints to identify bottlenecks
2. Optimize database queries and add proper indexing
3. Implement caching for frequently accessed data
4. Review third-party service dependencies

## Deployment Issues

### Production Build Fails
**Problem**: `npm run build` fails in production environment
**Solution**:
1. Check Node.js version in deployment environment
2. Verify all dependencies are available in production
3. Check environment-specific configurations
4. Review build logs for specific error messages

### Backend Not Accessible in Production
**Problem**: Frontend can't connect to backend API in production
**Solution**:
1. Verify API URL configuration in production environment
2. Check firewall and security group settings
3. Verify SSL/TLS configuration if required
4. Check CORS settings in FastAPI application

### Static Assets Not Loading
**Problem**: CSS, JS, or images don't load in production
**Solution**:
1. Verify static file serving configuration
2. Check asset paths and URL rewriting rules
3. Verify CDN configuration and cache settings
4. Check for mixed content issues (HTTP/HTTPS)

## Monitoring and Logging

### Accessing Application Logs
**Location**:
- Backend logs: Check your deployment platform's logging system
- Frontend logs: Browser developer console (F12)
- Error logs: In production, typically in `/logs/` directory

### Health Check Endpoints
**Available endpoints**:
- `/api/health` - Overall system health status
- Individual service endpoints for detailed status

### Common Log Messages
**Error codes**:
- 429: Rate limit exceeded
- 404: Resource not found
- 500: Internal server error
- 503: Service unavailable

### Performance Monitoring
**Key metrics to monitor**:
- Response times (p50, p95, p99 percentiles)
- Error rates
- Database query performance
- API endpoint usage patterns
- Resource utilization (CPU, memory)

## Getting Additional Help

If you encounter issues not covered in this guide:

1. **Check the logs**: Look for error messages and stack traces
2. **Review the documentation**: Check `/docs/` directory for detailed guides
3. **Verify configurations**: Double-check all environment variables and settings
4. **Test individually**: Test frontend and backend separately to isolate issues
5. **Contact support**: If using a hosted solution, contact your platform's support team

## Quick Reference Commands

**Frontend troubleshooting**:
```bash
cd website
npx docusaurus clear  # Clear cache
npm run build -- --debug  # Build with debug info
```

**Backend troubleshooting**:
```bash
cd backend
python -c "import sys; print(sys.version)"  # Check Python version
alembic current  # Check migration status
```

**Health checks**:
```bash
curl http://localhost:8000/api/health  # Backend health
curl http://localhost:3000  # Frontend accessibility
```

This troubleshooting guide will be updated as new issues are identified and resolved.