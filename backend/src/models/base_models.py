"""Base Pydantic models for the RAG Chatbot application."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    FULL_BOOK = "FULL_BOOK"
    USER_SELECTION = "USER_SELECTION"


class BookContentBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    content: str


class BookContent(BookContentBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


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


class QueryBase(BaseModel):
    query_text: str
    query_type: QueryType
    user_selected_text: Optional[str] = None
    book_id: Optional[str] = None
    session_id: Optional[str] = None


class Query(QueryBase):
    id: str
    query_embedding: Optional[list] = None
    created_at: datetime


class CitationBase(BaseModel):
    response_id: str
    section_id: str
    text_snippet: str
    page_number: Optional[int] = None
    confidence: Optional[float] = None


class Citation(CitationBase):
    id: str


class ResponseBase(BaseModel):
    query_id: str
    response_text: str
    citations: Optional[List[Citation]] = []
    retrieved_chunks: Optional[List[str]] = []
    confidence_score: Optional[float] = None


class Response(ResponseBase):
    id: str
    created_at: datetime