"""Book metadata retrieval service for the RAG Chatbot application."""

from typing import Optional
from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.book_content import BookContent
from src.utils.cache import cached, invalidate_cache
import logging

logger = logging.getLogger(__name__)


class BookService:
    """Service for retrieving book metadata."""

    def __init__(self):
        pass

    @cached(ttl_seconds=600)  # Cache for 10 minutes
    def get_book_info(self, book_id: str) -> Optional[dict]:
        """Get information about a specific book."""
        db = SessionLocal()
        try:
            # Get the book from the database
            book = db.query(BookContent).filter(BookContent.id == book_id).first()

            if not book:
                logger.info(f"Book not found: {book_id}")
                return None

            # Count the sections for this book
            from src.models import BookSection
            section_count = db.query(BookSection).filter(BookSection.book_id == book_id).count()

            # Estimate total pages (this would be more accurate if stored in the database)
            # For now, we'll estimate based on content length
            total_pages = len(book.content) // 2000  # Rough estimate: 2000 chars per page

            book_info = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "section_count": section_count,
                "total_pages": total_pages,
                "created_at": book.created_at.isoformat() if book.created_at else "",
                "updated_at": book.updated_at.isoformat() if book.updated_at else ""
            }

            # Log the book retrieval operation for User Story 3
            logger.info(f"User Story 3 - Book info retrieved: {book_id}, Title: {book.title}")
            return book_info

        except Exception as e:
            logger.error(f"Error retrieving book info for {book_id}: {str(e)}")
            raise e
        finally:
            db.close()

    def invalidate_book_cache(self, book_id: str):
        """Invalidate the cache for a specific book."""
        # Create the same cache key that would be used by get_book_info
        cache_key = f"src.services.book_service.BookService.get_book_info:('{book_id}',):[]"
        from src.utils.cache import cache
        cache.delete(cache_key)


# Singleton instance
book_service = BookService()