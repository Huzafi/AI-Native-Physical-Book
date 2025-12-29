"""Cohere API integration for the RAG Chatbot application."""

import cohere
from pydantic_settings import BaseSettings
import os
from typing import List, Optional


class CohereSettings(BaseSettings):
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from .env that don't match class fields


# Create settings instance
settings = CohereSettings()

# Initialize Cohere client
co = cohere.Client(api_key=settings.cohere_api_key)


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Cohere API.
    
    Args:
        texts: List of texts to generate embeddings for
        
    Returns:
        List of embedding vectors
    """
    response = co.embed(
        texts=texts,
        model='embed-english-v3.0',  # Using Cohere's latest embedding model
        input_type='search_document'  # Specify the type of input for better embeddings
    )
    return [embedding for embedding in response.embeddings]


def generate_text(prompt: str, max_tokens: int = 500) -> str:
    """
    Generate text using Cohere's generation API.
    
    Args:
        prompt: Input prompt for text generation
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        Generated text
    """
    response = co.generate(
        model='command-r',  # Using Cohere's command model for generation
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    
    return response.generations[0].text


def rerank_documents(query: str, documents: List[str], top_n: int = 5) -> List[dict]:
    """
    Rerank documents based on relevance to the query using Cohere's rerank API.
    
    Args:
        query: The search query
        documents: List of documents to rerank
        top_n: Number of top results to return
        
    Returns:
        List of reranked documents with relevance scores
    """
    response = co.rerank(
        model='rerank-english-v2.0',
        query=query,
        documents=documents,
        top_n=top_n
    )
    
    return response.results