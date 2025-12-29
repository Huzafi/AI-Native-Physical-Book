"""Embedding generation and storage service for the RAG Chatbot application."""

from typing import List, Dict, Any
from src.config.cohere_config import generate_embeddings
from src.config.qdrant_config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating and storing embeddings."""
    
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        self.collection_name = QDRANT_COLLECTION_NAME
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        try:
            embeddings = generate_embeddings(texts)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise e
    
    def store_embeddings(self, texts: List[str], metadata: List[Dict[str, Any]] = None) -> List[str]:
        """Store embeddings in Qdrant and return the IDs."""
        try:
            # Generate embeddings
            embeddings = self.generate_embeddings(texts)
            
            # Create collection if it doesn't exist
            try:
                self.qdrant_client.get_collection(self.collection_name)
            except:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=len(embeddings[0]) if embeddings else 384, distance=models.Distance.COSINE),
                )
            
            # Prepare points for upsert
            points = []
            ids = []
            for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                point_id = str(uuid.uuid4())
                ids.append(point_id)
                
                payload = {
                    "text": text,
                    "created_at": str("datetime.utcnow()")  # Using string representation
                }
                
                # Add additional metadata if provided
                if metadata and i < len(metadata):
                    payload.update(metadata[i])
                
                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )
                )
            
            # Store embeddings in Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Stored {len(points)} embeddings in Qdrant")
            return ids
            
        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            raise e
    
    def search_similar(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar texts using the query text."""
        try:
            # Generate embedding for the query
            query_embeddings = self.generate_embeddings([query_text])
            query_vector = query_embeddings[0] if query_embeddings else []
            
            if not query_vector:
                logger.warning("Could not generate embedding for query")
                return []
            
            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
            )
            
            # Extract relevant information from results
            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "text": result.payload.get("text", ""),
                    "score": result.score,
                    "payload": result.payload
                })
            
            logger.info(f"Found {len(results)} similar texts for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching for similar texts: {str(e)}")
            raise e
    
    def delete_embeddings(self, ids: List[str]):
        """Delete embeddings by their IDs."""
        try:
            self.qdrant_client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=ids
                )
            )
            logger.info(f"Deleted {len(ids)} embeddings from Qdrant")
        except Exception as e:
            logger.error(f"Error deleting embeddings: {str(e)}")
            raise e


# Singleton instance
embedding_service = EmbeddingService()