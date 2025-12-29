"""User-selected text isolation mechanism for the RAG Chatbot application."""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class UserSelectionIsolationService:
    """Service to ensure responses are based only on user-selected text."""
    
    def __init__(self):
        pass
    
    def isolate_context(
        self, 
        query: str, 
        selected_text: str, 
        book_content: str = None,
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        Isolate the context to only include the user-selected text.
        
        Args:
            query: The user's query
            selected_text: The text selected by the user
            book_content: Full book content (should not be used in isolation mode)
            additional_context: Any additional context (should not be used in isolation mode)
            
        Returns:
            Dictionary with isolated context and validation results
        """
        try:
            # Ensure that only the selected text is used as context
            # The book_content and additional_context should be ignored
            isolated_context = {
                "query": query,
                "context": selected_text,
                "context_type": "USER_SELECTION",
                "context_length": len(selected_text),
                "validation_passed": True,
                "message": "Context successfully isolated to user-selected text"
            }
            
            # Log the isolation for audit purposes
            logger.info(f"Context isolated for query. Selected text length: {len(selected_text)} characters")
            
            return isolated_context
            
        except Exception as e:
            logger.error(f"Error in context isolation: {str(e)}")
            return {
                "query": query,
                "context": "",
                "context_type": "USER_SELECTION",
                "context_length": 0,
                "validation_passed": False,
                "message": f"Error during context isolation: {str(e)}"
            }
    
    def validate_isolation(
        self, 
        response: str, 
        selected_text: str, 
        book_content: str = None
    ) -> Dict[str, Any]:
        """
        Validate that the response was generated only from the selected text.
        
        Args:
            response: The generated response
            selected_text: The text selected by the user
            book_content: Full book content for comparison (should not influence response)
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Check if the response contains information that's not in the selected text
            # This is a simplified check - in a real implementation, we might use more sophisticated methods
            response_words = set(response.lower().split())
            selected_text_words = set(selected_text.lower().split())
            
            # Find words in response that are not in selected text
            extra_words = response_words - selected_text_words
            
            # Calculate overlap percentage
            if len(response_words) > 0:
                overlap_percentage = 1 - (len(extra_words) / len(response_words))
            else:
                overlap_percentage = 1.0  # If response is empty, consider it valid
            
            validation_result = {
                "is_isolated": overlap_percentage > 0.7,  # Threshold for isolation
                "overlap_percentage": overlap_percentage,
                "extra_words_count": len(extra_words),
                "message": f"Response isolation validation completed. Overlap: {overlap_percentage:.2%}"
            }
            
            logger.info(f"Isolation validation completed. Overlap: {overlap_percentage:.2%}, Isolated: {validation_result['is_isolated']}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error in isolation validation: {str(e)}")
            return {
                "is_isolated": False,
                "overlap_percentage": 0.0,
                "extra_words_count": 0,
                "message": f"Error during isolation validation: {str(e)}"
            }


# Singleton instance
user_selection_isolation_service = UserSelectionIsolationService()