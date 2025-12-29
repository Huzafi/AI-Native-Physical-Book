"""Response model for the RAG Chatbot application."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .citation import Citation


class ResponseBase(BaseModel):
    query_id: str
    response_text: str
    citations: Optional[List[Citation]] = []
    retrieved_chunks: Optional[List[str]] = []
    confidence_score: Optional[float] = None


class Response(ResponseBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True