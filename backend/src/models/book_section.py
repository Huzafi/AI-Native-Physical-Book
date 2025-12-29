"""BookSection model for the RAG Chatbot application."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookSectionBase(BaseModel):
    book_id: str
    section_title: str
    content: str
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    section_order: int
    vector_id: Optional[str] = None


class BookSection(BookSectionBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True