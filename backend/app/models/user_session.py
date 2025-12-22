from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class UserSession(Base):
    __tablename__ = "user_session"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    last_read_position = Column(JSON, nullable=False)  # JSON object with chapter/section/paragraph position
    preferences = Column(JSON, default=lambda: {})  # JSON object with reader preferences like language selection
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # Short-lived session

    def __repr__(self):
        return f"<UserSession(session_id={self.session_id})>"