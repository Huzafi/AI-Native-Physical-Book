"""Custom request models for handling both frontend and full API formats."""

from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional
from src.utils.security import SecurityUtils


class FlexibleQueryRequest(BaseModel):
    """Request model that can handle both frontend format and full format."""
    query: str
    book_id: Optional[str] = None
    include_citations: Optional[bool] = True
    
    @field_validator('query')
    def validate_and_sanitize_query(cls, v):
        is_valid, error_msg = SecurityUtils.validate_query_text(v)
        if not is_valid:
            raise ValueError(error_msg)
        return SecurityUtils.sanitize_input(v)
    
    @field_validator('book_id', mode='before')
    def validate_book_id(cls, v):
        if v is None or v == "":
            return v
        if not SecurityUtils.validate_book_id(v):
            raise ValueError('Invalid book ID format')
        return v
    
    @property
    def is_full_format(self) -> bool:
        """Check if this request is in the full format (has required fields)."""
        return self.book_id is not None and self.book_id != ""


class FrontendQueryResponse(BaseModel):
    """Response model for frontend format."""
    answer: str