import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """Test client for the FastAPI app"""
    return TestClient(app)


def test_query_selection_endpoint_contract(client):
    """Test the contract for POST /api/v1/query/selection endpoint"""
    # Test request body structure for user selection query
    request_data = {
        "query": "What does this paragraph mean?",
        "selected_text": "The paragraph of text the user has selected...",
        "include_citations": False
    }
    
    response = client.post("/api/v1/query/selection", json=request_data)
    
    # Check that the response has the correct status code
    assert response.status_code in [200, 400, 422]
    
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
        assert response_data["query_type"] == "USER_SELECTION"


def test_query_selection_endpoint_missing_fields(client):
    """Test that the endpoint properly handles missing required fields"""
    # Request without required fields
    request_data = {
        "query": "What does this paragraph mean?"
        # Missing selected_text
    }
    
    response = client.post("/api/v1/query/selection", json=request_data)
    
    # Should return 422 for validation error or 400 for bad request
    assert response.status_code in [400, 422]


def test_query_selection_endpoint_empty_fields(client):
    """Test the endpoint with empty required fields"""
    request_data = {
        "query": "",
        "selected_text": "",
        "include_citations": False
    }
    
    response = client.post("/api/v1/query/selection", json=request_data)
    
    # Should return 422 for validation error
    assert response.status_code in [400, 422]


def test_query_selection_endpoint_valid_fields(client):
    """Test the endpoint with properly formatted request"""
    request_data = {
        "query": "What does this paragraph mean?",
        "selected_text": "The paragraph of text the user has selected...",
        "include_citations": True
    }
    
    response = client.post("/api/v1/query/selection", json=request_data)
    
    # Response could be 200 (success), 400 (bad request), or 422 (validation error)
    assert response.status_code in [200, 400, 422]
    
    if response.status_code == 200:
        response_data = response.json()
        # Verify the response structure is as expected
        assert "id" in response_data
        assert "query_type" in response_data
        assert response_data["query_type"] == "USER_SELECTION"


if __name__ == "__main__":
    pytest.main([__file__])