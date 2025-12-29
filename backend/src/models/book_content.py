"""BookContent model for the RAG Chatbot application."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookContentBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    content: str


class BookContent(BookContentBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True