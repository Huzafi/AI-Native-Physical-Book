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
            search_results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=5,  # Get top 5 most relevant results
                with_payload=True,
            )

            # Extract content from search results
            contexts = []
            results_metadata = []

            for result in search_results:
                if result.payload:
                    content = result.payload.get('text', '') or result.payload.get('content', '')
                    metadata = {
                        'id': result.id,
                        'score': result.score,
                        'payload': result.payload
                    }
                    contexts.append(content)
                    results_metadata.append(metadata)

            # Prepare context for Cohere
            context_text = "\n\n".join(contexts) if contexts else "No relevant context found in the book."

            # Generate response using Cohere
            if contexts:
                prompt = f"""
                Based on the following context from the book, please answer the question.
                If the context doesn't contain enough information to answer the question, please say so.

                Context:
                {context_text}

                Question: {query}

                Answer:
                """
            else:
                prompt = f"""
                The system couldn't find any relevant information in the book to answer the question: {query}
                Please acknowledge that you couldn't find relevant information in the provided book content.
                """

            response = self.cohere_client.generate(
                model='command-r-plus',  # Using a powerful model for better responses
                prompt=prompt,
                max_tokens=500,
                temperature=0.7,
                stop_sequences=["\n\n"]
            )

            generated_text = response.generations[0].text.strip()

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
            self.cohere_client.generate(
                model='command-r-plus',
                prompt="Say 'health check successful'",
                max_tokens=10
            )

            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False