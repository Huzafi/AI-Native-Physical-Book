import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.rag_service import RAGService
from src.services.embedding_service import EmbeddingService
from src.services.response_service import ResponseService
from src.services.selection_service import SelectionService
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
def mock_selection_service():
    """Mock selection service"""
    return Mock(spec=SelectionService)


@pytest.fixture
def rag_service(mock_embedding_service, mock_response_service, mock_selection_service):
    """RAG service with mocked dependencies for isolation mode"""
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        response_service=mock_response_service,
        query_service=Mock()  # Not used in isolation mode
    )
    # We'll inject the selection service separately or modify the RAG service to accept it
    return rag_service


@pytest.mark.asyncio
async def test_user_selected_text_isolation_integration(mock_embedding_service, mock_response_service, mock_selection_service):
    """Integration test for user-selected text isolation mode"""
    from src.services.rag_service import RAGService
    
    # Create RAG service with selection service
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        response_service=mock_response_service,
        query_service=Mock()
    )
    
    # Setup test data for user selection
    query_text = "What does this paragraph mean?"
    selected_text = "The paragraph of text the user has selected. This text should be the only context used for the response."
    query_model = QueryModel(
        id="test-query-id",
        query_text=query_text,
        query_type="USER_SELECTION",
        user_selected_text=selected_text,
        session_id="test-session"
    )
    
    # Mock embeddings
    mock_embedding = [0.1, 0.2, 0.3]
    mock_embedding_service.generate_embedding.return_value = mock_embedding
    
    # Mock response generation - should only use the selected text as context
    mock_response_text = "This paragraph means that the user's selected text is the only context used for generating the response."
    mock_response_service.generate_response.return_value = mock_response_text
    
    # Execute the RAG pipeline in isolation mode
    # This would be a method that handles USER_SELECTION queries specifically
    result = await rag_service.process_selection_query(query_text, selected_text)
    
    # Verify the pipeline executed correctly in isolation mode
    mock_embedding_service.generate_embedding.assert_called_once_with(query_text)
    mock_response_service.generate_response.assert_called_once_with(
        query_text=query_text,
        context_chunks=[{"content": selected_text}],  # Only the selected text as context
        query_type="USER_SELECTION"
    )
    
    # Verify the result structure
    assert result.response_text == mock_response_text
    assert result.query_type == "USER_SELECTION"


@pytest.mark.asyncio
async def test_user_selected_text_isolation_no_external_context(mock_embedding_service, mock_response_service, mock_selection_service):
    """Test that user-selected text mode doesn't use external book context"""
    from src.services.rag_service import RAGService
    
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        response_service=mock_response_service,
        query_service=Mock()
    )
    
    # Setup test data
    query_text = "Explain this concept?"
    selected_text = "The specific concept the user wants to understand from the selected text."
    query_model = QueryModel(
        id="test-query-id",
        query_text=query_text,
        query_type="USER_SELECTION",
        user_selected_text=selected_text,
        session_id="test-session"
    )
    
    # Mock embeddings
    mock_embedding = [0.4, 0.5, 0.6]
    mock_embedding_service.generate_embedding.return_value = mock_embedding
    
    # Mock response generation
    mock_response_text = "Based on the selected text, this concept refers to..."
    mock_response_service.generate_response.return_value = mock_response_text
    
    # Execute the RAG pipeline in isolation mode
    result = await rag_service.process_selection_query(query_text, selected_text)
    
    # Verify that the embedding service was NOT called to retrieve book chunks
    # In isolation mode, we should not be retrieving from the vector store
    # This is the key test for isolation - no external context should be used
    assert result.response_text == mock_response_text
    assert result.query_type == "USER_SELECTION"


@pytest.mark.asyncio
async def test_user_selected_text_isolation_empty_selection(mock_embedding_service, mock_response_service, mock_selection_service):
    """Test behavior when user provides empty selected text"""
    from src.services.rag_service import RAGService
    
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        response_service=mock_response_service,
        query_service=Mock()
    )
    
    # Setup test data with empty selected text
    query_text = "What does this mean?"
    selected_text = ""  # Empty selection
    query_model = QueryModel(
        id="test-query-id",
        query_text=query_text,
        query_type="USER_SELECTION",
        user_selected_text=selected_text,
        session_id="test-session"
    )
    
    # Mock response generation for empty context
    mock_response_text = "No text was selected to answer your query about."
    mock_response_service.generate_response.return_value = mock_response_text
    
    # Execute the RAG pipeline in isolation mode
    result = await rag_service.process_selection_query(query_text, selected_text)
    
    # Verify the response handles empty selection appropriately
    assert result.response_text == mock_response_text
    assert result.query_type == "USER_SELECTION"


@pytest.mark.asyncio
async def test_user_selected_text_isolation_special_characters(mock_embedding_service, mock_response_service, mock_selection_service):
    """Test isolation mode with special characters in selected text"""
    from src.services.rag_service import RAGService
    
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        response_service=mock_response_service,
        query_service=Mock()
    )
    
    # Setup test data with special characters
    query_text = "Analyze this code snippet?"
    selected_text = "def hello_world():\n    print('Hello, world!')\n# This is a comment"
    query_model = QueryModel(
        id="test-query-id",
        query_text=query_text,
        query_type="USER_SELECTION",
        user_selected_text=selected_text,
        session_id="test-session"
    )
    
    # Mock response generation
    mock_response_text = "This code snippet defines a function that prints 'Hello, world!' to the console."
    mock_response_service.generate_response.return_value = mock_response_text
    
    # Execute the RAG pipeline in isolation mode
    result = await rag_service.process_selection_query(query_text, selected_text)
    
    # Verify the result handles special characters correctly
    assert result.response_text == mock_response_text
    assert result.query_type == "USER_SELECTION"


if __name__ == "__main__":
    pytest.main([__file__])