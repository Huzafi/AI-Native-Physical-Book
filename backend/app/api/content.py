from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from app.database.database import get_db
from app.services.content_service import content_service
from app.api.content_models import (
    ContentResponse, ContentListPaginatedResponse, TableOfContentsResponse,
    ReadingProgressRequest, ReadingProgressResponse, ReadingProgressGetResponse
)
from app.middleware.error_handlers import search_rate_limit
from app.models.book_content import BookContent
from app.models.translation_set import TranslationSet

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content_by_id(content_id: str, db: Session = Depends(get_db)):
    """Retrieve specific book content by ID"""
    content = content_service.get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Fetch available translations for this content
    translations = db.query(TranslationSet).filter(
        TranslationSet.content_id == content_id
    ).all()

    # Format translations for response
    formatted_translations = []
    for translation in translations:
        formatted_translations.append({
            "language_code": translation.language_code,
            "title": translation.translated_title,
            "content": translation.translated_content,
            "summary": translation.summary
        })

    return ContentResponse(
        id=content.id,
        title=content.title,
        slug=content.slug,
        content=content.content,
        chapter_number=content.chapter_number,
        section_number=content.section_number,
        parent_id=content.parent_id,
        metadata=content.metadata_json,
        translations=formatted_translations,
        created_at=content.created_at,
        updated_at=content.updated_at
    )

@router.get("/", response_model=ContentListPaginatedResponse)
async def list_content(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    chapter: Optional[int] = Query(None),
    tags: str = Query(None),
    db: Session = Depends(get_db)
):
    """List book content with pagination"""
    skip = (page - 1) * limit

    # Parse tags if provided
    tags_list = tags.split(",") if tags else None

    contents = content_service.get_content_list(
        db, skip=skip, limit=limit, chapter=chapter, tags=tags_list
    )

    # Convert to response format
    items = []
    for content in contents:
        # Fetch available languages for this content
        available_languages = db.query(TranslationSet.language_code).filter(
            TranslationSet.content_id == content.id
        ).all()
        language_codes = [lang.language_code for lang in available_languages]

        items.append({
            "id": content.id,
            "title": content.title,
            "slug": content.slug,
            "chapter_number": content.chapter_number,
            "section_number": content.section_number,
            "url_path": f"/docs/{content.slug}",
            "preview": content.content[:200] + "..." if len(content.content) > 200 else content.content,
            "tags": [],
            "reading_time": len(content.content.split()) // 200,  # Rough estimate
            "available_translations": language_codes  # Include available translation languages
        })

    # Calculate total for pagination (properly this time)
    total = db.query(BookContent).count()

    return ContentListPaginatedResponse(
        items=items,
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    )

@router.get("/toc", response_model=TableOfContentsResponse)
async def get_table_of_contents(db: Session = Depends(get_db)):
    """Retrieve table of contents structure"""
    toc = content_service.get_table_of_contents(db)
    return TableOfContentsResponse(**toc)

@router.post("/reading-progress", response_model=ReadingProgressResponse)
@search_rate_limit  # Apply rate limiting
async def save_reading_progress(
    request: Request,
    reading_progress_request: ReadingProgressRequest,
    db: Session = Depends(get_db)
):
    """Save user's reading progress (temporary session)"""
    # In a real implementation, we would store this in the UserSession model
    # For now, we'll just return a success response
    from datetime import datetime, timedelta

    expires_at = datetime.now() + timedelta(hours=24)  # Session expires in 24 hours

    return ReadingProgressResponse(
        status="saved",
        expires_at=expires_at
    )

@router.get("/reading-progress/{session_id}", response_model=ReadingProgressGetResponse)
async def get_reading_progress(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve user's reading progress"""
    # In a real implementation, we would fetch from the UserSession model
    # For now, we'll return a default response
    return ReadingProgressGetResponse(
        position={
            "content_id": "",
            "chapter": 1,
            "section": 1,
            "paragraph": 1,
            "percent": 0
        },
        preferences={
            "language": "en"
        }
    )