from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import logging
import time
from app.database.database import get_db
from app.services.vector_db import vector_db_service
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for backend services"""
    start_time = time.time()

    # Check database connectivity
    try:
        # Simple query to test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"

    # Check vector database connectivity
    try:
        # Try to ping the vector database
        vector_db_status = vector_db_service.health_check() if hasattr(vector_db_service, 'health_check') else "healthy"
    except Exception as e:
        logger.error(f"Vector database health check failed: {str(e)}")
        vector_db_status = "unhealthy"

    # Check AI service (RAG service) - we'll consider it healthy if it's loaded
    try:
        # Check if the RAG service is available
        ai_service_status = "healthy" if rag_service else "unhealthy"
    except Exception as e:
        logger.error(f"AI service health check failed: {str(e)}")
        ai_service_status = "unhealthy"

    # Determine overall status
    all_services = [db_status, vector_db_status, ai_service_status]
    if "unhealthy" in all_services:
        overall_status = "unhealthy"
    elif "degraded" in all_services:
        overall_status = "degraded"
    else:
        overall_status = "healthy"

    response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    return {
        "status": overall_status,
        "services": {
            "database": db_status,
            "vector_db": vector_db_status,
            "ai_service": ai_service_status
        },
        "timestamp": datetime.now().isoformat(),
        "response_time_ms": round(response_time, 2)
    }