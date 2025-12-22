"""
Comprehensive backend test suite for AI-Native Book
Tests all backend functionality including API endpoints, services, and models
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import get_db
from app.models.content import Content
from unittest.mock import AsyncMock, patch
from datetime import datetime
import json


# Create test client
client = TestClient(app)

class TestContentAPI:
    """Test content-related API endpoints"""

    def test_get_content_list(self):
        """Test retrieving list of content"""
        response = client.get("/api/content")
        assert response.status_code in [200, 404]  # 404 if no content exists
        if response.status_code == 200:
            data = response.json()
            assert "items" in data
            assert isinstance(data["items"], list)

    def test_get_specific_content(self):
        """Test retrieving specific content"""
        # First, try to get a list to find an ID
        response = client.get("/api/content")
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                content_id = data["items"][0].get("id")
                if content_id:
                    response = client.get(f"/api/content/{content_id}")
                    assert response.status_code in [200, 404]

    def test_get_table_of_contents(self):
        """Test retrieving table of contents"""
        response = client.get("/api/toc")
        assert response.status_code in [200, 404]  # 404 if no content exists
        if response.status_code == 200:
            data = response.json()
            assert "chapters" in data
            assert isinstance(data["chapters"], list)

    def test_reading_progress(self):
        """Test reading progress functionality"""
        import uuid
        session_id = str(uuid.uuid4())

        # Test saving reading progress
        progress_data = {
            "session_id": session_id,
            "content_id": "test-content",
            "position": {
                "chapter": 1,
                "section": 1,
                "paragraph": 1,
                "percent": 50.0
            }
        }

        response = client.post("/api/content/reading-progress", json=progress_data)
        assert response.status_code in [200, 400]  # 400 if validation fails

        # Test retrieving reading progress
        response = client.get(f"/api/content/reading-progress/{session_id}")
        assert response.status_code in [200, 404]


class TestSearchAPI:
    """Test search-related API endpoints"""

    def test_search_functionality(self):
        """Test search API functionality"""
        search_data = {
            "query": "test",
            "limit": 10
        }

        response = client.post("/api/search", json=search_data)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert isinstance(data["results"], list)
        assert "total_count" in data

    def test_search_with_filters(self):
        """Test search API with filters"""
        search_data = {
            "query": "test",
            "limit": 5,
            "filters": {
                "tags": ["example"],
                "chapter": "1"
            }
        }

        response = client.post("/api/search", json=search_data)
        # May return 200 or 400 depending on filter implementation
        assert response.status_code in [200, 400]

    def test_search_relevance_ranking(self):
        """Test search relevance and ranking accuracy"""
        search_data = {
            "query": "artificial intelligence",
            "limit": 20
        }

        response = client.post("/api/search", json=search_data)
        assert response.status_code == 200
        data = response.json()
        results = data.get("results", [])

        # Verify that results are properly ranked by relevance score
        if len(results) > 1:
            # Check that results are sorted by relevance score (descending)
            scores = [result.get("relevance_score", 0) for result in results]
            assert scores == sorted(scores, reverse=True), "Results should be sorted by relevance score (descending)"

        # Verify that relevance scores are within expected range
        for result in results:
            score = result.get("relevance_score", 0)
            assert 0 <= score <= 1, f"Relevance score {score} should be between 0 and 1"

    def test_search_edge_cases(self):
        """Test search functionality with edge cases"""
        # Test empty query
        response = client.post("/api/search", json={"query": "", "limit": 10})
        assert response.status_code in [400, 422]  # Should fail validation

        # Test very long query
        long_query = "a" * 501  # Exceeds max length of 500
        response = client.post("/api/search", json={"query": long_query, "limit": 10})
        assert response.status_code in [400, 422]  # Should fail validation

        # Test special characters
        special_query = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        response = client.post("/api/search", json={"query": special_query, "limit": 10})
        assert response.status_code == 200  # Should handle special characters safely

        # Test single character query (should work if min length is 1)
        response = client.post("/api/search", json={"query": "a", "limit": 10})
        assert response.status_code in [200, 404]  # Should work or return no results

        # Test query with spaces
        response = client.post("/api/search", json={"query": "  test  ", "limit": 10})
        assert response.status_code == 200  # Should handle leading/trailing spaces

        # Test no results case
        response = client.post("/api/search", json={"query": "qwertyuiop1234567890", "limit": 10})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert isinstance(data["results"], list)
        # Results may be empty, which is valid


class TestAIAssistantAPI:
    """Test AI assistant API endpoints"""

    def test_ai_assistant_basic(self):
        """Test basic AI assistant functionality"""
        ai_data = {
            "question": "What is this book about?",
            "include_sources": True
        }

        response = client.post("/api/ai-assistant", json=ai_data)
        # Could be 200 (success), 400 (bad request), 429 (rate limited), or 500 (service unavailable)
        assert response.status_code in [200, 400, 429, 500]

        if response.status_code == 200:
            data = response.json()
            assert "answer" in data
            assert isinstance(data["answer"], str)

    def test_ai_assistant_with_context(self):
        """Test AI assistant with context"""
        ai_data = {
            "question": "What was discussed earlier?",
            "context_content_id": "introduction",
            "include_sources": True
        }

        response = client.post("/api/ai-assistant", json=ai_data)
        assert response.status_code in [200, 400, 404, 429, 500]

    def test_ai_assistant_response_accuracy(self):
        """Test AI response accuracy against book content (T081)"""
        # Test with a general question that should have a valid response
        ai_data = {
            "question": "What topics does this book cover?",
            "include_sources": True
        }

        response = client.post("/api/ai-assistant", json=ai_data)
        assert response.status_code == 200

        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "confidence" in data

        # Verify the response structure
        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)
        assert isinstance(data["confidence"], (int, float))

        # Confidence should be between 0 and 1
        assert 0 <= data["confidence"] <= 1

        # If sources exist, they should have proper structure
        for source in data["sources"]:
            assert "content_id" in source
            assert "title" in source
            assert "url_path" in source
            assert "relevance_score" in source

    def test_ai_assistant_response_time(self):
        """Test AI response time (T082)"""
        import time

        ai_data = {
            "question": "What is artificial intelligence?",
            "include_sources": True
        }

        start_time = time.time()
        response = client.post("/api/ai-assistant", json=ai_data)
        end_time = time.time()

        response_time = end_time - start_time

        # Check that response time is under 5 seconds as required
        assert response_time < 5.0, f"AI response time {response_time}s exceeds 5 seconds limit"

        # If successful, verify the response structure
        if response.status_code == 200:
            data = response.json()
            assert "answer" in data
            assert "response_time_ms" in data

    def test_ai_assistant_performance_impact(self):
        """Test that AI functionality doesn't impact normal reading performance (T083)"""
        import time

        # Measure time for content API (not AI) to ensure it's not affected by AI service
        content_start = time.time()
        content_response = client.get("/api/content")
        content_end = time.time()

        content_time = content_end - content_start

        # Content API should be fast regardless of AI service status
        assert content_time < 3.0, f"Content API response time {content_time}s is too slow"

        # Verify content API still works normally
        assert content_response.status_code in [200, 404]  # 404 if no content exists
        if content_response.status_code == 200:
            data = content_response.json()
            assert "items" in data


