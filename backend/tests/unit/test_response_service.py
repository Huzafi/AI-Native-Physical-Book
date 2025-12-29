import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.response_service import ResponseService


class TestResponseService:
    """Unit tests for the ResponseService class"""

    @pytest.fixture
    def mock_cohere_client(self):
        """Mock Cohere client"""
        mock_client = Mock()
        mock_client.generate = Mock(return_value=Mock(text="Generated response"))
        return mock_client

    @pytest.fixture
    def response_service(self, mock_cohere_client):
        """Create a ResponseService instance with mocked dependencies"""
        service = ResponseService(cohere_client=mock_cohere_client)
        return service

    def test_generate_response_success(self, response_service, mock_cohere_client):
        """Test successful response generation"""
        query_text = "What is the main theme?"
        context_chunks = [
            {"content": "The main theme is about growth and learning", "section_id": "section-1", "page_number": 10},
            {"content": "Characters develop through challenges", "section_id": "section-2", "page_number": 15}
        ]
        query_type = "FULL_BOOK"
        
        result = response_service.generate_response(
            query_text=query_text,
            context_chunks=context_chunks,
            query_type=query_type
        )
        
        # Verify the Cohere client was called
        assert mock_cohere_client.generate.called
        
        # Verify the result
        assert result == "Generated response"

    def test_generate_response_with_empty_context(self, response_service, mock_cohere_client):
        """Test response generation with empty context"""
        query_text = "What is the meaning of life?"
        context_chunks = []
        query_type = "FULL_BOOK"
        
        result = response_service.generate_response(
            query_text=query_text,
            context_chunks=context_chunks,
            query_type=query_type
        )
        
        # Should still generate a response even with no context
        assert result == "Generated response"

    def test_generate_response_user_selection(self, response_service, mock_cohere_client):
        """Test response generation for user selection query"""
        query_text = "What does this mean?"
        context_chunks = [{"content": "User selected text content"}]
        query_type = "USER_SELECTION"
        
        result = response_service.generate_response(
            query_text=query_text,
            context_chunks=context_chunks,
            query_type=query_type
        )
        
        # Verify the Cohere client was called
        assert mock_cohere_client.generate.called
        
        # Verify the result
        assert result == "Generated response"

    def test_format_response_with_citations(self, response_service):
        """Test response formatting with citations"""
        response_text = "This is the answer based on the book content."
        context_chunks = [
            {"content": "The main theme is growth", "section_id": "section-1", "page_number": 10, "section_title": "Chapter 1"},
            {"content": "Learning happens through challenges", "section_id": "section-2", "page_number": 15, "section_title": "Chapter 2"}
        ]
        
        formatted_response = response_service.format_response_with_citations(
            response_text=response_text,
            context_chunks=context_chunks
        )
        
        # Verify the response text is preserved
        assert response_text in formatted_response["response"]
        
        # Verify citations are included
        assert len(formatted_response["citations"]) == 2

    def test_format_response_with_citations_empty_chunks(self, response_service):
        """Test response formatting with empty context chunks"""
        response_text = "This is the answer."
        context_chunks = []
        
        formatted_response = response_service.format_response_with_citations(
            response_text=response_text,
            context_chunks=context_chunks
        )
        
        # Verify the response text is preserved
        assert formatted_response["response"] == response_text
        
        # Verify no citations are included
        assert len(formatted_response["citations"]) == 0

    def test_format_response_with_citations_missing_fields(self, response_service):
        """Test response formatting when context chunks have missing fields"""
        response_text = "This is the answer based on the book content."
        context_chunks = [
            {"content": "The main theme is growth", "section_id": "section-1"},  # Missing page_number and section_title
            {"content": "Learning happens through challenges", "page_number": 15}  # Missing section_id and section_title
        ]
        
        formatted_response = response_service.format_response_with_citations(
            response_text=response_text,
            context_chunks=context_chunks
        )
        
        # Verify the response text is preserved
        assert response_text in formatted_response["response"]
        
        # Verify citations are included with default values for missing fields
        assert len(formatted_response["citations"]) == 2

    def test_calculate_confidence_score(self, response_service):
        """Test confidence score calculation"""
        # This would depend on the specific implementation
        # For now, we'll test that it returns a float between 0 and 1
        context_chunks = [
            {"content": "The main theme is growth", "section_id": "section-1", "page_number": 10},
            {"content": "Learning happens through challenges", "section_id": "section-2", "page_number": 15}
        ]
        
        confidence = response_service.calculate_confidence_score(context_chunks)
        
        # Verify it's a float
        assert isinstance(confidence, float)
        
        # Verify it's between 0 and 1
        assert 0.0 <= confidence <= 1.0

    def test_calculate_confidence_score_empty_chunks(self, response_service):
        """Test confidence score calculation with empty chunks"""
        confidence = response_service.calculate_confidence_score([])
        
        # Should return a low confidence for empty context
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0