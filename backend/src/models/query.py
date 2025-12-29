"""Query model for the RAG Chatbot application."""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    FULL_BOOK = "FULL_BOOK"
    USER_SELECTION = "USER_SELECTION"


class QueryBase(BaseModel):
    query_text: str
    query_type: QueryType
    user_selected_text: Optional[str] = None
    book_id: Optional[str] = None
    session_id: Optional[str] = None


class Query(QueryBase):
    id: str
    query_embedding: Optional[List[float]] = None
    created_at: datetime

    class Config:
        from_attributes = True