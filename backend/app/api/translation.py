from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from app.database.database import get_db
from app.services.translation_service import translation_service
from app.models.translation_set import TranslationSet

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", tags=["translation"])
async def create_translation(
    content_id: str,
    language_code: str,
    translated_title: str,
    translated_content: str,
    summary: str = None,
    db: Session = Depends(get_db)
):
    """Create a translation for content"""
    try:
        # Validate language code (should be ISO 639-1 or 639-2)
        if len(language_code) not in [2, 3]:
            raise HTTPException(status_code=400, detail="Invalid language code. Use ISO 639-1 or 639-2 format.")

        # Validate translation content
        validation_result = translation_service.validate_translation_content(
            content_id, language_code, translated_title, translated_content
        )

        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Translation validation failed: {'; '.join(validation_result['errors'])}"
            )

        # Check if translation already exists
        existing_translation = translation_service.get_translation(db, content_id, language_code)
        if existing_translation:
            raise HTTPException(status_code=409, detail="Translation already exists for this content and language.")

        # Create the translation
        translation = translation_service.create_translation(
            db=db,
            content_id=content_id,
            language_code=language_code,
            translated_title=translated_title,
            translated_content=translated_content,
            summary=summary
        )

        return {
            "id": translation.id,
            "content_id": translation.content_id,
            "language_code": translation.language_code,
            "translated_title": translation.translated_title,
            "summary": translation.summary
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating translation: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service unavailable")

@router.get("/{content_id}/{language_code}", tags=["translation"])
async def get_translation(
    content_id: str,
    language_code: str,
    db: Session = Depends(get_db)
):
    """Get a specific translation for content and language"""
    try:
        translation = translation_service.get_translation(db, content_id, language_code)
        if not translation:
            raise HTTPException(status_code=404, detail="Translation not found")

        return {
            "id": translation.id,
            "content_id": translation.content_id,
            "language_code": translation.language_code,
            "translated_title": translation.translated_title,
            "translated_content": translation.translated_content,
            "summary": translation.summary,
            "created_at": translation.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting translation: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service unavailable")

@router.get("/{content_id}", tags=["translation"])
async def get_translations_for_content(
    content_id: str,
    db: Session = Depends(get_db)
):
    """Get all translations for a specific content"""
    try:
        translations = translation_service.get_translations_for_content(db, content_id)

        return {
            "content_id": content_id,
            "translations": [
                {
                    "id": t.id,
                    "language_code": t.language_code,
                    "translated_title": t.translated_title,
                    "summary": t.summary,
                    "created_at": t.created_at
                }
                for t in translations
            ]
        }
    except Exception as e:
        logger.error(f"Error getting translations for content: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service unavailable")

@router.get("/progress/{language_code}", tags=["translation"])
async def get_translation_progress(
    language_code: str,
    db: Session = Depends(get_db)
):
    """Get translation progress for a language"""
    try:
        progress = translation_service.get_translation_progress(db, language_code)
        return progress
    except Exception as e:
        logger.error(f"Error getting translation progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service unavailable")

@router.put("/{content_id}/{language_code}", tags=["translation"])
async def update_translation(
    content_id: str,
    language_code: str,
    translated_title: str = None,
    translated_content: str = None,
    summary: str = None,
    db: Session = Depends(get_db)
):
    """Update an existing translation"""
    try:
        # Get the current translation to update
        current_translation = translation_service.get_translation(db, content_id, language_code)
        if not current_translation:
            raise HTTPException(status_code=404, detail="Translation not found")

        # Use existing values if not provided in update
        update_translated_title = translated_title or current_translation.translated_title
        update_translated_content = translated_content or current_translation.translated_content
        update_summary = summary if summary is not None else current_translation.summary

        # Validate translation content
        validation_result = translation_service.validate_translation_content(
            content_id, language_code, update_translated_title, update_translated_content
        )

        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Translation validation failed: {'; '.join(validation_result['errors'])}"
            )

        # Prepare update data
        update_data = {}
        if translated_title is not None:
            update_data["translated_title"] = translated_title
        if translated_content is not None:
            update_data["translated_content"] = translated_content
        if summary is not None:
            update_data["summary"] = summary

        # Update the translation
        updated_translation = translation_service.update_translation(
            db=db,
            content_id=content_id,
            language_code=language_code,
            **update_data
        )

        if not updated_translation:
            raise HTTPException(status_code=500, detail="Failed to update translation")

        return {
            "id": updated_translation.id,
            "content_id": updated_translation.content_id,
            "language_code": updated_translation.language_code,
            "translated_title": updated_translation.translated_title,
            "summary": updated_translation.summary
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating translation: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service unavailable")

@router.delete("/{content_id}/{language_code}", tags=["translation"])
async def delete_translation(
    content_id: str,
    language_code: str,
    db: Session = Depends(get_db)
):
    """Delete a translation"""
    try:
        success = translation_service.delete_translation(db, content_id, language_code)
        if not success:
            raise HTTPException(status_code=404, detail="Translation not found")

        return {"message": "Translation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting translation: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service unavailable")