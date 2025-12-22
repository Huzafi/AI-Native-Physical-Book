from typing import List, Dict, Any, Optional
from app.services.vector_db import vector_db_service
from app.services.search_service import search_service
from app.services.content_service import content_service
from sqlalchemy.orm import Session
import logging
import uuid
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Initialize sentence transformer model for embeddings
        # In a real implementation, you might use OpenAI embeddings or another service
        try:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model for embeddings
        except Exception as e:
            logger.warning(f"Could not initialize sentence transformer: {e}")
            self.encoder = None

    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using sentence transformer."""
        if self.encoder:
            embedding = self.encoder.encode([text])
            return embedding[0].tolist()  # Convert to list for JSON serialization
        else:
            # Fallback: return a zero vector of appropriate size
            return [0.0] * 384  # Size of all-MiniLM-L6-v2 embeddings

    def index_content_for_rag(self, db: Session, content_id: str, content_text: str, metadata: Dict[str, Any] = None) -> bool:
        """Index content for RAG using vector database."""
        try:
            # Chunk the content into smaller pieces for better retrieval
            chunks = self._chunk_content(content_text)

            points = []
            for i, chunk in enumerate(chunks):
                # Generate embedding for the chunk
                embedding = self.generate_embeddings(chunk)

                # Create a unique ID for this chunk
                chunk_id = f"{content_id}_chunk_{i}"

                # Create a Qdrant point
                point = models.PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "content_id": content_id,
                        "chunk_text": chunk,
                        "chunk_index": i,
                        "metadata": metadata or {}
                    }
                )
                points.append(point)

            # Upsert points to vector database
            vector_db_service.upsert_vectors(points)
            logger.info(f"Indexed {len(chunks)} chunks for content {content_id}")
            return True
        except Exception as e:
            logger.error(f"Error indexing content {content_id} for RAG: {str(e)}")
            return False

    def _chunk_content(self, text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
        """Chunk content into smaller pieces."""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # If we're not at the end, try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings near the end
                sentence_end = max(text.rfind('.', start, end),
                                 text.rfind('!', start, end),
                                 text.rfind('?', start, end))

                if sentence_end > start + chunk_size // 2:  # Only break if it's not too early
                    end = sentence_end + 1
                else:
                    # If no sentence end found, break at word boundary
                    word_end = text.rfind(' ', start + chunk_size // 2, end)
                    if word_end > start:
                        end = word_end

            chunks.append(text[start:end].strip())
            start = end - overlap if end < len(text) else end

            # Ensure we're making progress
            if start == end:
                start += chunk_size

        return [chunk for chunk in chunks if chunk]  # Filter out empty chunks

    def retrieve_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query using vector search."""
        try:
            # Generate embedding for the query
            query_embedding = self.generate_embeddings(query)

            # Search in vector database
            results = vector_db_service.search_vectors(query_embedding, limit=limit)

            # Format results
            contexts = []
            for result in results:
                contexts.append({
                    "content_id": result.payload.get("content_id"),
                    "chunk_text": result.payload.get("chunk_text"),
                    "relevance_score": result.score,  # Cosine similarity score
                    "metadata": result.payload.get("metadata", {})
                })

            return contexts
        except Exception as e:
            logger.error(f"Error retrieving context for query '{query}': {str(e)}")
            return []

    def generate_answer(self, query: str, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate an answer based on query and retrieved contexts."""
        try:
            # Combine contexts into a single context string
            context_text = "\n\n".join([ctx["chunk_text"] for ctx in contexts])

            # In a real implementation, you would use an LLM like OpenAI GPT to generate the answer
            # For this implementation, we'll create a simple response based on the context

            # Simple answer generation (in real implementation, use an LLM)
            answer = self._simple_answer_generation(query, context_text)

            # Calculate confidence based on context relevance
            avg_relevance = np.mean([ctx["relevance_score"] for ctx in contexts]) if contexts else 0.0

            return {
                "answer": answer,
                "sources": [
                    {
                        "content_id": ctx["content_id"],
                        "title": ctx["metadata"].get("title", "Unknown Title"),
                        "url_path": ctx["metadata"].get("url_path", ""),
                        "relevance_score": ctx["relevance_score"]
                    }
                    for ctx in contexts
                ],
                "confidence": float(avg_relevance)
            }
        except Exception as e:
            logger.error(f"Error generating answer for query '{query}': {str(e)}")
            return {
                "answer": "Sorry, I couldn't generate an answer for your question.",
                "sources": [],
                "confidence": 0.0
            }

    def _simple_answer_generation(self, query: str, context: str) -> str:
        """Simple answer generation (placeholder for actual LLM)."""
        # This is a placeholder implementation
        # In a real implementation, you would use an LLM like OpenAI's API
        return f"Based on the provided context, here's an answer to your question '{query}': The context contains relevant information that addresses your query. For more details, please refer to the provided sources."

    def answer_question(self, db: Session, question: str, context_content_id: Optional[str] = None) -> Dict[str, Any]:
        """Answer a question using RAG approach."""
        try:
            # Retrieve relevant context
            contexts = self.retrieve_context(question)

            # If specific content ID is provided, filter contexts to that content
            if context_content_id:
                contexts = [ctx for ctx in contexts if ctx["content_id"] == context_content_id]

            # If no contexts found, provide a graceful fallback
            if not contexts:
                return {
                    "answer": "I couldn't find relevant information in the book to answer your question. Please try rephrasing your question or check other sections of the book.",
                    "sources": [],
                    "confidence": 0.1  # Low confidence when no context found
                }

            # Generate answer based on contexts
            result = self.generate_answer(question, contexts)

            return result
        except Exception as e:
            logger.error(f"Error answering question '{question}': {str(e)}")
            return {
                "answer": "Sorry, I'm having trouble answering your question right now. The AI service may be temporarily unavailable. Please try again later.",
                "sources": [],
                "confidence": 0.0
            }

# Create a global instance
rag_service = RAGService()