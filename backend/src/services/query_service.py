"""Query service for the RAG Chatbot application."""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.query import Query, QueryBase, QueryType
from src.models.response import Response
from src.models.citation import Citation
from src.models.database import SessionLocal
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class QueryService:
    """Service for managing queries and responses."""
    
    def __init__(self):
        pass
    
    def create_query(self, db: Session, query_data: QueryBase) -> Query:
        """Create a new query."""
        from src.models import Query as QueryModel
        
        db_query = QueryModel(
            query_text=query_data.query_text,
            query_type=query_data.query_type.value,
            user_selected_text=query_data.user_selected_text,
            book_id=query_data.book_id,
            session_id=query_data.session_id,
        )
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        
        logger.info(f"Created query with ID: {db_query.id}")
        return db_query
    
    def get_query(self, db: Session, query_id: str) -> Optional[Query]:
        """Get a query by ID."""
        from src.models import Query as QueryModel
        
        db_query = db.query(QueryModel).filter(QueryModel.id == query_id).first()
        return db_query
    
    def create_response(self, db: Session, query_id: str, response_data: dict) -> Response:
        """Create a response for a query."""
        from src.models import Response as ResponseModel
        
        db_response = ResponseModel(
            query_id=query_id,
            response_text=response_data.get('response_text', ''),
            citations=response_data.get('citations', []),
            retrieved_chunks=response_data.get('retrieved_chunks', []),
            confidence_score=response_data.get('confidence_score', 0.0)
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        
        logger.info(f"Created response with ID: {db_response.id} for query: {query_id}")
        return db_response
    
    def get_response(self, db: Session, response_id: str) -> Optional[Response]:
        """Get a response by ID."""
        from src.models import Response as ResponseModel
        
        db_response = db.query(ResponseModel).filter(ResponseModel.id == response_id).first()
        return db_response
    
    def get_response_by_query(self, db: Session, query_id: str) -> Optional[Response]:
        """Get the response for a specific query."""
        from src.models import Response as ResponseModel
        
        db_response = db.query(ResponseModel).filter(ResponseModel.query_id == query_id).first()
        return db_response


# Singleton instance
query_service = QueryService()


# uvicorn src.api.main:app --reload
