"""Content accuracy verification system for the RAG Chatbot application."""

from typing import List, Dict, Any
from src.config.cohere_config import rerank_documents
import logging

logger = logging.getLogger(__name__)


class ContentAccuracyService:
    """Service to ensure responses are grounded in book content."""
    
    def __init__(self):
        pass
    
    def verify_response_accuracy(
        self, 
        query: str, 
        response: str, 
        source_chunks: List[str], 
        threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Verify that the response is grounded in the provided source chunks.
        
        Args:
            query: The original query
            response: The generated response
            source_chunks: List of source chunks used to generate the response
            threshold: Minimum relevance score to consider the response accurate
            
        Returns:
            Dictionary with verification results
        """
        try:
            # Use Cohere's rerank to check relevance of source chunks to the response
            reranked_results = rerank_documents(query, source_chunks, top_n=len(source_chunks))
            
            # Calculate average relevance score
            total_score = sum([result.relevance_score for result in reranked_results])
            avg_score = total_score / len(reranked_results) if reranked_results else 0
            
            # Check if the response is grounded in the sources
            is_accurate = avg_score >= threshold
            
            # Identify which chunks were most relevant
            relevant_chunks = [
                {
                    "text": source_chunks[result.index],
                    "relevance_score": result.relevance_score
                }
                for result in reranked_results
                if result.relevance_score >= threshold
            ]
            
            verification_result = {
                "is_accurate": is_accurate,
                "accuracy_score": avg_score,
                "threshold": threshold,
                "relevant_chunks": relevant_chunks,
                "message": f"Response is {'accurate' if is_accurate else 'not accurate'} based on source content"
            }
            
            logger.info(f"Content accuracy verification completed. Score: {avg_score}, Accurate: {is_accurate}")
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Error in content accuracy verification: {str(e)}")
            # In case of error, we'll be conservative and mark as not accurate
            return {
                "is_accurate": False,
                "accuracy_score": 0.0,
                "threshold": threshold,
                "relevant_chunks": [],
                "message": f"Error during accuracy verification: {str(e)}"
            }
    
    def validate_citations(
        self, 
        response: str, 
        citations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate that citations in the response are supported by actual content.
        
        Args:
            response: The generated response
            citations: List of citations to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            valid_citations = []
            invalid_citations = []
            
            for citation in citations:
                # Check if the citation's text snippet appears in the response
                text_snippet = citation.get('text_snippet', '')
                if text_snippet and text_snippet in response:
                    valid_citations.append(citation)
                else:
                    invalid_citations.append(citation)
            
            validation_result = {
                "valid_citations_count": len(valid_citations),
                "invalid_citations_count": len(invalid_citations),
                "valid_citations": valid_citations,
                "invalid_citations": invalid_citations,
                "is_valid": len(invalid_citations) == 0
            }
            
            logger.info(f"Citation validation completed. Valid: {len(valid_citations)}, Invalid: {len(invalid_citations)}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error in citation validation: {str(e)}")
            return {
                "valid_citations_count": 0,
                "invalid_citations_count": len(citations),
                "valid_citations": [],
                "invalid_citations": citations,
                "is_valid": False,
                "message": f"Error during citation validation: {str(e)}"
            }


# Singleton instance
content_accuracy_service = ContentAccuracyService()