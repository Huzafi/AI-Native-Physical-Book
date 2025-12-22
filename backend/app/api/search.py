from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging
from app.database.database import get_db
from app.services.search_service import search_service
from app.middleware.error_handlers import search_rate_limit

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", tags=["search"])
@search_rate_limit  # Apply rate limiting
async def search_content(
    request: Request,
    query: str = Query(..., min_length=1, max_length=500),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    filters: Dict[str, Any] = None,
    include_highlights: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Search for content within the book"""
    try:
        # Perform search
        results = search_service.search(
            db=db,
            query=query,
            limit=limit,
            offset=offset,
            filters=filters or {},
            include_highlights=include_highlights
        )

        # Calculate total count (in a real implementation, this would be separate)
        total_count = search_service.get_total_search_count(db, query, filters or {})

        # Return results in the expected format with proper ranking
        return {
            "results": results,
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "query_time_ms": 10  # Placeholder - would measure actual time in real implementation
        }
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search service unavailable")

@router.get("/index-all", tags=["search"])
async def index_all_content(db: Session = Depends(get_db)):
    """Index all content for search (admin endpoint)"""
    try:
        indexed_count = search_service.index_all_content(db)
        return {
            "status": "success",
            "indexed_count": indexed_count
        }
    except Exception as e:
        logger.error(f"Index all error: {str(e)}")
        raise HTTPException(status_code=500, detail="Indexing service unavailable")


@router.get("/suggest", tags=["search"])
@search_rate_limit  # Apply rate limiting
async def get_search_suggestions(
    request: Request,
    q: str = Query(..., min_length=1, max_length=50),
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """Get search suggestions for auto-complete"""
    try:
        if not q or len(q.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Get suggestions from search service
        suggestions = search_service.get_suggestions(
            db=db,
            query=q,
            limit=limit
        )

        return {
            "query": q,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
    except Exception as e:
        logger.error(f"Search suggestions error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search suggestions service unavailable")