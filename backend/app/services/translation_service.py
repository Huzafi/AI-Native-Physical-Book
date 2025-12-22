from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.translation_set import TranslationSet
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        pass

    def create_translation(self, db: Session, content_id: str, language_code: str,
                          translated_title: str, translated_content: str,
                          summary: Optional[str] = None) -> TranslationSet:
        """Create a new translation for content."""
        translation = TranslationSet(
            content_id=content_id,
            language_code=language_code,
            translated_title=translated_title,
            translated_content=translated_content,
            summary=summary
        )
        db.add(translation)
        db.commit()
        db.refresh(translation)
        return translation

    def get_translation(self, db: Session, content_id: str, language_code: str) -> Optional[TranslationSet]:
        """Get a specific translation for content and language."""
        return db.query(TranslationSet).filter(
            TranslationSet.content_id == content_id,
            TranslationSet.language_code == language_code
        ).first()

    def get_translations_for_content(self, db: Session, content_id: str) -> List[TranslationSet]:
        """Get all translations for a specific content."""
        return db.query(TranslationSet).filter(
            TranslationSet.content_id == content_id
        ).all()

    def get_translations_by_language(self, db: Session, language_code: str) -> List[TranslationSet]:
        """Get all translations for a specific language."""
        return db.query(TranslationSet).filter(
            TranslationSet.language_code == language_code
        ).all()

    def update_translation(self, db: Session, content_id: str, language_code: str,
                          **kwargs) -> Optional[TranslationSet]:
        """Update an existing translation."""
        translation = db.query(TranslationSet).filter(
            TranslationSet.content_id == content_id,
            TranslationSet.language_code == language_code
        ).first()

        if translation:
            for key, value in kwargs.items():
                if hasattr(translation, key):
                    setattr(translation, key, value)
            db.commit()
            db.refresh(translation)

        return translation

    def delete_translation(self, db: Session, content_id: str, language_code: str) -> bool:
        """Delete a translation."""
        translation = db.query(TranslationSet).filter(
            TranslationSet.content_id == content_id,
            TranslationSet.language_code == language_code
        ).first()

        if translation:
            db.delete(translation)
            db.commit()
            return True

        return False

    def get_available_languages_for_content(self, db: Session, content_id: str) -> List[str]:
        """Get all available language codes for a specific content."""
        translations = db.query(TranslationSet.language_code).filter(
            TranslationSet.content_id == content_id
        ).all()

        return [t.language_code for t in translations]

    def get_translation_progress(self, db: Session, language_code: str) -> dict:
        """Get translation progress for a language."""
        # Get total book content
        from app.models.book_content import BookContent
        total_content = db.query(BookContent).count()

        # Get translated content for the specified language
        translated_content = db.query(TranslationSet).filter(
            TranslationSet.language_code == language_code
        ).count()

        # Calculate progress percentage
        progress_percentage = (translated_content / total_content * 100) if total_content > 0 else 0

        return {
            "language_code": language_code,
            "total_content": total_content,
            "translated_content": translated_content,
            "progress_percentage": progress_percentage
        }

    def validate_translation_content(self, content_id: str, language_code: str,
                                   translated_title: str, translated_content: str) -> dict:
        """Validate translation content quality and format."""
        errors = []

        # Check if required fields are provided
        if not translated_title or len(translated_title.strip()) == 0:
            errors.append("Translated title is required")

        if not translated_content or len(translated_content.strip()) == 0:
            errors.append("Translated content is required")

        # Check for quality issues
        if translated_content:
            # Check for repeated characters that might indicate encoding issues
            import re
            if re.search(r'(.)\1{5,}', translated_content):
                errors.append("Translation contains repeated characters that may indicate encoding issues")

            # Check for unusual character sequences
            if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', translated_content):
                errors.append("Translation contains control characters that may indicate processing errors")

        # Check if translation is too short compared to expected content length
        # This is a simple check - in a real implementation, we might compare to original content
        if translated_content and len(translated_content.strip()) < 10:
            errors.append("Translation content appears to be too short")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

# Create a global instance
translation_service = TranslationService()