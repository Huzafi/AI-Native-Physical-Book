from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ai_book.db")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-and-long-random-string-change-in-production")
    debug: str = os.getenv("DEBUG", "false")
    log_level: str = os.getenv("LOG_LEVEL", "info")

    class Config:
        env_file = ".env"


settings = Settings()