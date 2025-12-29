import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.query_service import QueryService
from src.models.query import QueryModel, QueryType


class TestQueryService:
    """Unit tests for the QueryService class"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        session = Mock()
        session.add = Mock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()
        return session

    @pytest.fixture
    def query_service(self):
        """Create a QueryService instance"""
        service = QueryService()
        return service

    @pytest.mark.asyncio
    async def test_create_query_success(self, query_service, mock_db_session):
        """Test successful creation of a query"""
        query_data = {
            "query_text": "What is the main theme?",
            "query_type": QueryType.FULL_BOOK,
            "book_id": "test-book-id",
            "session_id": "test-session-id"
        }
        
        query = await query_service.create_query(mock_db_session, **query_data)
        
        # Verify the query was created with correct attributes
        assert query.query_text == query_data["query_text"]
        assert query.query_type == query_data["query_type"]
        assert query.book_id == query_data["book_id"]
        assert query.session_id == query_data["session_id"]
        
        # Verify the session methods were called
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_query_with_selected_text(self, query_service, mock_db_session):
        """Test creation of a query with selected text"""
        query_data = {
            "query_text": "What does this mean?",
            "query_type": QueryType.USER_SELECTION,
            "user_selected_text": "Selected text content",
            "session_id": "test-session-id"
        }
        
        query = await query_service.create_query(mock_db_session, **query_data)
        
        # Verify the query was created with correct attributes
        assert query.query_text == query_data["query_text"]
        assert query.query_type == query_data["query_type"]
        assert query.user_selected_text == query_data["user_selected_text"]
        assert query.session_id == query_data["session_id"]
        
        # Verify the session methods were called
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_query_missing_required_fields(self, query_service, mock_db_session):
        """Test query creation with missing required fields"""
        query_data = {
            # Missing query_text
            "query_type": QueryType.FULL_BOOK,
            "book_id": "test-book-id",
            "session_id": "test-session-id"
        }
        
        with pytest.raises(ValueError):
            await query_service.create_query(mock_db_session, **query_data)

    @pytest.mark.asyncio
    async def test_get_query_by_id_success(self, query_service, mock_db_session):
        """Test successful retrieval of a query by ID"""
        query_id = "test-query-id"
        mock_query = Mock(spec=QueryModel)
        mock_query.id = query_id
        mock_query.query_text = "Test query"
        
        # Mock the query filter
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_query
        
        result = await query_service.get_query_by_id(mock_db_session, query_id)
        
        # Verify the result
        assert result == mock_query
        mock_db_session.query.assert_called_once()
        mock_db_session.query.return_value.filter.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_query_by_id_not_found(self, query_service, mock_db_session):
        """Test retrieval of a non-existent query"""
        query_id = "nonexistent-query-id"
        
        # Mock the query filter to return None
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = await query_service.get_query_by_id(mock_db_session, query_id)
        
        # Verify the result is None
        assert result is None

    @pytest.mark.asyncio
    async def test_create_response_success(self, query_service, mock_db_session):
        """Test successful creation of a response"""
        response_data = {
            "query_id": "test-query-id",
            "response_text": "This is the response",
            "citations": [{"section_title": "Chapter 1", "page_number": 5, "text_snippet": "Relevant text"}],
            "confidence_score": 0.95
        }
        
        response = await query_service.create_response(mock_db_session, **response_data)
        
        # Verify the response was created with correct attributes
        assert response.query_id == response_data["query_id"]
        assert response.response_text == response_data["response_text"]
        assert response.citations == response_data["citations"]
        assert response.confidence_score == response_data["confidence_score"]
        
        # Verify the session methods were called
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_response_invalid_confidence(self, query_service, mock_db_session):
        """Test response creation with invalid confidence score"""
        response_data = {
            "query_id": "test-query-id",
            "response_text": "This is the response",
            "citations": [],
            "confidence_score": 1.5  # Invalid confidence score > 1
        }
        
        # Should handle invalid confidence scores appropriately
        response = await query_service.create_response(mock_db_session, **response_data)
        
        # Verify the response was created
        assert response.query_id == response_data["query_id"]
        assert response.response_text == response_data["response_text"]

    @pytest.mark.asyncio
    async def test_get_response_by_query_id_success(self, query_service, mock_db_session):
        """Test successful retrieval of a response by query ID"""
        query_id = "test-query-id"
        mock_response = Mock()
        mock_response.query_id = query_id
        mock_response.response_text = "Test response"
        
        # Mock the query filter
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_response
        
        result = await query_service.get_response_by_query_id(mock_db_session, query_id)
        
        # Verify the result
        assert result == mock_response
        mock_db_session.query.assert_called_once()
        mock_db_session.query.return_value.filter.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_response_by_query_id_not_found(self, query_service, mock_db_session):
        """Test retrieval of a response for a query that has no response"""
        query_id = "query-without-response"
        
        # Mock the query filter to return None
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = await query_service.get_response_by_query_id(mock_db_session, query_id)
        
        # Verify the result is None
        assert result is None

    def test_validate_query_data_full_book(self, query_service):
        """Test validation of query data for full book queries"""
        query_data = {
            "query_text": "What is the main theme?",
            "query_type": QueryType.FULL_BOOK,
            "book_id": "test-book-id",
            "session_id": "test-session-id"
        }
        
        is_valid, errors = query_service.validate_query_data(query_data)
        
        # Should be valid
        assert is_valid
        assert len(errors) == 0

    def test_validate_query_data_user_selection(self, query_service):
        """Test validation of query data for user selection queries"""
        query_data = {
            "query_text": "What does this mean?",
            "query_type": QueryType.USER_SELECTION,
            "user_selected_text": "Selected text content",
            "session_id": "test-session-id"
        }
        
        is_valid, errors = query_service.validate_query_data(query_data)
        
        # Should be valid
        assert is_valid
        assert len(errors) == 0

    def test_validate_query_data_missing_fields(self, query_service):
        """Test validation of query data with missing required fields"""
        query_data = {
            "query_type": QueryType.FULL_BOOK,
            # Missing query_text and book_id
        }
        
        is_valid, errors = query_service.validate_query_data(query_data)
        
        # Should not be valid
        assert not is_valid
        assert len(errors) > 0

    def test_validate_query_data_incorrect_type(self, query_service):
        """Test validation of query data with incorrect query type"""
        query_data = {
            "query_text": "What is the main theme?",
            "query_type": QueryType.FULL_BOOK,
            "user_selected_text": "This should not be present for FULL_BOOK",  # Should not be present
            "book_id": "test-book-id",
            "session_id": "test-session-id"
        }
        
        is_valid, errors = query_service.validate_query_data(query_data)
        
        # Should not be valid
        assert not is_valid
        assert len(errors) > 0