"""Health check API router for the RAG Chatbot application."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

# Create router instance
router = APIRouter()

# Response models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    dependencies: Dict[str, str]

class DependencyStatus(BaseModel):
    cohere_api: str
    qdrant: str
    neon_postgres: str

# Health check endpoint
@router.get("/health", response_model=HealthResponse)
async def health_check():
    # In a real implementation, we would check actual service connectivity
    # For now, we'll return a mock response
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        dependencies={
            "cohere_api": "connected",  # Would check actual connectivity in real implementation
            "qdrant": "connected",     # Would check actual connectivity in real implementation
            "neon_postgres": "connected"  # Would check actual connectivity in real implementation
        }
    )