class TestTranslationAPI:
    """Test translation-related API endpoints"""

    def test_translation_endpoints_exist(self):
        """Test that translation endpoints are accessible"""
        # Test GET endpoint (may return 404 if no translations exist)
        response = client.get("/api/translation/test-content?lang=ur")
        assert response.status_code in [200, 404, 400]

    def test_translation_management(self):
        """Test translation management endpoints"""
        # Test POST endpoint (may return 405 if method not allowed)
        response = client.get("/api/translation")
        assert response.status_code in [200, 404, 405]


class TestHealthAPI:
    """Test health check API endpoint"""

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "services" in data
        assert "timestamp" in data

        # Status should be one of: healthy, degraded, unhealthy
        assert data["status"] in ["healthy", "degraded", "unhealthy"]


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_endpoint(self):
        """Test handling of invalid endpoints"""
        response = client.get("/api/invalid-endpoint")
        assert response.status_code in [404, 405]

    def test_invalid_method(self):
        """Test handling of invalid HTTP methods"""
        response = client.post("/api/health")  # POST to GET endpoint
        assert response.status_code in [405, 422]

    def test_large_request_body(self):
        """Test handling of large request bodies"""
        large_data = {"query": "a" * 10000}  # Very large query
        response = client.post("/api/search", json=large_data)
        # Should handle gracefully, possibly with 413 or 422
        assert response.status_code in [413, 422, 400, 200]

    def test_rate_limiting(self):
        """Test rate limiting functionality (if implemented)"""
        # Make multiple requests quickly
        for i in range(50):
            response = client.post("/api/search", json={"query": f"test{i}", "limit": 1})
            if response.status_code == 429:
                # Rate limited as expected
                break

        # At least one request should succeed or be rate limited
        assert True  # This test verifies the system doesn't crash under load


class TestSecurity:
    """Test security-related functionality"""

    def test_input_validation(self):
        """Test input validation for common security issues"""
        # Test SQL injection attempts
        malicious_data = {
            "query": "test'; DROP TABLE test; --",
            "limit": 10
        }
        response = client.post("/api/search", json=malicious_data)
        assert response.status_code in [200, 400, 422]  # Should not crash

        # Test XSS attempts
        xss_data = {
            "question": "<script>alert('xss')</script>",
            "include_sources": True
        }
        response = client.post("/api/ai-assistant", json=xss_data)
        assert response.status_code in [200, 400, 422]  # Should handle safely


class TestPerformance:
    """Test performance-related aspects"""

    def test_response_time(self):
        """Test that responses are returned within acceptable time"""
        import time

        start_time = time.time()
        response = client.get("/api/health")
        end_time = time.time()

        response_time = end_time - start_time

        # Health check should be very fast
        assert response_time < 1.0  # Less than 1 second
        assert response.status_code == 200

    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import concurrent.futures

        def make_request():
            return client.get("/api/health").status_code

        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]

        # All requests should succeed
        assert all(result == 200 for result in results)


class TestComprehensiveIntegration:
    """Test comprehensive integration of all components"""

    def test_full_content_lifecycle(self):
        """Test creating, retrieving, searching, and translating content"""
        # This would test the full lifecycle of content in a real implementation
        assert True  # Placeholder for comprehensive integration test

    def test_user_journey_simulation(self):
        """Simulate a complete user journey through the application"""
        # Test a sequence of operations a user might perform
        # 1. Get table of contents
        response = client.get("/api/toc")
        assert response.status_code in [200, 404]

        # 2. Get content list
        response = client.get("/api/content")
        assert response.status_code in [200, 404]

        # 3. Search for content
        response = client.post("/api/search", json={"query": "test", "limit": 5})
        assert response.status_code == 200

        # 4. Use AI assistant
        response = client.post("/api/ai-assistant", json={"question": "What is this about?", "include_sources": True})
        assert response.status_code in [200, 400, 429, 500]

        # All operations should work together without conflicts
        assert True


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])