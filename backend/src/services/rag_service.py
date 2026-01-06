"""RAG orchestration service for the RAG Chatbot application."""

from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.services.book_content_service import book_content_service as imported_book_content_service
from src.services.query_service import query_service as imported_query_service
from src.services.content_accuracy_service import content_accuracy_service as imported_content_accuracy_service
from src.services.response_service import ResponseService
from src.models.database import SessionLocal
from src.models.query import QueryType
from src.utils.error_handler import log_query, AppException
import logging
import uuid

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
        self.book_content_service = book_content_service or imported_book_content_service
        self.query_service = query_service or imported_query_service
        self.content_accuracy_service = content_accuracy_service or imported_content_accuracy_service

        # Validate that required services are available
        if self.query_service is None:
            raise ValueError("query_service cannot be None - it's required for RAG operations")
        if self.book_content_service is None:
            raise ValueError("book_content_service cannot be None - it's required for RAG operations")

    def query_full_book(self, query_text: str, book_id: str, include_citations: bool = True) -> Dict[str, Any]:
        """Process a query against the full book content."""
        try:
            # Try to create the query in the database, but continue if it fails
            try:
                with get_db_session() as db:
                    from src.models.query import QueryBase
                    query_data = QueryBase(
                        query_text=query_text,
                        query_type=QueryType.FULL_BOOK,
                        book_id=book_id
                    )
                    query = self.query_service.create_query(db, query_data)
                    query_id = query.id
                    db_available = True
            except Exception as db_error:
                logger.warning(f"Database error creating query: {str(db_error)}. Continuing without database logging.")
                query_id = str(uuid.uuid4())  # Generate a temporary ID
                db_available = False

            # Search for relevant sections in the book - this is the core of RAG
            relevant_sections = self.book_content_service.search_sections(query_text)

            if not relevant_sections:
                logger.warning(f"No relevant sections found for query: {query_text}")
                # Check if the Qdrant collection is empty (book content not indexed)
                try:
                    from src.config.qdrant_config import QDRANT_COLLECTION_NAME
                    collection_info = self.book_content_service.qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
                    if collection_info.points_count == 0:
                        return {
                            "id": query_id,
                            "query": query_text,
                            "response": "Book content is not indexed yet. Please upload or index the book first.",
                            "citations": [],
                            "confidence_score": 0.0,
                            "query_type": "FULL_BOOK"
                        }
                    else:
                        return {
                            "id": query_id,
                            "query": query_text,
                            "response": "I couldn't find relevant information in the book to answer your question.",
                            "citations": [],
                            "confidence_score": 0.0,
                            "query_type": "FULL_BOOK"
                        }
                except Exception:
                    # If we can't access the collection, assume no content is indexed
                    return {
                        "id": query_id,
                        "query": query_text,
                        "response": "Book content is not indexed yet. Please upload or index the book first.",
                        "citations": [],
                        "confidence_score": 0.0,
                        "query_type": "FULL_BOOK"
                    }

            # Ensure the response is strictly grounded in book content
            book_contents = [section['content'] for section in relevant_sections]

            # Generate response using ONLY the relevant sections from the book
            response_text = self.response_service.generate_response(
                query_text,
                book_contents  # Pass only book content, ensuring grounding
            )

            # Verify that the response is actually grounded in the source content
            if not self._is_response_based_on_content(response_text, book_contents):
                logger.warning(f"Response may not be properly grounded in book content for query: {query_text}")
                response_text = "I found relevant information in the book, but I need to be careful not to fabricate details. Please check the book sections directly for accurate information."

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
                book_contents
            )

            # Try to save response to database if DB is available
            if db_available:
                try:
                    with get_db_session() as db:
                        # Create the response in the database
                        response_data = {
                            "response_text": response_text,
                            "citations": citations,
                            "retrieved_chunks": [section['id'] for section in relevant_sections],
                            "confidence_score": accuracy_result.get("accuracy_score", 0.0)
                        }
                        response = self.query_service.create_response(db, query.id, response_data)
                        response_id = response.id

                        # Log the query and response for analytics
                        log_query(query_text, response_text, accuracy_result.get("accuracy_score", 0.0))
                        logger.info(f"Processed full book query: {query.id}")
                except Exception as db_error:
                    logger.warning(f"Database error creating response: {str(db_error)}. Response still generated successfully.")
                    response_id = str(uuid.uuid4())  # Generate a temporary ID
            else:
                response_id = str(uuid.uuid4())  # Generate a temporary ID when DB is unavailable

            return {
                "id": response_id,
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
        try:
            # Try to create the query in the database, but continue if it fails
            try:
                with get_db_session() as db:
                    from src.models.query import QueryBase
                    query_data = QueryBase(
                        query_text=query_text,
                        query_type=QueryType.USER_SELECTION,
                        user_selected_text=selected_text
                    )
                    query = self.query_service.create_query(db, query_data)
                    query_id = query.id
                    db_available = True
            except Exception as db_error:
                logger.warning(f"Database error creating query: {str(db_error)}. Continuing without database logging.")
                query_id = str(uuid.uuid4())  # Generate a temporary ID
                db_available = False

            # Check if selected text is empty or too short
            if not selected_text or len(selected_text.strip()) < 5:
                logger.warning(f"Selected text is empty or too short for query: {query_text}")
                response_text = "The selected text is too short or empty to generate a meaningful response. Please select more content."
            else:
                # Generate response using only the selected text - ensuring grounding
                response_text = self.response_service.generate_response(
                    query_text,
                    [selected_text]
                )

            # Verify that the response is actually grounded in the provided text
            if not self._is_response_based_on_content(response_text, [selected_text]):
                logger.warning(f"Response may not be properly grounded in user selection for query: {query_text}")
                response_text = "Based on the selected text provided, I cannot generate a specific answer. Please review the selected text for more details."

            # For user selection, citations are not applicable in the same way
            citations = []

            # Verify content accuracy
            accuracy_result = self.content_accuracy_service.verify_response_accuracy(
                query_text,
                response_text,
                [selected_text]
            )

            # Try to save response to database if DB is available
            if db_available:
                try:
                    with get_db_session() as db:
                        # Create the response in the database
                        response_data = {
                            "response_text": response_text,
                            "citations": citations,
                            "retrieved_chunks": ["user_selection"],
                            "confidence_score": accuracy_result.get("accuracy_score", 0.0)
                        }
                        response = self.query_service.create_response(db, query.id, response_data)
                        response_id = response.id

                        # Log the query and response for analytics
                        log_query(query_text, response_text, accuracy_result.get("accuracy_score", 0.0))
                        logger.info(f"Processed user selection query: {query.id}")
                except Exception as db_error:
                    logger.warning(f"Database error creating response: {str(db_error)}. Response still generated successfully.")
                    response_id = str(uuid.uuid4())  # Generate a temporary ID
            else:
                response_id = str(uuid.uuid4())  # Generate a temporary ID when DB is unavailable

            return {
                "id": response_id,
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

    def _is_response_based_on_content(self, response: str, content_list: List[str]) -> bool:
        """
        Check if the response is based on the provided content.
        This is a simple check that looks for content overlap.
        """
        if not content_list:
            return False

        response_lower = response.lower()
        content_text = " ".join(content_list).lower()

        # Check if there's significant overlap between response and content
        response_words = set(response_lower.split())
        content_words = set(content_text.split())

        # If more than 30% of response words appear in content, consider it grounded
        if response_words and content_words:
            overlap = len(response_words.intersection(content_words))
            return overlap / len(response_words) > 0.3

        return True  # If no words to compare, assume it's OK

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