"""Response formatting for frontend integration in the RAG Chatbot application."""

from typing import Dict, Any, List
from src.models.citation import Citation


def format_query_response_for_frontend(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the query response for frontend consumption.
    
    Args:
        response_data: Raw response data from the backend services
        
    Returns:
        Formatted response data suitable for frontend consumption
    """
    formatted_response = {
        "id": response_data.get("id", ""),
        "query": response_data.get("query", ""),
        "response": response_data.get("response", ""),
        "citations": format_citations_for_frontend(response_data.get("citations", [])),
        "confidence_score": response_data.get("confidence_score", 0.0),
        "query_type": response_data.get("query_type", ""),
        "isolation_validated": response_data.get("isolation_validated", True),
        "isolation_overlap": response_data.get("isolation_overlap", 1.0)
    }
    
    return formatted_response


def format_citations_for_frontend(citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format citations for frontend consumption.
    
    Args:
        citations: List of raw citation data
        
    Returns:
        Formatted citations suitable for frontend consumption
    """
    formatted_citations = []
    
    for citation in citations:
        formatted_citation = {
            "section_title": citation.get("section_title", "Unknown Section"),
            "page_number": citation.get("page_number", 0),
            "text_snippet": citation.get("text_snippet", "")[:200] + "..."  # Truncate if too long
        }
        formatted_citations.append(formatted_citation)
    
    return formatted_citations


def format_book_info_for_frontend(book_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format book information for frontend consumption.
    
    Args:
        book_info: Raw book information data
        
    Returns:
        Formatted book info suitable for frontend consumption
    """
    formatted_book = {
        "id": book_info.get("id", ""),
        "title": book_info.get("title", ""),
        "author": book_info.get("author", ""),
        "isbn": book_info.get("isbn", ""),
        "section_count": book_info.get("section_count", 0),
        "total_pages": book_info.get("total_pages", 0),
        "created_at": book_info.get("created_at", ""),
        "updated_at": book_info.get("updated_at", "")
    }
    
    return formatted_book


def format_error_for_frontend(error_code: str, message: str, details: str = None) -> Dict[str, Any]:
    """
    Format error response for frontend consumption.
    
    Args:
        error_code: Code identifying the type of error
        message: Human-readable error message
        details: Additional error details (optional)
        
    Returns:
        Formatted error response suitable for frontend consumption
    """
    error_response = {
        "error": {
            "code": error_code,
            "message": message
        }
    }
    
    if details:
        error_response["error"]["details"] = details
    
    return error_response