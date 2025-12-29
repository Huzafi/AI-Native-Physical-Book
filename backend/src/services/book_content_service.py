"""BookContent service for the RAG Chatbot application."""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.book_content import BookContent, BookContentBase
from src.models.database import SessionLocal
from src.models.book_section import BookSection
from src.config.qdrant_config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging

logger = logging.getLogger(__name__)


class BookContentService:
    """Service for managing book content and sections."""
    
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        self.collection_name = QDRANT_COLLECTION_NAME
    
    def create_book_content(self, db: Session, book_data: BookContentBase) -> BookContent:
        """Create a new book content entry."""
        from src.models import BookContent as BookContentModel
        
        db_book = BookContentModel(
            title=book_data.title,
            author=book_data.author,
            isbn=book_data.isbn,
            content=book_data.content
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        
        logger.info(f"Created book content with ID: {db_book.id}")
        return db_book
    
    def get_book_content(self, db: Session, book_id: str) -> Optional[BookContent]:
        """Get book content by ID."""
        from src.models import BookContent as BookContentModel
        
        db_book = db.query(BookContentModel).filter(BookContentModel.id == book_id).first()
        return db_book
    
    def create_book_sections(self, db: Session, book_id: str, sections: List[dict]) -> List[BookSection]:
        """Create sections for a book and store their embeddings in Qdrant."""
        from src.models import BookSection as BookSectionModel
        from src.config.cohere_config import generate_embeddings
        
        created_sections = []
        
        for i, section_data in enumerate(sections):
            # Create the section in the database
            db_section = BookSectionModel(
                book_id=book_id,
                section_title=section_data.get('title', f'Section {i+1}'),
                content=section_data.get('content', ''),
                page_start=section_data.get('page_start'),
                page_end=section_data.get('page_end'),
                section_order=section_data.get('order', i),
            )
            db.add(db_section)
            db.commit()
            db.refresh(db_section)
            
            # Generate embedding for the section content
            embeddings = generate_embeddings([db_section.content])
            embedding_vector = embeddings[0] if embeddings else []
            
            # Store the embedding in Qdrant
            if embedding_vector:
                # Create collection if it doesn't exist
                try:
                    self.qdrant_client.get_collection(self.collection_name)
                except:
                    self.qdrant_client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=models.VectorParams(size=len(embedding_vector), distance=models.Distance.COSINE),
                    )
                
                # Store the embedding
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=[
                        models.PointStruct(
                            id=db_section.id,
                            vector=embedding_vector,
                            payload={
                                "book_id": book_id,
                                "section_id": db_section.id,
                                "section_title": db_section.section_title,
                                "content": db_section.content,
                                "page_start": db_section.page_start,
                                "page_end": db_section.page_end,
                            }
                        )
                    ]
                )
                
                # Update the section with the vector ID
                db_section.vector_id = db_section.id
                db.add(db_section)
                db.commit()
            
            created_sections.append(db_section)
        
        logger.info(f"Created {len(created_sections)} sections for book {book_id}")
        return created_sections
    
    def search_sections(self, query_text: str, limit: int = 5) -> List[dict]:
        """Search for relevant sections using vector similarity."""
        from src.config.cohere_config import generate_embeddings
        
        # Generate embedding for the query
        query_embeddings = generate_embeddings([query_text])
        query_vector = query_embeddings[0] if query_embeddings else []
        
        if not query_vector:
            logger.warning("Could not generate embedding for query")
            return []
        
        # Search in Qdrant
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
        )
        
        # Extract relevant information from results
        sections = []
        for result in search_results:
            sections.append({
                "id": result.payload.get("section_id"),
                "title": result.payload.get("section_title"),
                "content": result.payload.get("content"),
                "page_start": result.payload.get("page_start"),
                "page_end": result.payload.get("page_end"),
                "score": result.score
            })
        
        logger.info(f"Found {len(sections)} relevant sections for query")
        return sections


# Singleton instance
book_content_service = BookContentService()