"""Security utilities for the RAG Chatbot application."""

import re
from typing import Optional, Union
import html
import bleach
from pydantic import BaseModel, validator
from fastapi import HTTPException, status


class SecurityUtils:
    """Utility class for security-related functions."""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS and other injection attacks."""
        if not text:
            return text
            
        # Remove potentially dangerous characters/sequences
        # First, HTML escape the content
        text = html.escape(text)
        
        # Then use bleach to strip any remaining potentially dangerous tags
        # Allow only safe tags if any
        text = bleach.clean(text, tags=[], attributes={}, strip=True)
        
        return text
    
    @staticmethod
    def validate_book_id(book_id: str) -> bool:
        """Validate that a book ID is in a proper UUID format."""
        if not book_id:
            return False
            
        # UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(book_id))
    
    @staticmethod
    def validate_query_text(query_text: str) -> tuple[bool, Optional[str]]:
        """Validate query text for length and content."""
        if not query_text or not query_text.strip():
            return False, "Query text cannot be empty"
        
        # Check length
        if len(query_text) > 1000:  # Arbitrary limit, adjust as needed
            return False, "Query text is too long (max 1000 characters)"
        
        # Check for potentially malicious patterns
        dangerous_patterns = [
            r'<script',  # Script tags
            r'javascript:',  # JavaScript URLs
            r'on\w+\s*=',  # Event handlers
            r'<iframe',  # Iframe tags
            r'<object',  # Object tags
            r'<embed',  # Embed tags
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query_text, re.IGNORECASE):
                return False, f"Potentially dangerous content detected in query: {pattern}"
        
        return True, None
    
    @staticmethod
    def validate_selected_text(selected_text: str) -> tuple[bool, Optional[str]]:
        """Validate selected text for length and content."""
        if not selected_text or not selected_text.strip():
            return False, "Selected text cannot be empty"
        
        # Check length
        if len(selected_text) > 10000:  # Arbitrary limit, adjust as needed
            return False, "Selected text is too long (max 10000 characters)"
        
        # Check for potentially malicious patterns
        dangerous_patterns = [
            r'<script',  # Script tags
            r'javascript:',  # JavaScript URLs
            r'on\w+\s*=',  # Event handlers
            r'<iframe',  # Iframe tags
            r'<object',  # Object tags
            r'<embed',  # Embed tags
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, selected_text, re.IGNORECASE):
                return False, f"Potentially dangerous content detected in selected text: {pattern}"
        
        return True, None
    
    @staticmethod
    def sanitize_book_content(content: str) -> str:
        """Sanitize book content before storing or processing."""
        if not content:
            return content
            
        # Remove potentially dangerous content while preserving text
        content = bleach.clean(content, tags=['p', 'br', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'], 
                              attributes={}, strip=True)
        return content


# Create a security middleware function for FastAPI
async def security_middleware(request, call_next):
    """Security middleware to validate and sanitize requests."""
    # For POST requests, validate and sanitize the body content
    if request.method in ["POST", "PUT", "PATCH"]:
        # Note: In a real implementation, you'd want to be more careful about 
        # reading the body multiple times. This is a simplified example.
        try:
            body = await request.json()
            
            # Sanitize and validate fields based on endpoint
            path = request.url.path
            
            if "/query" in path and path != "/query/selection":
                # Validate full book query
                if "query" in body:
                    is_valid, error_msg = SecurityUtils.validate_query_text(body["query"])
                    if not is_valid:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_msg
                        )
                    # Sanitize the query
                    body["query"] = SecurityUtils.sanitize_input(body["query"])
                    
                if "book_id" in body:
                    if not SecurityUtils.validate_book_id(body["book_id"]):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid book ID format"
                        )
                        
            elif "/query/selection" in path:
                # Validate user selection query
                if "query" in body:
                    is_valid, error_msg = SecurityUtils.validate_query_text(body["query"])
                    if not is_valid:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_msg
                        )
                    # Sanitize the query
                    body["query"] = SecurityUtils.sanitize_input(body["query"])
                    
                if "selected_text" in body:
                    is_valid, error_msg = SecurityUtils.validate_selected_text(body["selected_text"])
                    if not is_valid:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_msg
                        )
                    # Sanitize the selected text
                    body["selected_text"] = SecurityUtils.sanitize_input(body["selected_text"])
            
            # Update the request body with sanitized content
            # Note: This is a simplified approach; in practice, you'd need to handle
            # request body replacement more carefully
        except Exception:
            # If there's an issue parsing the body, continue with the original request
            pass
    
    response = await call_next(request)
    return response


# Input validation models for Pydantic
class SecureQueryRequest(BaseModel):
    query: str
    book_id: str
    include_citations: bool = True
    
    @validator('query')
    def validate_query(cls, v):
        is_valid, error_msg = SecurityUtils.validate_query_text(v)
        if not is_valid:
            raise ValueError(error_msg)
        return SecurityUtils.sanitize_input(v)
    
    @validator('book_id')
    def validate_book_id(cls, v):
        if not SecurityUtils.validate_book_id(v):
            raise ValueError('Invalid book ID format')
        return v


class SecureSelectionQueryRequest(BaseModel):
    query: str
    selected_text: str
    include_citations: bool = False
    
    @validator('query')
    def validate_query(cls, v):
        is_valid, error_msg = SecurityUtils.validate_query_text(v)
        if not is_valid:
            raise ValueError(error_msg)
        return SecurityUtils.sanitize_input(v)
    
    @validator('selected_text')
    def validate_selected_text(cls, v):
        is_valid, error_msg = SecurityUtils.validate_selected_text(v)
        if not is_valid:
            raise ValueError(error_msg)
        return SecurityUtils.sanitize_input(v)