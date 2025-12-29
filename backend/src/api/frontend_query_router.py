"""Frontend-compatible query API router for the RAG Chatbot application."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.services.rag_service import rag_service
from src.services.query_service import query_service
from src.models.query import QueryBase, QueryType
from src.models.database import get_async_session
from src.models import BookContent as BookContentModel
from src.utils.error_handler import handle_exception
from src.utils.security import SecurityUtils


# Create router instance
router = APIRouter()

# Request/Response models for frontend compatibility
class FrontendQueryRequest(BaseModel):
    query: str

class FrontendQueryResponse(BaseModel):
    answer: str

@router.post("/query", response_model=FrontendQueryResponse)
async def query_endpoint(
    request: FrontendQueryRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Frontend-compatible endpoint that accepts { "query": "<user message>" }
    and returns { "answer": "<bot response>" }.

    This endpoint maps the frontend format to the backend services.
    """
    try:
        # Sanitize the input query
        sanitized_query = SecurityUtils.sanitize_input(request.query)

        # Validate the query text
        is_valid, error_msg = SecurityUtils.validate_query_text(sanitized_query)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Get the first available book from the database as default
        result = await db.execute(select(BookContentModel).limit(1))
        first_book = result.scalars().first()

        if not first_book:
            # If no books are available, return a default response
            return FrontendQueryResponse(
                answer="No books are currently available in the database. Please contact the administrator to load book content."
            )
        default_book_id = first_book.id

        # Process the query using the RAG service
        rag_result = rag_service.query_full_book(
            query_text=sanitized_query,
            book_id=default_book_id,
            include_citations=True
        )

        # Store the query in the database using QueryService
        query_record = QueryBase(
            query=sanitized_query,
            response=rag_result["response"],
            query_type=QueryType.FULL_BOOK,
            book_id=default_book_id
        )
        query_service.create_query(query_record)

        return FrontendQueryResponse(
            answer=rag_result["response"]
        )
    except HTTPException:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise
    except Exception as e:
        # Handle all other exceptions with our custom error handler
        return handle_exception(e, {
            "endpoint": "/api/v1/query",
            "method": "POST",
            "request": request.dict()
        })