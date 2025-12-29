"""User-selected text processing service for the RAG Chatbot application."""

from typing import List, Dict, Any
from src.services.user_selection_isolation_service import user_selection_isolation_service
from src.services.rag_service import rag_service
from src.models.database import SessionLocal
from src.models.query import QueryType
import logging

logger = logging.getLogger(__name__)


class SelectionService:
    """Service for processing user-selected text queries."""
    
    def __init__(self):
        pass
    
    def process_selection_query(
        self, 
        query_text: str, 
        selected_text: str, 
        include_citations: bool = False
    ) -> Dict[str, Any]:
        """
        Process a query against user-selected text only.
        
        Args:
            query_text: The user's query
            selected_text: The text selected by the user
            include_citations: Whether to include citations in the response
            
        Returns:
            Dictionary with the query response and metadata
        """
        try:
            # Validate inputs
            if not query_text or not selected_text:
                raise ValueError("Both query text and selected text are required")
            
            # Isolate the context to only include the selected text
            isolation_result = user_selection_isolation_service.isolate_context(
                query=query_text,
                selected_text=selected_text
            )
            
            if not isolation_result.get("validation_passed"):
                logger.warning(f"Context isolation failed: {isolation_result.get('message')}")
            
            # Process the query using the RAG service in selection mode
            result = rag_service.query_user_selection(
                query_text=query_text,
                selected_text=selected_text,
                include_citations=include_citations
            )
            
            # Validate that the response is properly isolated
            validation_result = user_selection_isolation_service.validate_isolation(
                response=result["response"],
                selected_text=selected_text
            )
            
            logger.info(f"Processed selection query with isolation validation: {validation_result.get('message')}")
            
            # Add isolation validation info to the result
            result["isolation_validated"] = validation_result.get("is_isolated", False)
            result["isolation_overlap"] = validation_result.get("overlap_percentage", 0.0)

            # Log the selection query operation
            logger.info(f"User Story 2 - Selection query processed: {result['id']}, Isolation validated: {result['isolation_validated']}")

            return result

        except Exception as e:
            logger.error(f"Error processing selection query: {str(e)}")
            raise e


# Singleton instance
selection_service = SelectionService()