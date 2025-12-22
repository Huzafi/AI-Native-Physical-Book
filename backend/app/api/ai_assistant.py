from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import logging
from app.database.database import get_db
from app.services.rag_service import rag_service
from app.middleware.error_handlers import ai_assistant_rate_limit

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", tags=["ai-assistant"])
@ai_assistant_rate_limit  # Apply rate limiting
async def ask_question(
    request: Request,
    question: str,
    context_content_id: str = None,
    include_sources: bool = True,
    db: Session = Depends(get_db)
):
    """Ask questions about book content"""
    try:
        if not question or len(question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        if len(question) > 1000:
            raise HTTPException(status_code=400, detail="Question is too long (max 1000 characters)")

        # Answer the question using RAG
        result = rag_service.answer_question(
            db=db,
            question=question,
            context_content_id=context_content_id
        )

        # Return response in the expected format
        response = {
            "answer": result["answer"],
            "sources": result["sources"] if include_sources else [],
            "response_time_ms": 100,  # Placeholder - would measure actual time in real implementation
            "confidence": result["confidence"]
        }

        return response
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"AI assistant error: {str(e)}")
        raise HTTPException(status_code=500, detail="AI service unavailable")