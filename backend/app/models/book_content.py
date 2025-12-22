from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class BookContent(Base):
    __tablename__ = "book_content"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=False)  # MDX content
    chapter_number = Column(Integer, nullable=False)
    section_number = Column(Integer, nullable=False)
    parent_id = Column(String, nullable=True)  # For nested sections
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    metadata_json = Column(JSON, name="metadata")  # Additional content metadata

    def __repr__(self):
        return f"<BookContent(id={self.id}, title={self.title}, slug={self.slug})>"