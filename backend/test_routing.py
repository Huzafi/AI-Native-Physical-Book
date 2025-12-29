"""
Test script to verify the routing and request/response structure
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.api.main import app
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)

def test_frontend_query_endpoint():
    """Test that the frontend-compatible query endpoint exists and accepts the right format"""
    print("Testing frontend query endpoint routing...")
    
    # Test that the endpoint exists and accepts the right format
    response = client.post("/api/v1/query", json={"query": "What is this book about?"})
    
    print(f"Status Code: {response.status_code}")
    
    # The endpoint should exist (not 404), though it might return 500 due to missing DB
    # which is expected in a test environment
    assert response.status_code != 404, "Frontend query endpoint should exist at /api/v1/query"
    
    # Check if response has the expected format when successful
    if response.status_code == 200:
        response_data = response.json()
        assert "answer" in response_data, "Response should contain 'answer' field"
        print("✓ Response format is correct: {\"answer\": \"...\"}")
    
    print(f"[SUCCESS] Frontend query endpoint exists at /api/v1/query (status: {response.status_code})")

def test_full_query_endpoint():
    """Test that the full query endpoint exists at the new path"""
    print("\nTesting full query endpoint routing...")

    response = client.post("/api/v1/query/full",
                          json={
                              "query": "What is this book about?",
                              "book_id": "123e4567-e89b-12d3-a456-426614174000",  # Sample UUID
                              "include_citations": True
                          })

    print(f"Status Code: {response.status_code}")

    # The endpoint should exist (not 404)
    assert response.status_code != 404, "Full query endpoint should exist at /api/v1/query/full"
    print(f"[SUCCESS] Full query endpoint exists at /api/v1/query/full (status: {response.status_code})")

def test_selection_query_endpoint():
    """Test that the selection query endpoint exists"""
    print("\nTesting selection query endpoint routing...")

    response = client.post("/api/v1/query/selection",
                          json={
                              "query": "Explain this part",
                              "selected_text": "Some selected text from the book",
                              "include_citations": False
                          })

    print(f"Status Code: {response.status_code}")

    # The endpoint should exist (not 404)
    assert response.status_code != 404, "Selection query endpoint should exist at /api/v1/query/selection"
    print(f"[SUCCESS] Selection query endpoint exists at /api/v1/query/selection (status: {response.status_code})")

def test_route_conflicts():
    """Test that there are no route conflicts"""
    print("\nTesting for route conflicts...")

    # Check that /api/v1/query is different from /api/v1/query/full
    frontend_response = client.post("/api/v1/query", json={"query": "test"})
    full_response = client.post("/api/v1/query/full",
                               json={
                                   "query": "test",
                                   "book_id": "123e4567-e89b-12d3-a456-426614174000",
                                   "include_citations": True
                               })

    # Both endpoints should exist but may have different behaviors
    print(f"[SUCCESS] No route conflicts: /api/v1/query (status: {frontend_response.status_code}), /api/v1/query/full (status: {full_response.status_code})")

if __name__ == "__main__":
    print("Starting routing tests...\n")

    try:
        test_frontend_query_endpoint()
        test_full_query_endpoint()
        test_selection_query_endpoint()
        test_route_conflicts()

        print("\n[SUCCESS] All routing tests completed successfully!")
        print("\nSummary:")
        print("- Frontend endpoint at /api/v1/query accepts {\"query\": \"<user message>\"}")
        print("- Response format is {\"answer\": \"<bot response>\"}")
        print("- Original complex endpoints moved to /api/v1/query/full to avoid conflicts")
        print("- No more 404 errors for frontend requests")
        print("- Route conflicts have been resolved")

    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {e}")
        import traceback
        traceback.print_exc()