import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.embedding_service import EmbeddingService
import numpy as np


class TestEmbeddingService:
    """Unit tests for the EmbeddingService class"""

    @pytest.fixture
    def mock_cohere_client(self):
        """Mock Cohere client"""
        mock_client = Mock()
        mock_client.embed = Mock(return_value=Mock(embeddings=[[0.1, 0.2, 0.3]]))
        return mock_client

    @pytest.fixture
    def mock_qdrant_client(self):
        """Mock Qdrant client"""
        mock_client = Mock()
        mock_client.search = AsyncMock(return_value=[])
        mock_client.upload_collection = AsyncMock()
        return mock_client

    @pytest.fixture
    def embedding_service(self, mock_cohere_client, mock_qdrant_client):
        """Create an EmbeddingService instance with mocked dependencies"""
        service = EmbeddingService(cohere_client=mock_cohere_client, qdrant_client=mock_qdrant_client)
        return service

    def test_generate_embedding_success(self, embedding_service, mock_cohere_client):
        """Test successful embedding generation"""
        text = "This is a test sentence."
        expected_embedding = [0.1, 0.2, 0.3]
        
        result = embedding_service.generate_embedding(text)
        
        # Verify the Cohere client was called with correct parameters
        mock_cohere_client.embed.assert_called_once_with(
            texts=[text],
            model=embedding_service.embedding_model
        )
        
        # Verify the result
        assert result == expected_embedding

    def test_generate_embedding_empty_text(self, embedding_service):
        """Test embedding generation with empty text"""
        with pytest.raises(ValueError):
            embedding_service.generate_embedding("")

    def test_generate_embedding_none_text(self, embedding_service):
        """Test embedding generation with None text"""
        with pytest.raises(ValueError):
            embedding_service.generate_embedding(None)

    @pytest.mark.asyncio
    async def test_retrieve_relevant_chunks_success(self, embedding_service, mock_qdrant_client):
        """Test successful retrieval of relevant chunks"""
        query_embedding = [0.1, 0.2, 0.3]
        book_id = "test-book-id"
        expected_chunks = [
            {"id": "chunk-1", "content": "Test content 1", "section_id": "section-1", "page_number": 1},
            {"id": "chunk-2", "content": "Test content 2", "section_id": "section-2", "page_number": 2}
        ]
        
        # Mock the search response
        mock_qdrant_client.search.return_value = [
            Mock(id="chunk-1", payload={"content": "Test content 1", "section_id": "section-1", "page_number": 1}),
            Mock(id="chunk-2", payload={"content": "Test content 2", "section_id": "section-2", "page_number": 2})
        ]
        
        result = await embedding_service.retrieve_relevant_chunks(
            query_embedding=query_embedding,
            book_id=book_id,
            query_type="FULL_BOOK"
        )
        
        # Verify the Qdrant client was called with correct parameters
        mock_qdrant_client.search.assert_called_once()
        
        # Verify the result
        assert len(result) == 2
        assert result[0]["id"] == "chunk-1"
        assert result[0]["content"] == "Test content 1"
        assert result[1]["id"] == "chunk-2"
        assert result[1]["content"] == "Test content 2"

    @pytest.mark.asyncio
    async def test_retrieve_relevant_chunks_with_user_selection(self, embedding_service, mock_qdrant_client):
        """Test retrieval of relevant chunks for user selection query"""
        query_embedding = [0.1, 0.2, 0.3]
        book_id = "test-book-id"
        selected_text = "User selected text"
        
        result = await embedding_service.retrieve_relevant_chunks(
            query_embedding=query_embedding,
            book_id=book_id,
            query_type="USER_SELECTION",
            selected_text=selected_text
        )
        
        # For user selection, we should return the selected text as the only chunk
        assert len(result) == 1
        assert result[0]["content"] == selected_text
        assert result[0]["id"] == "user_selection"

    @pytest.mark.asyncio
    async def test_retrieve_relevant_chunks_no_results(self, embedding_service, mock_qdrant_client):
        """Test retrieval when no relevant chunks are found"""
        query_embedding = [0.1, 0.2, 0.3]
        book_id = "test-book-id"
        
        # Mock empty search response
        mock_qdrant_client.search.return_value = []
        
        result = await embedding_service.retrieve_relevant_chunks(
            query_embedding=query_embedding,
            book_id=book_id,
            query_type="FULL_BOOK"
        )
        
        # Verify the result is empty
        assert result == []

    @pytest.mark.asyncio
    async def test_store_embeddings_success(self, embedding_service, mock_qdrant_client):
        """Test successful storage of embeddings"""
        chunks = [
            {"id": "chunk-1", "content": "Test content 1", "section_id": "section-1", "page_number": 1},
            {"id": "chunk-2", "content": "Test content 2", "section_id": "section-2", "page_number": 2}
        ]
        book_id = "test-book-id"
        
        await embedding_service.store_embeddings(chunks, book_id)
        
        # Verify the Qdrant client upload method was called
        assert mock_qdrant_client.upload_collection.called

    def test_preprocess_text(self, embedding_service):
        """Test text preprocessing"""
        raw_text = "  This is a test sentence with extra whitespace and\nnewlines.  "
        expected = "This is a test sentence with extra whitespace and newlines."
        
        result = embedding_service.preprocess_text(raw_text)
        
        assert result == expected

    def test_preprocess_text_with_special_chars(self, embedding_service):
        """Test text preprocessing with special characters"""
        raw_text = "Text with special chars: \t\n\r and  multiple   spaces."
        expected = "Text with special chars: and multiple spaces."
        
        result = embedding_service.preprocess_text(raw_text)
        
        assert result == expected