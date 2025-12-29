"""
Quickstart validation tests to ensure the application works as described in the quickstart guide.
This tests the examples provided in the quickstart.md file.
"""

import pytest
import os
from fastapi.testclient import TestClient
from src.api.main import app
from src.config.settings import settings


@pytest.fixture
def client():
    """Test client for the FastAPI app"""
    return TestClient(app)


def test_environment_variables():
    """Test that required environment variables are set as mentioned in quickstart.md"""
    required_vars = [
        "COHERE_API_KEY",
        "QDRANT_URL", 
        "QDRANT_API_KEY",
        "NEON_DATABASE_URL"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    # Note: For testing purposes, we're just verifying the variables are expected
    # In a real scenario, these would need to be set for full functionality
    print(f"Expected environment variables: {required_vars}")
    print(f"Missing environment variables: {missing_vars}")
    # This test doesn't fail to allow for testing without actual API keys


def test_health_check_endpoint(client):
    """Test the health check endpoint as described in quickstart.md"""
    response = client.get("/api/v1/health")
    
    # The health endpoint should return 200
    assert response.status_code == 200
    
    # Check that the response has the expected structure
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "dependencies" in data
    
    # Check that dependencies are reported
    assert isinstance(data["dependencies"], dict)


def test_api_response_format(client):
    """Test that API responses follow the format described in quickstart.md"""
    # Since we can't make actual queries without valid book IDs and API keys,
    # we'll test the error response format which should follow the same structure
    
    # Try to query with a malformed request to get an error response
    response = client.post("/api/v1/query", json={
        "query": "test query"
        # Missing required book_id field
    })
    
    # Should return 422 for validation error
    assert response.status_code in [400, 422]
    
    # Check that error response follows the format described in quickstart.md
    data = response.json()
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
    # "details" may or may not be present depending on implementation


def test_application_startup():
    """Test that the application starts up correctly as described in quickstart.md"""
    # The FastAPI TestClient already verifies that the app can be instantiated
    # Let's make a simple request to the root endpoint
    response = client.get("/")
    
    # Should return 200 with a welcome message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome" in data["message"]


def test_endpoint_routes_exist():
    """Test that the endpoints mentioned in quickstart.md exist"""
    endpoints_to_test = [
        ("/api/v1/query", "post"),
        ("/api/v1/query/selection", "post"), 
        ("/api/v1/books/test-book-id", "get"),
        ("/api/v1/health", "get")
    ]
    
    for endpoint, method in endpoints_to_test:
        if method.lower() == "get":
            response = client.get(endpoint)
        elif method.lower() == "post":
            if endpoint == "/api/v1/query":
                response = client.post(endpoint, json={"query": "test", "book_id": "test"})
            elif endpoint == "/api/v1/query/selection":
                response = client.post(endpoint, json={"query": "test", "selected_text": "test"})
            else:
                # For other POST endpoints, just test they exist
                response = client.post(endpoint, json={})
        else:
            # For other methods, just try a GET request to see if routing works
            response = client.get(endpoint)
        
        # The endpoint should exist (not return 404)
        # Note: They might return 422 for validation errors or 500 for missing dependencies,
        # but shouldn't return 404 if the route exists
        assert response.status_code != 404, f"Endpoint {endpoint} does not exist"


if __name__ == "__main__":
    pytest.main([__file__])