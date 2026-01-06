# Hugging Face Spaces Deployment Summary

## Files Created for Deployment

1. **app.py** - Entry point for the Hugging Face application
2. **Dockerfile** - Defines the container environment
3. **README.md** - Hugging Face Space configuration and documentation
4. **.env.example** - Example environment variables
5. **Procfile** - Process file for deployment platforms
6. **DEPLOYMENT_GUIDE.md** - Complete guide for deployment
7. **deploy_hf.sh** - Helper script for deployment

## Deployment Steps

1. Create a Space on Hugging Face Hub with Docker SDK
2. Clone or set up the repository
3. Copy all files from this backend directory to the Space repository
4. Set environment variables in the Space settings:
   - `COHERE_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `NEON_DATABASE_URL`
   - `QDRANT_COLLECTION_NAME` (optional)
5. Push the code to the repository
6. Monitor the Space logs for successful deployment

## Environment Variables Required

The application requires the following environment variables to function properly:

- `COHERE_API_KEY`: Your Cohere API key for embeddings and generation
- `QDRANT_URL`: Your Qdrant vector database URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `NEON_DATABASE_URL`: Your Neon PostgreSQL database connection string
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (defaults to 'book_embeddings')

## API Endpoints Available

Once deployed, the following endpoints will be available:

- `GET /` - Root endpoint with welcome message
- `POST /api/v1/query` - Query the entire book content
- `POST /api/v1/query/selection` - Query user-selected text only
- `GET /api/v1/books/{book_id}` - Get book information
- `GET /api/v1/health` - Health check endpoint
- `GET /metrics` - Prometheus metrics endpoint

## Important Notes

- The application uses external APIs that may have usage costs
- Ensure your API keys have the necessary permissions
- The application expects to run on port 7860 (as required by Hugging Face Spaces)
- CORS is configured to allow requests from localhost:3000 (for development)