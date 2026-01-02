import logging
from typing import List, Dict, Any, Optional
import cohere
from qdrant_client import QdrantClient
from src.config.qdrant_config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
from src.config.cohere_config import settings as cohere_settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
        self.cohere_client = cohere.Client(api_key=cohere_settings.cohere_api_key)
        self.collection_name = QDRANT_COLLECTION_NAME

    async def search_and_generate(self, query: str) -> Dict[str, Any]:
        """
        Search Qdrant for relevant documents and generate a response using Cohere
        """
        try:
            from qdrant_client.http import models
            from src.config.cohere_config import generate_embeddings

            # Check if this is a general book query (summary, overview, about, etc.)
            query_lower = query.lower().strip()
            is_general_book_query = any(
                keyword in query_lower
                for keyword in ['summary', 'overview', 'introduction', 'about this book', 'about the book', 'book summary', 'what is this book about', 'book overview']
            )

            # Generate embedding for the query
            query_embeddings = generate_embeddings([query])
            query_vector = query_embeddings[0] if query_embeddings else []

            if not query_vector:
                logger.warning("Could not generate embedding for query")
                return {
                    "answer": "Could not process your query due to embedding generation issue.",
                    "results": []
                }

            # Search in Qdrant using the vector with the new API
            # For general book queries, get more results to provide a comprehensive view
            limit = 10 if is_general_book_query else 5
            search_response = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True,
            )

            # Extract content from search results - the response is a named tuple-like object
            contexts = []
            results_metadata = []

            # Handle the response format properly
            # The response has a 'points' attribute containing the search results
            if hasattr(search_response, 'points'):
                search_results = search_response.points
            else:
                # Fallback if the response format is different
                search_results = search_response

            for result in search_results:
                # Handle both new and old API response formats
                if hasattr(result, 'payload'):
                    payload = result.payload
                elif isinstance(result, dict) and 'payload' in result:
                    payload = result['payload']
                elif hasattr(result, '_payload'):
                    payload = result._payload
                else:
                    continue  # Skip if we can't extract payload

                if payload:
                    content = payload.get('text', '') or payload.get('content', '')
                    metadata = {
                        'id': result.id if hasattr(result, 'id') else getattr(result, 'payload', {}).get('id', 'unknown'),
                        'score': result.score if hasattr(result, 'score') else getattr(result, 'score', 0),
                        'payload': payload
                    }
                    contexts.append(content)
                    results_metadata.append(metadata)

            # Prepare context for Cohere
            context_text = "\n\n".join(contexts) if contexts else "No relevant context found in the book."

            # Generate response using Cohere Chat API
            if contexts:
                if is_general_book_query:
                    # For general book queries, ask the model to provide a comprehensive summary or overview
                    message = f"""
                    Based on the following content from the book, please provide a comprehensive summary or overview of the book.
                    Focus on the main topics, themes, and key points covered in the book.

                    Book Content:
                    {context_text}

                    Please provide a summary of the book based on the above content.
                    """
                else:
                    # For specific queries, use the standard approach
                    message = f"""
                    Based on the following context from the book, please answer the question.
                    If the context doesn't contain enough information to answer the question, please say so.

                    Context:
                    {context_text}

                    Question: {query}

                    Answer:
                    """
            else:
                message = f"""
                The system couldn't find any relevant information in the book to answer the question: {query}
                Please acknowledge that you couldn't find relevant information in the provided book content.
                """

            response = self.cohere_client.chat(
                model='command-r-08-2024',  # Using a specific version of command-r
                message=message,
                max_tokens=1000,  # Increase token limit for book summaries
                temperature=0.7
            )

            generated_text = response.text.strip()

            return {
                "answer": generated_text,
                "results": results_metadata
            }

        except Exception as e:
            logger.error(f"Error in search_and_generate: {str(e)}")
            # Return a structured error response instead of raising the exception
            return {
                "answer": f"An error occurred while processing your query: {str(e)}",
                "results": []
            }

    async def health_check(self) -> bool:
        """
        Check if Qdrant and Cohere services are accessible
        """
        try:
            # Test Qdrant connection
            self.qdrant_client.get_collection(self.collection_name)

            # Test Cohere connection by making a simple request
            self.cohere_client.chat(
                model='command-r-08-2024',
                message="Say 'health check successful'",
                max_tokens=10
            )

            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False