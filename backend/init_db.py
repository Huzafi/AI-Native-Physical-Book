"""Script to initialize the database tables."""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import all models to register them with Base before creating tables
from src.models import Query, Response, BookContent, BookSection, Citation
from src.models.database import engine, Base

def init_db():
    """Initialize the database by creating all tables."""
    print("Initializing database...")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    return True

if __name__ == "__main__":
    success = init_db()
    if success:
        print("Database initialization completed successfully.")
    else:
        print("Database initialization failed.")
        sys.exit(1)