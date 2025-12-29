"""Response generation service for the RAG Chatbot application."""

from typing import List
from src.config.cohere_config import generate_text
import logging

logger = logging.getLogger(__name__)


class ResponseService:
    """Service for generating responses with citations."""
    
    def __init__(self):
        pass
    
    def generate_response(self, query: str, context_chunks: List[str]) -> str:
        """
        Generate a response based on the query and context chunks.
        
        Args:
            query: The user's query
            context_chunks: List of relevant text chunks to use as context
            
        Returns:
            Generated response text
        """
        try:
            # Combine the context chunks into a single context string
            context = "\n\n".join(context_chunks)
            
            # Create a prompt for the language model
            prompt = f"""
            Based on the following context, please answer the question. 
            If the answer cannot be found in the context, please say so.
            
            Context:
            {context}
            
            Question: {query}
            
            Answer:"""
            
            # Generate the response using Cohere
            response = generate_text(prompt, max_tokens=500)
            
            logger.info(f"Generated response for query: {query[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            # Return a default response in case of error
            return "I'm sorry, but I encountered an error while generating a response. Please try again later."
    
    def format_citations(self, response: str, source_chunks: List[dict]) -> List[dict]:
        """
        Format citations for the response based on the source chunks.
        
        Args:
            response: The generated response
            source_chunks: List of source chunks used to generate the response
            
        Returns:
            List of formatted citations
        """
        try:
            citations = []
            for chunk in source_chunks:
                citation = {
                    "section_title": chunk.get("title", "Unknown Section"),
                    "page_number": chunk.get("page_start", 0),
                    "text_snippet": chunk.get("content", "")[:200] + "..."  # First 200 chars
                }
                citations.append(citation)
            
            logger.info(f"Formatted {len(citations)} citations for response")
            return citations
            
        except Exception as e:
            logger.error(f"Error formatting citations: {str(e)}")
            return []


# Singleton instance
response_service = ResponseService()