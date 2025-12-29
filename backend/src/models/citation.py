"""Citation model for the RAG Chatbot application."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CitationBase(BaseModel):
    response_id: str
    section_id: str
    text_snippet: str
    page_number: Optional[int] = None
    confidence: Optional[float] = None


class Citation(CitationBase):
    id: str

    class Config:
        from_attributes = True