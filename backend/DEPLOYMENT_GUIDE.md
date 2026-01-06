# Deployment Guide: Hugging Face Spaces

This guide explains how to deploy the Integrated RAG Chatbot backend to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account
2. Git installed locally
3. The Hugging Face Hub CLI (optional but recommended): `pip install huggingface_hub`

## Deployment Methods

### Method 1: Using Git (Recommended for beginners)

1. **Create a new Space on Hugging Face**:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose:
     - SDK: Docker
     - License: MIT (or your preferred license)
     - Hardware: Choose based on your needs (note that this application uses external APIs)
   - Click "Create Space"

2. **Clone your Space repository**:
   ```bash
   git clone https://huggingface.co/spaces/[your-username]/[your-space-name]
   cd [your-space-name]
   ```

3. **Copy the prepared files**:
   - Copy all files from this directory to your cloned repository:
     - `app.py`
     - `Dockerfile`
     - `requirements.txt`
     - `Procfile`
     - `.env.example`
     - All other files in the backend directory

4. **Set up environment variables**:
   - In your Space settings on Hugging Face, add the following environment variables:
     - `COHERE_API_KEY`: Your Cohere API key
     - `QDRANT_URL`: Your Qdrant URL
     - `QDRANT_API_KEY`: Your Qdrant API key
     - `NEON_DATABASE_URL`: Your Neon database URL
     - `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection to use (default: book_embeddings)

5. **Commit and push**:
   ```bash
   git add .
   git commit -m "Initial deployment of RAG Chatbot backend"
   git push origin main
   ```

6. **Monitor the deployment**:
   - Check the Space logs on Hugging Face to ensure the application starts correctly

### Method 2: Using Hugging Face Hub CLI

1. **Install the CLI**:
   ```bash
   pip install huggingface_hub
   ```

2. **Login to Hugging Face**:
   ```bash
   huggingface-cli login
   ```

3. **Create or use an existing Space repository**:
   - Either create a new Space on the Hugging Face website
   - Or use an existing repository

4. **Upload all files**:
   ```bash
   # From the backend directory
   huggingface-cli upload [your-username]/[your-space-name] ./* --repo-type space
   ```

5. **Set environment variables**:
   - Go to your Space settings on Hugging Face
   - Add the required environment variables as mentioned above

### Method 3: Direct upload through Hugging Face interface

1. **Go to your Space repository** on Hugging Face
2. **Click "Add file" → "Upload files"**
3. **Upload all the necessary files**:
   - `app.py`
   - `Dockerfile`
   - `requirements.txt`
   - `Procfile`
   - `.env.example`
   - All other source files
4. **Set environment variables** in Space settings

## Important Notes

- The application uses external APIs (Cohere, Qdrant, Neon) which may have usage limits and costs
- Make sure to secure your API keys and never expose them publicly
- The Dockerfile is configured to run on port 7860, which is required for Hugging Face Spaces
- The application expects environment variables to be set for the various API keys and database connections

## Verification

Once deployed:
1. Check that the Space is running without errors in the logs
2. Verify that the API is accessible by visiting the Space URL
3. Test the health endpoint: `GET /api/v1/health`
4. Test the root endpoint: `GET /`

## Troubleshooting

- If the Space fails to build, check the build logs for errors
- If the application crashes, check the runtime logs
- Make sure all required environment variables are set
- Verify that your API keys have the necessary permissions

## API Documentation

The API endpoints are documented in the main README.md file in this repository.

## Security Considerations

- Never commit actual API keys to the repository
- Use environment variables for all sensitive information
- Consider implementing authentication for your endpoints in production
- The current CORS settings allow localhost:3000 for development - adjust for production as needed