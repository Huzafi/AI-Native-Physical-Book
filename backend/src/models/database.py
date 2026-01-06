"""Database configuration and setup for the RAG Chatbot application."""

import os
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base  # Import the Base from models module to ensure all models are registered

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseSettings(BaseSettings):
    """
    Database settings.
    Defaults to SQLite if no environment variable is provided.
    """
    database_url: str = os.getenv(
        "NEON_DATABASE_URL",
        "sqlite:///./rag_chatbot.db"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


# Create settings instance
settings = DatabaseSettings()

# Detect database type
using_postgres = settings.database_url.lower().startswith("postgresql")

# Ensure sslmode for Neon PostgreSQL
if using_postgres and "neon" in settings.database_url.lower():
    if "sslmode" not in settings.database_url:
        if "?" in settings.database_url:
            settings.database_url += "&sslmode=require"
        else:
            settings.database_url += "?sslmode=require"


# Create SQLAlchemy engine
if using_postgres:
    engine = create_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        echo=True,
        connect_args={"check_same_thread": False},
    )

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
