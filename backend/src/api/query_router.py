"""Query API router for the RAG Chatbot application."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

from sqlalchemy import select

from src.services.rag_service import rag_service
from src.services.query_service import query_service
from src.utils.error_handler import handle_exception
from src.utils.security import (
    SecureQueryRequest,
    SecureSelectionQueryRequest,
)
from src.models.query import QueryBase, QueryType
from src.models.database import get_db
from src.models import BookContent as BookContentModel

# Create router instance
router = APIRouter()


# -------------------------
# Response Models
# -------------------------
class Citation(BaseModel):
    section_title: str
    page_number: int
    text_snippet: str


class QueryResponse(BaseModel):
    id: str
    query: str
    response: str
    citations: List[Citation]
    confidence_score: float
    query_type: str


# -------------------------
# Full Book Query Endpoint
# -------------------------
@router.post("/query/full", response_model=QueryResponse)
def query_full_book(
    request: SecureQueryRequest,
    db=Depends(get_db),
):
    try:
        # Fetch book from DB
        result = db.execute(
            select(BookContentModel).where(
                BookContentModel.id == request.book_id
            )
        )
        book = result.scalars().first()

        if not book:
            return QueryResponse(
                id="",
                query=request.query,
                response="The specified book is not available in the database.",
                citations=[],
                confidence_score=0.0,
                query_type=QueryType.FULL_BOOK.value,
            )

        # RAG processing
        rag_result = rag_service.query_full_book(
            query_text=request.query,
            book_id=request.book_id,
            include_citations=request.include_citations,
        )

        # Save query
        query_record = QueryBase(
            query=request.query,
            response=rag_result["response"],
            query_type=QueryType.FULL_BOOK,
            book_id=request.book_id,
        )
        query_service.create_query(query_record)

        return QueryResponse(
            id=rag_result["id"],
            query=rag_result["query"],
            response=rag_result["response"],
            citations=rag_result["citations"],
            confidence_score=rag_result["confidence_score"],
            query_type=rag_result["query_type"],
        )

    except HTTPException:
        raise
    except Exception as e:
        return handle_exception(
            e,
            {
                "endpoint": "/api/v1/query/full",
                "method": "POST",
                "request": request.dict(),
            },
        )


# -------------------------
# User Selection Query
# -------------------------
@router.post("/query/selection", response_model=QueryResponse)
def query_selection(
    request: SecureSelectionQueryRequest,
    db=Depends(get_db),
):
    try:
        rag_result = rag_service.query_user_selection(
            query_text=request.query,
            selected_text=request.selected_text,
            include_citations=request.include_citations,
        )

        query_record = QueryBase(
            query=request.query,
            response=rag_result["response"],
            query_type=QueryType.SELECTION,
            book_id=None,
        )
        query_service.create_query(query_record)

        return QueryResponse(
            id=rag_result["id"],
            query=rag_result["query"],
            response=rag_result["response"],
            citations=rag_result["citations"],
            confidence_score=rag_result["confidence_score"],
            query_type=rag_result["query_type"],
        )

    except HTTPException:
        raise
    except Exception as e:
        return handle_exception(
            e,
            {
                "endpoint": "/api/v1/query/selection",
                "method": "POST",
                "request": request.dict(),
            },
        )
