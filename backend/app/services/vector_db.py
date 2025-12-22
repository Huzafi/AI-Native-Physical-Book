from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from typing import List, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Using HTTP API
        )
        self.collection_name = "book_content"
        self.vector_size = 1536  # Assuming OpenAI embeddings, adjust as needed
        self.distance = Distance.COSINE
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist."""
        try:
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=self.distance
                    )
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")
            raise

    def upsert_vectors(self, points):
        """Upsert vectors to the collection."""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Upserted {len(points)} vectors to {self.collection_name}")
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            raise

    def search_vectors(self, query_vector, limit=10):
        """Search for similar vectors."""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            raise

    def delete_vectors(self, point_ids):
        """Delete vectors by point IDs."""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=point_ids
            )
            logger.info(f"Deleted {len(point_ids)} vectors from {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            raise

# Create a global instance
vector_db_service = VectorDBService()