"""RAG orchestration service for the RAG Chatbot application."""

from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from sqlalchemy.orm import Session
from src.services.book_content_service import book_content_service
from src.services.query_service import query_service
from src.services.content_accuracy_service import content_accuracy_service
from src.services.response_service import ResponseService
from src.models.database import SessionLocal
from src.models.query import QueryType
from src.utils.error_handler import log_query, AppException
import logging

logger = logging.getLogger(__name__)


@contextmanager
def get_db_session():
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RAGService:
    """Main service for orchestrating the RAG pipeline."""

    def __init__(self,
                 response_service: Optional[ResponseService] = None,
                 book_content_service=None,
                 query_service=None,
                 content_accuracy_service=None):
        self.response_service = response_service or ResponseService()
        self.book_content_service = book_content_service or book_content_service
        self.query_service = query_service or query_service
        self.content_accuracy_service = content_accuracy_service or content_accuracy_service

    def query_full_book(self, query_text: str, book_id: str, include_citations: bool = True) -> Dict[str, Any]:
        """Process a query against the full book content."""
        with get_db_session() as db:
            try:
                # Create the query in the database
                from src.models.query import QueryBase
                query_data = QueryBase(
                    query_text=query_text,
                    query_type=QueryType.FULL_BOOK,
                    book_id=book_id
                )
                query = self.query_service.create_query(db, query_data)

                # Search for relevant sections in the book
                relevant_sections = self.book_content_service.search_sections(query_text)

                if not relevant_sections:
                    logger.warning(f"No relevant sections found for query: {query_text}")
                    return {
                        "id": query.id,
                        "query": query_text,
                        "response": "I couldn't find relevant information in the book to answer your question.",
                        "citations": [],
                        "confidence_score": 0.0,
                        "query_type": "FULL_BOOK"
                    }

                # Generate response using the relevant sections
                response_text = self.response_service.generate_response(
                    query_text,
                    [section['content'] for section in relevant_sections]
                )

                # Create citations for the response
                citations = []
                if include_citations:
                    for section in relevant_sections:
                        citations.append({
                            "section_title": section.get("title", "Unknown Section"),
                            "page_number": section.get("page_start", 0),
                            "text_snippet": self._truncate_text(section.get("content", ""), 200) + "..."  # First 200 chars
                        })

                # Verify content accuracy
                accuracy_result = self.content_accuracy_service.verify_response_accuracy(
                    query_text,
                    response_text,
                    [section['content'] for section in relevant_sections]
                )

                # Create the response in the database
                response_data = {
                    "response_text": response_text,
                    "citations": citations,
                    "retrieved_chunks": [section['id'] for section in relevant_sections],
                    "confidence_score": accuracy_result.get("accuracy_score", 0.0)
                }
                response = self.query_service.create_response(db, query.id, response_data)

                # Log the query and response for analytics
                log_query(query_text, response_text, accuracy_result.get("accuracy_score", 0.0))

                logger.info(f"Processed full book query: {query.id}")

                return {
                    "id": response.id,
                    "query": query_text,
                    "response": response_text,
                    "citations": citations,
                    "confidence_score": accuracy_result.get("accuracy_score", 0.0),
                    "query_type": "FULL_BOOK"
                }

            except AppException:
                # Re-raise application-specific exceptions
                raise
            except Exception as e:
                logger.error(f"Error processing full book query: {str(e)}")
                raise AppException(
                    status_code=500,
                    detail=f"Error processing full book query: {str(e)}",
                    error_code="RAG_SERVICE_ERROR"
                )

    def query_user_selection(self, query_text: str, selected_text: str, include_citations: bool = False) -> Dict[str, Any]:
        """Process a query against user-selected text only."""
        with get_db_session() as db:
            try:
                # Create the query in the database
                from src.models.query import QueryBase
                query_data = QueryBase(
                    query_text=query_text,
                    query_type=QueryType.USER_SELECTION,
                    user_selected_text=selected_text
                )
                query = self.query_service.create_query(db, query_data)

                # Generate response using only the selected text
                response_text = self.response_service.generate_response(
                    query_text,
                    [selected_text]
                )

                # For user selection, citations are not applicable in the same way
                citations = []

                # Verify content accuracy
                accuracy_result = self.content_accuracy_service.verify_response_accuracy(
                    query_text,
                    response_text,
                    [selected_text]
                )

                # Create the response in the database
                response_data = {
                    "response_text": response_text,
                    "citations": citations,
                    "retrieved_chunks": ["user_selection"],
                    "confidence_score": accuracy_result.get("accuracy_score", 0.0)
                }
                response = self.query_service.create_response(db, query.id, response_data)

                # Log the query and response for analytics
                log_query(query_text, response_text, accuracy_result.get("accuracy_score", 0.0))

                logger.info(f"Processed user selection query: {query.id}")

                return {
                    "id": response.id,
                    "query": query_text,
                    "response": response_text,
                    "citations": citations,
                    "confidence_score": accuracy_result.get("accuracy_score", 0.0),
                    "query_type": "USER_SELECTION"
                }

            except AppException:
                # Re-raise application-specific exceptions
                raise
            except Exception as e:
                logger.error(f"Error processing user selection query: {str(e)}")
                raise AppException(
                    status_code=500,
                    detail=f"Error processing user selection query: {str(e)}",
                    error_code="RAG_SERVICE_ERROR"
                )

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Helper method to truncate text to a maximum length."""
        if len(text) <= max_length:
            return text
        return text[:max_length]

    def process_query(self, query_model) -> Dict[str, Any]:
        """Process a query model based on its type."""
        if query_model.query_type == QueryType.FULL_BOOK:
            return self.query_full_book(
                query_text=query_model.query_text,
                book_id=query_model.book_id,
                include_citations=True
            )
        elif query_model.query_type == QueryType.USER_SELECTION:
            return self.query_user_selection(
                query_text=query_model.query_text,
                selected_text=query_model.user_selected_text,
                include_citations=False
            )
        else:
            raise AppException(
                status_code=400,
                detail=f"Unsupported query type: {query_model.query_type}",
                error_code="UNSUPPORTED_QUERY_TYPE"
            )


# Singleton instance
rag_service = RAGService()