from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["query"])

# Request model
class QueryRequest(BaseModel):
    query: str

# Response model
class QueryResponse(BaseModel):
    answer: str
    results: List[Dict[str, Any]]

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    RAG query endpoint that searches Qdrant and generates response with Cohere
    """
    # Initialize the RAG service
    rag_service = RAGService()

    # Perform the search and generation
    result = await rag_service.search_and_generate(request.query)

    return QueryResponse(
        answer=result["answer"],
        results=result["results"]
    )

@router.get("/query/health")
async def query_health():
    """
    Health check for the query service
    """
    try:
        rag_service = RAGService()
        is_healthy = await rag_service.health_check()

        if is_healthy:
            return {"status": "healthy", "service": "query"}
        else:
            raise HTTPException(
                status_code=503,
                detail={"status": "unhealthy", "service": "query"}
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "service": "query",
                "error": str(e)
            }
        )