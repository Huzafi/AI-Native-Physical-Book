"""Database models for the RAG Chatbot application."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class BookContent(Base):
    __tablename__ = 'book_content'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=True)  # Optional ISBN
    content = Column(Text, nullable=False)  # Full book content
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BookSection(Base):
    __tablename__ = 'book_sections'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    book_id = Column(String, ForeignKey('book_content.id'), nullable=False)
    section_title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    page_start = Column(Integer, nullable=True)
    page_end = Column(Integer, nullable=True)
    section_order = Column(Integer, nullable=False)
    vector_id = Column(String, nullable=True)  # ID in Qdrant vector store
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Query(Base):
    __tablename__ = 'queries'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    query_text = Column(Text, nullable=False)
    query_embedding = Column(JSON, nullable=True)  # Embedding vector stored as JSON
    query_type = Column(String, nullable=False)  # 'FULL_BOOK' or 'USER_SELECTION'
    user_selected_text = Column(Text, nullable=True)  # Optional text for isolation mode
    book_id = Column(String, ForeignKey('book_content.id'), nullable=True)
    session_id = Column(String, nullable=True)  # ID to group related queries
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Response(Base):
    __tablename__ = 'responses'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    query_id = Column(String, ForeignKey('queries.id'), nullable=False)
    response_text = Column(Text, nullable=False)
    citations = Column(JSON, nullable=True)  # List of citations with section/page info
    retrieved_chunks = Column(JSON, nullable=True)  # List of retrieved chunk IDs
    confidence_score = Column(Integer, nullable=True)  # Confidence score of the response
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Citation(Base):
    __tablename__ = 'citations'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    response_id = Column(String, ForeignKey('responses.id'), nullable=False)
    section_id = Column(String, ForeignKey('book_sections.id'), nullable=False)
    text_snippet = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    confidence = Column(Integer, nullable=True)  # Confidence of the citation relevance