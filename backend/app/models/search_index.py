from sqlalchemy import Column, Integer, String, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class SearchIndex(Base):
    __tablename__ = "search_index"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content_preview = Column(Text, nullable=False)  # Shortened content for search results
    url_path = Column(String, nullable=False, unique=True)
    tags = Column(ARRAY(String), default=[])  # Content tags for filtering
    last_indexed = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<SearchIndex(id={self.id}, title={self.title}, url_path={self.url_path})>"