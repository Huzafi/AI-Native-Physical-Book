"""API routing and middleware structure for the RAG Chatbot application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import query_router, health_router, book_router
from app.api.rag_query import router as rag_query_router  # Import our new RAG query router
from src.utils.prometheus_metrics import PrometheusMiddleware, get_metrics as get_prometheus_metrics

# Create FastAPI app instance
app = FastAPI(
    title="Integrated RAG Chatbot for Published Book",
    description="API for querying book content with RAG technology",
    version="0.1.0",
)

# Add Prometheus metrics middleware first (so it wraps all other operations)
app.add_middleware(PrometheusMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend development URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Explicitly specify allowed methods
    allow_headers=["X-API-Key", "Content-Type", "Authorization"],  # Explicitly allowed headers
    # In production, avoid using allow_all_origins=True
)


# Include API routers
# Include our new RAG query router which handles the /query endpoint with Qdrant and Cohere
app.include_router(rag_query_router, prefix="/api/v1", tags=["query"])
app.include_router(query_router.router, prefix="/api/v1", tags=["query"])
# Note: frontend_query_router is excluded since rag_query_router handles the same endpoint with better implementation
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