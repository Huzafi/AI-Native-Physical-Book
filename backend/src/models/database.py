"""Database configuration and setup for the RAG Chatbot application."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os


class DatabaseSettings(BaseSettings):
    database_url: str = os.getenv("NEON_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
    async_database_url: str = os.getenv("NEON_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")  # For async operations

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from .env that don't match class fields


# Create settings instance
settings = DatabaseSettings()

# Create sync engine and session factory
sync_engine = create_engine(
    settings.database_url.replace("+asyncpg", "") if "+asyncpg" in settings.database_url else settings.database_url,
    echo=True,  # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Create async engine and session factory
async_engine = create_async_engine(
    settings.async_database_url,
    echo=True,  # Set to True for SQL query logging
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """Dependency to get sync database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_session():
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        yield session