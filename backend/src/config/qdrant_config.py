"""Qdrant configuration for the RAG Chatbot application."""

from pydantic_settings import BaseSettings
import os


class QdrantSettings(BaseSettings):
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "book_embeddings")

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from .env that don't match class fields


# Create settings instance
settings = QdrantSettings()

# Export the settings
QDRANT_URL = settings.qdrant_url
QDRANT_API_KEY = settings.qdrant_api_key
QDRANT_COLLECTION_NAME = settings.qdrant_collection_name