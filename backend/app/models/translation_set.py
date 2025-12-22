from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class TranslationSet(Base):
    __tablename__ = "translation_set"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_id = Column(String, nullable=False)  # Reference to Book Content
    language_code = Column(String, nullable=False)  # e.g., 'ur' for Urdu
    translated_title = Column(String, nullable=False)
    translated_content = Column(Text, nullable=False)  # Translated MDX content
    summary = Column(Text, nullable=True)  # Optional summary in target language
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TranslationSet(id={self.id}, content_id={self.content_id}, language_code={self.language_code})>"