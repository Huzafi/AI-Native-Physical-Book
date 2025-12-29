import pytest
from unittest.mock import Mock, AsyncMock
from src.services.book_service import BookService
from src.models.book_content import BookContentModel
from src.models.book_section import BookSectionModel


@pytest.fixture
def mock_book_repository():
    """Mock repository for book data"""
    return Mock()


@pytest.fixture
def book_service(mock_book_repository):
    """Book service with mocked repository"""
    book_service = BookService()
    # Inject the mock repository
    book_service.book_repository = mock_book_repository
    return book_service


@pytest.mark.asyncio
async def test_get_book_by_id_integration(book_service, mock_book_repository):
    """Integration test for retrieving book information by ID"""
    # Setup test data
    book_id = "test-book-uuid"
    expected_book = BookContentModel(
        id=book_id,
        title="Test Book Title",
        author="Test Author",
        isbn="978-0-123456-78-9",
        content="Full book content here...",
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z"
    )
    
    # Mock the repository call
    mock_book_repository.get_by_id = AsyncMock(return_value=expected_book)
    
    # Mock section count
    mock_book_repository.get_section_count = AsyncMock(return_value=12)
    
    # Execute the service method
    result = await book_service.get_book_by_id(book_id)
    
    # Verify the repository was called correctly
    mock_book_repository.get_by_id.assert_called_once_with(book_id)
    mock_book_repository.get_section_count.assert_called_once_with(book_id)
    
    # Verify the result structure
    assert result["id"] == book_id
    assert result["title"] == expected_book.title
    assert result["author"] == expected_book.author
    assert result["section_count"] == 12
    assert "total_pages" in result
    assert "created_at" in result
    assert "updated_at" in result


@pytest.mark.asyncio
async def test_get_book_by_id_with_sections(book_service, mock_book_repository):
    """Test retrieving book information with section details"""
    book_id = "test-book-uuid"
    expected_book = BookContentModel(
        id=book_id,
        title="Test Book Title",
        author="Test Author",
        isbn="978-0-123456-78-9",
        content="Full book content here...",
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z"
    )
    
    # Mock sections
    expected_sections = [
        BookSectionModel(
            id="section-1",
            book_id=book_id,
            section_title="Chapter 1: Introduction",
            content="Introduction content...",
            page_start=1,
            page_end=10,
            section_order=1,
            vector_id="vector-1",
            created_at="2023-01-01T00:00:00Z"
        ),
        BookSectionModel(
            id="section-2",
            book_id=book_id,
            section_title="Chapter 2: Main Content",
            content="Main content...",
            page_start=11,
            page_end=50,
            section_order=2,
            vector_id="vector-2",
            created_at="2023-01-01T00:00:00Z"
        )
    ]
    
    # Mock the repository calls
    mock_book_repository.get_by_id = AsyncMock(return_value=expected_book)
    mock_book_repository.get_sections_by_book_id = AsyncMock(return_value=expected_sections)
    mock_book_repository.get_section_count = AsyncMock(return_value=2)
    
    # Execute the service method
    result = await book_service.get_book_by_id(book_id)
    
    # Verify the result includes section information
    assert result["id"] == book_id
    assert result["section_count"] == 2
    # Total pages should be calculated from sections
    assert result["total_pages"] == 50  # Based on the last page of the last section


@pytest.mark.asyncio
async def test_get_book_by_id_not_found(book_service, mock_book_repository):
    """Test retrieving a book that doesn't exist"""
    book_id = "nonexistent-book-uuid"
    
    # Mock the repository to return None
    mock_book_repository.get_by_id = AsyncMock(return_value=None)
    
    # Execute the service method - should raise an exception or return None
    result = await book_service.get_book_by_id(book_id)
    
    # Depending on implementation, this might return None or raise an exception
    # For this test, we'll assume it returns None if not found
    assert result is None


@pytest.mark.asyncio
async def test_get_book_by_id_with_empty_sections(book_service, mock_book_repository):
    """Test retrieving book information when it has no sections"""
    book_id = "test-book-uuid"
    expected_book = BookContentModel(
        id=book_id,
        title="Test Book Title",
        author="Test Author",
        isbn="978-0-123456-78-9",
        content="Full book content here...",
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z"
    )
    
    # Mock the repository calls
    mock_book_repository.get_by_id = AsyncMock(return_value=expected_book)
    mock_book_repository.get_sections_by_book_id = AsyncMock(return_value=[])
    mock_book_repository.get_section_count = AsyncMock(return_value=0)
    
    # Execute the service method
    result = await book_service.get_book_by_id(book_id)
    
    # Verify the result structure even with no sections
    assert result["id"] == book_id
    assert result["title"] == expected_book.title
    assert result["author"] == expected_book.author
    assert result["section_count"] == 0
    assert result["total_pages"] == 0


@pytest.mark.asyncio
async def test_get_book_by_id_special_characters(book_service, mock_book_repository):
    """Test retrieving book information with special characters in title/author"""
    book_id = "test-book-uuid"
    expected_book = BookContentModel(
        id=book_id,
        title="Test Book: A Story About \"Quotation\" and 'Apostrophe'",
        author="O'Connor, Test-Author & Co.",
        isbn="978-0-123456-78-9",
        content="Full book content with special characters...",
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z"
    )
    
    # Mock the repository calls
    mock_book_repository.get_by_id = AsyncMock(return_value=expected_book)
    mock_book_repository.get_section_count = AsyncMock(return_value=8)
    
    # Execute the service method
    result = await book_service.get_book_by_id(book_id)
    
    # Verify special characters are preserved
    assert result["id"] == book_id
    assert result["title"] == expected_book.title
    assert result["author"] == expected_book.author


if __name__ == "__main__":
    pytest.main([__file__])