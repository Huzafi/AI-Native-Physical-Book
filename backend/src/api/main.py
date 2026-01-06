"""API routing and middleware structure for the RAG Chatbot application."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api import query_router, health_router, book_router
from src.api.rag_query import router as rag_query_router  # Import our new RAG query router
from src.utils.prometheus_metrics import PrometheusMiddleware, get_metrics as get_prometheus_metrics
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models to register them with Base before creating tables
from src.models import Base
from src.models.database import engine

# Create FastAPI app instance
app = FastAPI(
    title="Integrated RAG Chatbot for Published Book",
    description="API for querying book content with RAG technology",
    version="0.1.0",
)

# Add Prometheus metrics middleware first (so it wraps all other operations)
app.add_middleware(PrometheusMiddleware)

# Add CORS middleware with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],  # Allow frontend development URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods for development
    allow_headers=["*"],  # Allow all headers for development
    # In production, use more restrictive settings
)

# Import and initialize services after middleware setup
from src.services.rag_service import rag_service

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting up RAG Chatbot API...")
    try:
        # Create all database tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Verify that rag_service is properly initialized
        if rag_service:
            logger.info("RAG service initialized successfully")
        else:
            logger.error("RAG service failed to initialize")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

# Include API routers
# Include our new RAG query router which handles the /query endpoint with Qdrant and Cohere
app.include_router(rag_query_router, prefix="/api/v1", tags=["query"])
# Note: query_router and frontend_query_router are excluded since rag_query_router handles the same endpoint with better implementation
app.include_router(health_router.router, prefix="/api/v1", tags=["health"])
app.include_router(book_router.router, prefix="/api/v1", tags=["books"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Integrated RAG Chatbot API"}

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    return get_prometheus_metrics()

    