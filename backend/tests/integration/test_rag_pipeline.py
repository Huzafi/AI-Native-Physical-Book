import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.rag_service import RAGService
from src.services.embedding_service import EmbeddingService
from src.services.response_service import ResponseService
from src.services.query_service import QueryService
from src.models.query import QueryModel
from src.models.response import ResponseModel


@pytest.fixture
def mock_embedding_service():
    """Mock embedding service"""
    return Mock(spec=EmbeddingService)


@pytest.fixture
def mock_response_service():
    """Mock response service"""
    return Mock(spec=ResponseService)


@pytest.fixture
def mock_query_service():
    """Mock query service"""
    return Mock(spec=QueryService)


@pytest.fixture
def rag_service(mock_embedding_service, mock_response_service, mock_query_service):
    """RAG service with mocked dependencies"""
    return RAGService(
        embedding_service=mock_embedding_service,
        response_service=mock_response_service,
        query_service=mock_query_service
    )


@pytest.mark.asyncio
async def test_full_book_rag_pipeline_integration(rag_service, mock_embedding_service, mock_response_service, mock_query_service):
    """Integration test for the full-book RAG pipeline"""
    # Setup test data
    query_text = "What is the main theme of this book?"
    book_id = "test-book-uuid"
    query_model = QueryModel(
        id="test-query-id",
        query_text=query_text,
        query_type="FULL_BOOK",
        book_id=book_id,
        session_id="test-session"
    )
    
    # Mock embeddings
    mock_embedding = [0.1, 0.2, 0.3]
    mock_embedding_service.generate_embedding.return_value = mock_embedding
    
    # Mock retrieved chunks
    mock_chunks = [
        {"id": "chunk-1", "content": "The main theme is about growth and learning", "section_id": "section-1", "page_number": 10},
        {"id": "chunk-2", "content": "Characters develop through challenges", "section_id": "section-2", "page_number": 15}
    ]
    mock_embedding_service.retrieve_relevant_chunks.return_value = mock_chunks
    
    # Mock response generation
    mock_response_text = "The main theme of the book is about growth and learning through challenges."
    mock_response_service.generate_response.return_value = mock_response_text
    
    # Execute the RAG pipeline
    result = await rag_service.process_query(query_model)
    
    # Verify the pipeline executed correctly
    mock_embedding_service.generate_embedding.assert_called_once_with(query_text)
    mock_embedding_service.retrieve_relevant_chunks.assert_called_once_with(
        query_embedding=mock_embedding,
        book_id=book_id,
        query_type="FULL_BOOK"
    )
    mock_response_service.generate_response.assert_called_once_with(
        query_text=query_text,
        context_chunks=mock_chunks,
        query_type="FULL_BOOK"
    )
    
    # Verify the result structure
    assert isinstance(result, ResponseModel)
    assert result.query_id == query_model.id
    assert result.response_text == mock_response_text
    assert result.query_type == "FULL_BOOK"


@pytest.mark.asyncio
async def test_full_book_rag_pipeline_with_citations(rag_service, mock_embedding_service, mock_response_service, mock_query_service):
    """Test the full-book RAG pipeline with citation generation"""
    # Setup test data
    query_text = "What does the author say about character development?"
    book_id = "test-book-uuid"
    query_model = QueryModel(
        id="test-query-id",
        query_text=query_text,
        query_type="FULL_BOOK",
        book_id=book_id,
        session_id="test-session"
    )
    
    # Mock embeddings and chunks
    mock_embedding = [0.4, 0.5, 0.6]
    mock_embedding_service.generate_embedding.return_value = mock_embedding
    
    mock_chunks = [
        {"id": "chunk-3", "content": "Character development happens through conflict", "section_id": "section-3", "page_number": 25},
        {"id": "chunk-4", "content": "Characters must overcome obstacles", "section_id": "section-4", "page_number": 30}
    ]
    mock_embedding_service.retrieve_relevant_chunks.return_value = mock_chunks
    
    # Mock response generation
    mock_response_text = "The author states that character development happens through conflict and overcoming obstacles."
    mock_response_service.generate_response.return_value = mock_response_text
    
    # Execute the RAG pipeline
    result = await rag_service.process_query(query_model)
    
    # Verify the result includes citation information
    assert result.response_text == mock_response_text
    # The citations would be generated based on the chunks retrieved
    # This would be handled by the response service or a dedicated citation service


@pytest.mark.asyncio
async def test_full_book_rag_pipeline_no_relevant_chunks(rag_service, mock_embedding_service, mock_response_service, mock_query_service):
    """Test the RAG pipeline when no relevant chunks are found"""
    # Setup test data
    query_text = "What is the meaning of life according to this book?"
    book_id = "test-book-uuid"
    query_model = QueryModel(
        id="test-query-id",
        query_text=query_text,
        query_type="FULL_BOOK",
        book_id=book_id,
        session_id="test-session"
    )
    
    # Mock embeddings and no chunks found
    mock_embedding = [0.7, 0.8, 0.9]
    mock_embedding_service.generate_embedding.return_value = mock_embedding
    mock_embedding_service.retrieve_relevant_chunks.return_value = []
    
    # Mock response generation for no context
    mock_response_text = "I couldn't find relevant information in the book to answer your question."
    mock_response_service.generate_response.return_value = mock_response_text
    
    # Execute the RAG pipeline
    result = await rag_service.process_query(query_model)
    
    # Verify the pipeline handled the case of no relevant chunks
    mock_embedding_service.retrieve_relevant_chunks.assert_called_once_with(
        query_embedding=mock_embedding,
        book_id=book_id,
        query_type="FULL_BOOK"
    )
    mock_response_service.generate_response.assert_called_once_with(
        query_text=query_text,
        context_chunks=[],
        query_type="FULL_BOOK"
    )
    
    assert result.response_text == mock_response_text


if __name__ == "__main__":
    pytest.main([__file__])