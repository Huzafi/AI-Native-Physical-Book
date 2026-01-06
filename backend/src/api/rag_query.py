from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from src.services.rag_service import rag_service  # Use the src version
from src.utils.error_handler import AppException

logger = logging.getLogger(__name__)

router = APIRouter(tags=["query"])

# Request model
class QueryRequest(BaseModel):
    query: str
    book_id: str = "default_book"  # Allow book_id to be passed in request

# Response model
class QueryResponse(BaseModel):
    answer: str
    results: List[Dict[str, Any]]
    citations: List[Dict[str, Any]] = []
    confidence_score: float = 0.0

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    RAG query endpoint that searches book content and generates response
    """
    try:
        # Use the proper method from rag_service that ensures book-grounded responses
        result = rag_service.query_full_book(
            query_text=request.query,
            book_id=request.book_id,
            include_citations=True
        )

        return QueryResponse(
            answer=result.get("response", "No response generated"),
            results=[{
                "id": result.get("id", ""),
                "query_type": result.get("query_type", ""),
                "query": result.get("query", "")
            }],
            citations=result.get("citations", []),
            confidence_score=result.get("confidence_score", 0.0)
        )
    except AppException as e:
        logger.error(f"Application error in query endpoint: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Unexpected error in query endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/query/health")
async def query_health():
    """
    Health check for the query service
    """
    try:
        # Check that rag_service is properly initialized
        if rag_service and hasattr(rag_service, 'query_full_book'):
            return {"status": "healthy", "service": "query", "message": "RAG service is available"}
        else:
            logger.error("RAG service is not properly initialized")
            raise HTTPException(
                status_code=503,
                detail={"status": "unhealthy", "service": "query", "message": "RAG service not available"}
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "service": "query",
                "error": str(e),
                "message": "RAG service health check failed"
            }
        )