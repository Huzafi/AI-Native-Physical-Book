import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """Test client for the FastAPI app"""
    return TestClient(app)


def test_get_book_by_id_contract(client):
    """Test the contract for GET /api/v1/books/{book_id} endpoint"""
    # Test with a sample book ID
    book_id = "test-book-uuid"
    response = client.get(f"/api/v1/books/{book_id}")
    
    # Check that the response has the correct status code
    # Could be 200 (found), 404 (not found), or other error codes
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify required fields in response
        assert "id" in response_data
        assert "title" in response_data
        assert "author" in response_data
        assert "section_count" in response_data
        assert "total_pages" in response_data
        assert "created_at" in response_data
        assert "updated_at" in response_data
        
        # Verify field types
        assert isinstance(response_data["id"], str)
        assert isinstance(response_data["title"], str)
        assert isinstance(response_data["author"], str)
        assert isinstance(response_data["section_count"], int)
        assert isinstance(response_data["total_pages"], int)
        assert isinstance(response_data["created_at"], str)  # ISO datetime string
        assert isinstance(response_data["updated_at"], str)  # ISO datetime string
        
        # Optional field check
        if "isbn" in response_data:
            assert isinstance(response_data["isbn"], str)


def test_get_book_by_id_invalid_uuid(client):
    """Test the endpoint with an invalid UUID format"""
    invalid_book_id = "invalid-uuid"
    response = client.get(f"/api/v1/books/{invalid_book_id}")
    
    # Should return 422 for validation error or 404 for not found
    assert response.status_code in [404, 422]


def test_get_book_by_id_nonexistent(client):
    """Test the endpoint with a UUID that doesn't exist in the database"""
    nonexistent_book_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/books/{nonexistent_book_id}")
    
    # Should return 404 for not found
    assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__])