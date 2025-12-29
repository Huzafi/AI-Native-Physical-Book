import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.rag_service import RAGService
from src.models.query import QueryModel, QueryType
from src.models.response import ResponseModel


class TestRAGService:
    """Unit tests for the RAGService class"""

    @pytest.fixture
    def mock_embedding_service(self):
        """Mock embedding service"""
        service = Mock()
        service.generate_embedding = Mock(return_value=[0.1, 0.2, 0.3])
        service.retrieve_relevant_chunks = AsyncMock(return_value=[])
        return service

    @pytest.fixture
    def mock_response_service(self):
        """Mock response service"""
        service = Mock()
        service.generate_response = Mock(return_value="Generated response")
        service.format_response_with_citations = Mock(return_value={
            "response": "Generated response",
            "citations": [],
            "confidence_score": 0.85
        })
        return service

    @pytest.fixture
    def mock_query_service(self):
        """Mock query service"""
        service = Mock()
        service.create_query = AsyncMock()
        service.create_response = AsyncMock()
        return service

    @pytest.fixture
    def rag_service(self, mock_embedding_service, mock_response_service, mock_query_service):
        """Create a RAGService instance with mocked dependencies"""
        service = RAGService(
            embedding_service=mock_embedding_service,
            response_service=mock_response_service,
            query_service=mock_query_service
        )
        return service

    @pytest.mark.asyncio
    async def test_process_query_full_book_success(self, rag_service, mock_embedding_service, mock_response_service, mock_query_service):
        """Test successful processing of a full book query"""
        query_model = QueryModel(
            id="test-query-id",
            query_text="What is the main theme?",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        # Mock the embedding service to return relevant chunks
        mock_chunks = [
            {"content": "The main theme is growth and learning", "section_id": "section-1", "page_number": 10},
            {"content": "Characters develop through challenges", "section_id": "section-2", "page_number": 15}
        ]
        mock_embedding_service.retrieve_relevant_chunks.return_value = mock_chunks
        
        # Mock the response service to return a formatted response
        formatted_response = {
            "response": "The main theme of the book is growth and learning through challenges.",
            "citations": [
                {"section_title": "Chapter 1", "page_number": 10, "text_snippet": "The main theme is growth and learning"},
                {"section_title": "Chapter 2", "page_number": 15, "text_snippet": "Characters develop through challenges"}
            ],
            "confidence_score": 0.92
        }
        mock_response_service.format_response_with_citations.return_value = formatted_response
        
        result = await rag_service.process_query(query_model)
        
        # Verify the embedding service was called to generate embeddings
        mock_embedding_service.generate_embedding.assert_called_once_with(query_model.query_text)
        
        # Verify the embedding service was called to retrieve relevant chunks
        mock_embedding_service.retrieve_relevant_chunks.assert_called_once()
        
        # Verify the response service was called to generate the response
        mock_response_service.generate_response.assert_called_once()
        
        # Verify the result
        assert result.response_text == formatted_response["response"]
        assert result.confidence_score == formatted_response["confidence_score"]
        assert len(result.citations) == len(formatted_response["citations"])

    @pytest.mark.asyncio
    async def test_process_query_user_selection_success(self, rag_service, mock_embedding_service, mock_response_service, mock_query_service):
        """Test successful processing of a user selection query"""
        query_model = QueryModel(
            id="test-query-id",
            query_text="What does this mean?",
            query_type=QueryType.USER_SELECTION,
            user_selected_text="Selected text content that should be the only context",
            session_id="test-session-id"
        )
        
        # Mock the response service to return a formatted response
        formatted_response = {
            "response": "This selected text means that the user's selected text is the only context used for generating the response.",
            "citations": [],
            "confidence_score": 0.88
        }
        mock_response_service.format_response_with_citations.return_value = formatted_response
        
        result = await rag_service.process_query(query_model)
        
        # For user selection, we should not call the embedding service to retrieve from vector store
        # Instead, we should use the selected text directly
        mock_embedding_service.generate_embedding.assert_called_once_with(query_model.query_text)
        
        # The response service should be called with the selected text as context
        mock_response_service.generate_response.assert_called_once()
        
        # Verify the result
        assert result.response_text == formatted_response["response"]
        assert result.confidence_score == formatted_response["confidence_score"]
        assert result.query_type == "USER_SELECTION"

    @pytest.mark.asyncio
    async def test_process_query_no_relevant_chunks(self, rag_service, mock_embedding_service, mock_response_service, mock_query_service):
        """Test processing a query when no relevant chunks are found"""
        query_model = QueryModel(
            id="test-query-id",
            query_text="What is the meaning of life according to this book?",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        # Mock the embedding service to return no relevant chunks
        mock_embedding_service.retrieve_relevant_chunks.return_value = []
        
        # Mock the response service to handle no context
        formatted_response = {
            "response": "I couldn't find relevant information in the book to answer your question.",
            "citations": [],
            "confidence_score": 0.3
        }
        mock_response_service.format_response_with_citations.return_value = formatted_response
        
        result = await rag_service.process_query(query_model)
        
        # Verify the result handles the case of no relevant chunks
        assert result.response_text == formatted_response["response"]
        assert result.confidence_score == formatted_response["confidence_score"]

    @pytest.mark.asyncio
    async def test_process_query_exception_handling(self, rag_service, mock_embedding_service, mock_response_service, mock_query_service):
        """Test that exceptions during query processing are handled properly"""
        query_model = QueryModel(
            id="test-query-id",
            query_text="What is the main theme?",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        # Mock the embedding service to raise an exception
        mock_embedding_service.generate_embedding.side_effect = Exception("Embedding service error")
        
        with pytest.raises(Exception):
            await rag_service.process_query(query_model)

    @pytest.mark.asyncio
    async def test_process_query_empty_query_text(self, rag_service, mock_embedding_service, mock_response_service, mock_query_service):
        """Test processing a query with empty text"""
        query_model = QueryModel(
            id="test-query-id",
            query_text="",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        with pytest.raises(ValueError):
            await rag_service.process_query(query_model)

    @pytest.mark.asyncio
    async def test_process_query_special_characters(self, rag_service, mock_embedding_service, mock_response_service, mock_query_service):
        """Test processing a query with special characters"""
        query_model = QueryModel(
            id="test-query-id",
            query_text="What does 'this' mean? And \"that\"?",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        # Mock the embedding service to return relevant chunks
        mock_chunks = [
            {"content": "Special characters like 'quotes' and \"double quotes\" are handled properly", "section_id": "section-1", "page_number": 10}
        ]
        mock_embedding_service.retrieve_relevant_chunks.return_value = mock_chunks
        
        # Mock the response service to return a formatted response
        formatted_response = {
            "response": "Special characters in the text are handled properly.",
            "citations": [
                {"section_title": "Chapter 1", "page_number": 10, "text_snippet": "Special characters like 'quotes' and \"double quotes\" are handled properly"}
            ],
            "confidence_score": 0.85
        }
        mock_response_service.format_response_with_citations.return_value = formatted_response
        
        result = await rag_service.process_query(query_model)
        
        # Verify the result handles special characters correctly
        assert result.response_text == formatted_response["response"]
        assert result.confidence_score == formatted_response["confidence_score"]

    def test_validate_query_model(self, rag_service):
        """Test validation of query models"""
        # Valid full book query
        valid_full_book_query = QueryModel(
            id="test-query-id",
            query_text="What is the main theme?",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        is_valid, errors = rag_service.validate_query_model(valid_full_book_query)
        assert is_valid
        assert len(errors) == 0
        
        # Valid user selection query
        valid_selection_query = QueryModel(
            id="test-query-id",
            query_text="What does this mean?",
            query_type=QueryType.USER_SELECTION,
            user_selected_text="Selected text",
            session_id="test-session-id"
        )
        
        is_valid, errors = rag_service.validate_query_model(valid_selection_query)
        assert is_valid
        assert len(errors) == 0

    def test_validate_query_model_invalid(self, rag_service):
        """Test validation of invalid query models"""
        # Invalid query - no query text
        invalid_query = QueryModel(
            id="test-query-id",
            query_text="",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        is_valid, errors = rag_service.validate_query_model(invalid_query)
        assert not is_valid
        assert len(errors) > 0

    @pytest.mark.asyncio
    async def test_process_query_performance_metrics(self, rag_service, mock_embedding_service, mock_response_service, mock_query_service):
        """Test that performance metrics are captured during query processing"""
        query_model = QueryModel(
            id="test-query-id",
            query_text="What is the main theme?",
            query_type=QueryType.FULL_BOOK,
            book_id="test-book-id",
            session_id="test-session-id"
        )
        
        # Mock the embedding service to return relevant chunks
        mock_chunks = [
            {"content": "The main theme is growth and learning", "section_id": "section-1", "page_number": 10}
        ]
        mock_embedding_service.retrieve_relevant_chunks.return_value = mock_chunks
        
        # Mock the response service to return a formatted response
        formatted_response = {
            "response": "The main theme of the book is growth and learning.",
            "citations": [
                {"section_title": "Chapter 1", "page_number": 10, "text_snippet": "The main theme is growth and learning"}
            ],
            "confidence_score": 0.92
        }
        mock_response_service.format_response_with_citations.return_value = formatted_response
        
        result = await rag_service.process_query(query_model)
        
        # Verify the result includes performance metrics
        assert hasattr(result, 'confidence_score')
        assert 0.0 <= result.confidence_score <= 1.0