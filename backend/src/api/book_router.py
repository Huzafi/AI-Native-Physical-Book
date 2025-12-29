"""Book API router for the RAG Chatbot application."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from src.services.book_service import book_service
from src.utils.error_handler import handle_exception, NotFoundError

# Create router instance
router = APIRouter()

# Response models
class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    isbn: Optional[str] = None
    section_count: int
    total_pages: int
    created_at: str
    updated_at: str

# Get book information endpoint
@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book_info(book_id: str):
    try:
        book_info = book_service.get_book_info(book_id)
        if not book_info:
            raise NotFoundError("Book", book_id)

        return book_info
    except HTTPException:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise
    except Exception as e:
        # Handle all other exceptions with our custom error handler
        return handle_exception(e, {"endpoint": f"/api/v1/books/{book_id}", "method": "GET"})