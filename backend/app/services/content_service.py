from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.book_content import BookContent
from app.models.search_index import SearchIndex
from app.models.translation_set import TranslationSet
from app.models.user_session import UserSession
import logging
import json

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        pass

    def create_content(self, db: Session, title: str, slug: str, content: str,
                      chapter_number: int, section_number: int, parent_id: Optional[str] = None,
                      metadata: Optional[dict] = None) -> BookContent:
        """Create a new book content entry."""
        db_content = BookContent(
            title=title,
            slug=slug,
            content=content,
            chapter_number=chapter_number,
            section_number=section_number,
            parent_id=parent_id,
            metadata_json=metadata or {}
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content

    def get_content_by_id(self, db: Session, content_id: str) -> Optional[BookContent]:
        """Get a book content entry by ID."""
        return db.query(BookContent).filter(BookContent.id == content_id).first()

    def get_content_by_slug(self, db: Session, slug: str) -> Optional[BookContent]:
        """Get a book content entry by slug."""
        return db.query(BookContent).filter(BookContent.slug == slug).first()

    def get_content_list(self, db: Session, skip: int = 0, limit: int = 20,
                        chapter: Optional[int] = None, tags: Optional[List[str]] = None) -> List[BookContent]:
        """Get a list of book content entries with optional filters."""
        query = db.query(BookContent)

        if chapter is not None:
            query = query.filter(BookContent.chapter_number == chapter)

        if tags:
            # For tag filtering, we'll need to join with search index
            # This is a simplified implementation - in a real system, tags would be stored differently
            pass

        return query.offset(skip).limit(limit).all()

    def update_content(self, db: Session, content_id: str, **kwargs) -> Optional[BookContent]:
        """Update a book content entry."""
        db_content = db.query(BookContent).filter(BookContent.id == content_id).first()
        if db_content:
            for key, value in kwargs.items():
                if hasattr(db_content, key):
                    setattr(db_content, key, value)
            db.commit()
            db.refresh(db_content)
        return db_content

    def delete_content(self, db: Session, content_id: str) -> bool:
        """Delete a book content entry."""
        db_content = db.query(BookContent).filter(BookContent.id == content_id).first()
        if db_content:
            db.delete(db_content)
            db.commit()
            return True
        return False

    def get_table_of_contents(self, db: Session) -> dict:
        """Get the table of contents structure."""
        # Get all content ordered by chapter and section
        all_content = db.query(BookContent).order_by(
            BookContent.chapter_number,
            BookContent.section_number
        ).all()

        # Organize by chapters
        toc = {"title": "AI-Native Book", "chapters": []}
        chapters = {}

        for content in all_content:
            if content.chapter_number not in chapters:
                chapters[content.chapter_number] = {
                    "id": f"chapter-{content.chapter_number}",
                    "number": content.chapter_number,
                    "title": content.title,
                    "url_path": f"/docs/chapter-{content.chapter_number}",
                    "sections": []
                }

            if content.section_number > 0:  # Only add as section if it has a section number
                chapters[content.chapter_number]["sections"].append({
                    "id": content.id,
                    "number": content.section_number,
                    "title": content.title,
                    "url_path": f"/docs/{content.slug}"
                })

        toc["chapters"] = list(chapters.values())
        return toc

    def save_reading_progress(self, db: Session, session_id: str, content_id: str, position: dict) -> bool:
        """Save reading progress for a user session."""
        # Check if session already exists
        session = db.query(UserSession).filter(UserSession.session_id == session_id).first()

        if session:
            # Update existing session
            session.last_read_position = position
            session.preferences = {"language": "en"}  # Default language
        else:
            # Create new session
            session = UserSession(
                session_id=session_id,
                last_read_position=position,
                preferences={"language": "en"}
            )
            db.add(session)

        db.commit()
        return True

    def get_reading_progress(self, db: Session, session_id: str) -> Optional[dict]:
        """Get reading progress for a user session."""
        session = db.query(UserSession).filter(UserSession.session_id == session_id).first()

        if session:
            return {
                "position": session.last_read_position,
                "preferences": session.preferences
            }
        return None

# Create a global instance
content_service = ContentService()