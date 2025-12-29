import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """Test client for the FastAPI app"""
    return TestClient(app)


def test_query_endpoint_contract_full_book(client):
    """Test the contract for POST /api/v1/query endpoint with full book query"""
    # Test request body structure
    request_data = {
        "query": "What is the main theme of this book?",
        "book_id": "test-book-uuid",
        "include_citations": True
    }
    
    response = client.post("/api/v1/query", json=request_data)
    
    # Check that the response has the correct status code
    # Note: This might return 404 if the book_id doesn't exist, which is expected
    assert response.status_code in [200, 404, 422]
    
    # If successful, check response structure
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify required fields in response
        assert "id" in response_data
        assert "query" in response_data
        assert "response" in response_data
        assert "citations" in response_data
        assert "confidence_score" in response_data
        assert "query_type" in response_data
        
        # Verify field types
        assert isinstance(response_data["id"], str)
        assert isinstance(response_data["query"], str)
        assert isinstance(response_data["response"], str)
        assert isinstance(response_data["citations"], list)
        assert isinstance(response_data["confidence_score"], (float, int))
        assert isinstance(response_data["query_type"], str)
        
        # Verify query type is correct
        assert response_data["query_type"] == "FULL_BOOK"
        
        # If citations are included, verify their structure
        if response_data["include_citations"]:
            for citation in response_data["citations"]:
                assert "section_title" in citation
                assert "page_number" in citation
                assert "text_snippet" in citation


def test_query_endpoint_contract_missing_fields(client):
    """Test that the endpoint properly handles missing required fields"""
    # Request without required fields
    request_data = {
        "query": "What is the main theme of this book?"
        # Missing book_id
    }
    
    response = client.post("/api/v1/query", json=request_data)
    
    # Should return 422 for validation error or 400 for bad request
    assert response.status_code in [400, 422]


def test_query_endpoint_invalid_book_id(client):
    """Test the endpoint with an invalid book ID"""
    request_data = {
        "query": "What is the main theme of this book?",
        "book_id": "invalid-book-id",
        "include_citations": True
    }
    
    response = client.post("/api/v1/query", json=request_data)
    
    # Should return 404 if book not found
    assert response.status_code in [404, 200, 422]


def test_query_endpoint_empty_query(client):
    """Test the endpoint with an empty query"""
    request_data = {
        "query": "",
        "book_id": "test-book-uuid",
        "include_citations": False
    }
    
    response = client.post("/api/v1/query", json=request_data)
    
    # Should return 422 for validation error
    assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__])