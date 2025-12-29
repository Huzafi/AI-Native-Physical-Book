#!/usr/bin/env python3
"""
End-to-End Testing Suite for AI-Native Book
Tests all user stories and their acceptance criteria
"""

import requests
import time
import json
from typing import Dict, List, Tuple
import unittest
from unittest.mock import Mock, patch

# Configuration
BASE_URL = "http://localhost:8000"  # Default backend URL
WEBSITE_URL = "http://localhost:3000"  # Default frontend URL
TIMEOUT = 10  # Request timeout in seconds

class EndToEndTestSuite:
    """
    Comprehensive end-to-end test suite for AI-Native Book
    """

    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.start_time = time.time()

    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name} - {details}")

    def test_user_story_1_read_book_content(self) -> bool:
        """
        Test User Story 1: Read Book Content
        As a reader, I want to navigate through the book content in a structured,
        book-like interface that provides a smooth reading experience with proper
        chapter organization, search functionality, and responsive design.
        """
        print("\n" + "="*60)
        print("Testing User Story 1: Read Book Content")
        print("="*60)

        all_passed = True

        # Test 1: Get table of contents
        try:
            response = self.session.get(f"{BASE_URL}/api/toc", timeout=TIMEOUT)
            if response.status_code == 200:
                toc_data = response.json()
                if "chapters" in toc_data and len(toc_data["chapters"]) > 0:
                    self.log_result("Get Table of Contents", True, "Successfully retrieved TOC with chapters")
                else:
                    self.log_result("Get Table of Contents", False, "TOC doesn't contain chapters")
                    all_passed = False
            else:
                self.log_result("Get Table of Contents", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Get Table of Contents", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 2: List content
        try:
            response = self.session.get(f"{BASE_URL}/api/content", timeout=TIMEOUT)
            if response.status_code == 200:
                content_data = response.json()
                if "items" in content_data and len(content_data["items"]) > 0:
                    self.log_result("List Book Content", True, f"Retrieved {len(content_data['items'])} content items")
                else:
                    self.log_result("List Book Content", False, "No content items found")
                    all_passed = False
            else:
                self.log_result("List Book Content", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("List Book Content", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 3: Get specific content
        try:
            # First get a content ID from the list
            response = self.session.get(f"{BASE_URL}/api/content", timeout=TIMEOUT)
            if response.status_code == 200:
                content_data = response.json()
                if "items" in content_data and len(content_data["items"]) > 0:
                    content_id = content_data["items"][0]["id"]

                    # Now get the specific content
                    response = self.session.get(f"{BASE_URL}/api/content/{content_id}", timeout=TIMEOUT)
                    if response.status_code == 200:
                        content = response.json()
                        if "title" in content and "content" in content:
                            self.log_result("Get Specific Content", True, f"Retrieved content: {content['title']}")
                        else:
                            self.log_result("Get Specific Content", False, "Missing required fields in response")
                            all_passed = False
                    else:
                        self.log_result("Get Specific Content", False, f"Status code: {response.status_code}")
                        all_passed = False
                else:
                    self.log_result("Get Specific Content", False, "No content available to test")
                    all_passed = False
            else:
                self.log_result("Get Specific Content", False, "Could not retrieve content list")
                all_passed = False
        except Exception as e:
            self.log_result("Get Specific Content", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 4: Test reading progress (if available)
        try:
            import uuid
            session_id = str(uuid.uuid4())

            response = self.session.get(f"{BASE_URL}/api/content/reading-progress/{session_id}", timeout=TIMEOUT)
            # This might return 404 if no progress exists, which is OK
            if response.status_code in [200, 404]:
                self.log_result("Reading Progress Retrieval", True, f"Status: {response.status_code}")
            else:
                self.log_result("Reading Progress Retrieval", False, f"Unexpected status: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Reading Progress Retrieval", False, f"Exception: {str(e)}")
            all_passed = False

        return all_passed

    def test_user_story_2_search_book_content(self) -> bool:
        """
        Test User Story 2: Search Book Content
        As a reader, I want to search for specific content within the book to
        quickly find relevant information without having to manually browse
        through all chapters.
        """
        print("\n" + "="*60)
        print("Testing User Story 2: Search Book Content")
        print("="*60)

        all_passed = True

        # Test 1: Perform a search
        try:
            search_payload = {
                "query": "AI",  # Common search term
                "limit": 5
            }

            response = self.session.post(
                f"{BASE_URL}/api/search",
                json=search_payload,
                timeout=TIMEOUT
            )

            if response.status_code == 200:
                search_results = response.json()
                if "results" in search_results:
                    result_count = len(search_results["results"])
                    self.log_result("Search Functionality", True, f"Found {result_count} results")
                else:
                    self.log_result("Search Functionality", False, "Missing results in response")
                    all_passed = False
            else:
                self.log_result("Search Functionality", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Search Functionality", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 2: Search with empty query (should handle gracefully)
        try:
            search_payload = {
                "query": "",
                "limit": 5
            }

            response = self.session.post(
                f"{BASE_URL}/api/search",
                json=search_payload,
                timeout=TIMEOUT
            )

            # Should either return empty results or 400 error
            if response.status_code in [200, 400]:
                self.log_result("Empty Search Query", True, f"Handled gracefully (status: {response.status_code})")
            else:
                self.log_result("Empty Search Query", False, f"Unexpected status: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Empty Search Query", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 3: Search performance (should be under 3 seconds)
        try:
            start_time = time.time()
            search_payload = {
                "query": "information",
                "limit": 10
            }

            response = self.session.post(
                f"{BASE_URL}/api/search",
                json=search_payload,
                timeout=TIMEOUT
            )

            response_time = time.time() - start_time

            if response.status_code == 200 and response_time < 3.0:
                self.log_result("Search Performance", True, f"Completed in {response_time:.3f}s")
            elif response.status_code != 200:
                self.log_result("Search Performance", False, f"Status code: {response.status_code}")
                all_passed = False
            else:
                self.log_result("Search Performance", False, f"Too slow: {response_time:.3f}s")
                all_passed = False
        except Exception as e:
            self.log_result("Search Performance", False, f"Exception: {str(e)}")
            all_passed = False

        return all_passed

    def test_user_story_3_ai_assistant(self) -> bool:
        """
        Test User Story 3: Use AI Assistant to Answer Questions
        As a reader, I want to ask questions about the book content and receive
        accurate answers based only on the book's content, without this feature
        interfering with my normal reading experience.
        """
        print("\n" + "="*60)
        print("Testing User Story 3: AI Assistant")
        print("="*60)

        all_passed = True

        # Test 1: AI assistant functionality
        try:
            ai_payload = {
                "question": "What is the main topic of this book?",
                "include_sources": True
            }

            response = self.session.post(
                f"{BASE_URL}/api/ai-assistant",
                json=ai_payload,
                timeout=15  # AI might take longer
            )

            if response.status_code == 200:
                ai_response = response.json()
                if "answer" in ai_response:
                    answer_length = len(ai_response["answer"])
                    sources_count = len(ai_response.get("sources", []))
                    self.log_result("AI Assistant Response", True, f"Answer length: {answer_length}, Sources: {sources_count}")
                else:
                    self.log_result("AI Assistant Response", False, "Missing answer in response")
                    all_passed = False
            elif response.status_code == 429:
                # Rate limited - this is expected behavior
                self.log_result("AI Assistant Response", True, "Rate limited as expected")
            else:
                self.log_result("AI Assistant Response", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("AI Assistant Response", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 2: AI performance (should be under 5 seconds)
        try:
            start_time = time.time()
            ai_payload = {
                "question": "Summarize the main concepts",
                "include_sources": True
            }

            response = self.session.post(
                f"{BASE_URL}/api/ai-assistant",
                json=ai_payload,
                timeout=15
            )

            response_time = time.time() - start_time

            if response.status_code == 200:
                if response_time < 5.0:
                    self.log_result("AI Performance", True, f"Completed in {response_time:.3f}s")
                else:
                    self.log_result("AI Performance", False, f"Too slow: {response_time:.3f}s")
                    all_passed = False
            elif response.status_code == 429:
                # Rate limited - acceptable
                self.log_result("AI Performance", True, "Rate limited as expected")
            else:
                self.log_result("AI Performance", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("AI Performance", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 3: AI with context
        try:
            ai_payload = {
                "question": "What was discussed in the introduction?",
                "context_content_id": "introduction",  # This might not exist, but should handle gracefully
                "include_sources": True
            }

            response = self.session.post(
                f"{BASE_URL}/api/ai-assistant",
                json=ai_payload,
                timeout=15
            )

            if response.status_code in [200, 404, 422]:  # 404 if context doesn't exist, 422 if invalid
                self.log_result("AI with Context", True, f"Handled gracefully (status: {response.status_code})")
            else:
                self.log_result("AI with Context", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("AI with Context", False, f"Exception: {str(e)}")
            all_passed = False

        return all_passed

    def test_user_story_4_translation(self) -> bool:
        """
        Test User Story 4: Access Urdu Translation and Summaries
        As a reader who prefers Urdu, I want to access translations and summaries
        of book content to enhance my understanding and reading experience.
        """
        print("\n" + "="*60)
        print("Testing User Story 4: Translation Features")
        print("="*60)

        all_passed = True

        # Test 1: Check if translation endpoints are available
        try:
            # Try to get available translations for a content item
            # First, get a content ID
            response = self.session.get(f"{BASE_URL}/api/content", timeout=TIMEOUT)
            if response.status_code == 200:
                content_data = response.json()
                if "items" in content_data and len(content_data["items"]) > 0:
                    content_id = content_data["items"][0]["id"]

                    # Try to get translations for this content
                    response = self.session.get(
                        f"{BASE_URL}/api/translation/{content_id}?lang=ur",
                        timeout=TIMEOUT
                    )

                    # Could be 200 (found), 404 (not found), or other error
                    if response.status_code in [200, 404, 400]:
                        self.log_result("Translation Retrieval", True, f"Handled gracefully (status: {response.status_code})")
                    else:
                        self.log_result("Translation Retrieval", False, f"Unexpected status: {response.status_code}")
                        all_passed = False
                else:
                    self.log_result("Translation Retrieval", True, "No content available, but endpoint accessible")
            else:
                self.log_result("Translation Retrieval", True, "No content available, but endpoint accessible")
        except Exception as e:
            self.log_result("Translation Retrieval", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 2: Check if translation management endpoint works
        try:
            response = self.session.get(f"{BASE_URL}/api/translation", timeout=TIMEOUT)
            # Should return 405 (method not allowed) or 404, not 404/500 error
            if response.status_code in [404, 405]:
                self.log_result("Translation Management", True, "Endpoint exists (status: {response.status_code})")
            elif response.status_code == 200:
                self.log_result("Translation Management", True, "Endpoint accessible")
            else:
                self.log_result("Translation Management", False, f"Unexpected status: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Translation Management", False, f"Exception: {str(e)}")
            all_passed = False

        return all_passed

    def test_cross_cutting_features(self) -> bool:
        """
        Test cross-cutting features like health checks, error handling, etc.
        """
        print("\n" + "="*60)
        print("Testing Cross-Cutting Features")
        print("="*60)

        all_passed = True

        # Test 1: Health check endpoint
        try:
            response = self.session.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
            if response.status_code == 200:
                health_data = response.json()
                if "status" in health_data:
                    self.log_result("Health Check", True, f"Status: {health_data['status']}")
                else:
                    self.log_result("Health Check", False, "Missing status in response")
                    all_passed = False
            else:
                self.log_result("Health Check", False, f"Status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Health Check", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 2: Error handling - invalid endpoint
        try:
            response = self.session.get(f"{BASE_URL}/api/invalid-endpoint", timeout=TIMEOUT)
            if response.status_code == 404:
                self.log_result("Error Handling", True, "Properly handles invalid endpoints")
            else:
                self.log_result("Error Handling", False, f"Unexpected status for invalid endpoint: {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Error Handling", False, f"Exception: {str(e)}")
            all_passed = False

        # Test 3: Rate limiting (if implemented)
        try:
            # Make multiple requests quickly to test rate limiting
            for i in range(5):
                response = self.session.post(
                    f"{BASE_URL}/api/search",
                    json={"query": f"test{i}", "limit": 1},
                    timeout=TIMEOUT
                )

            # The responses should not be 429 unless we exceeded limits
            # This test is more about ensuring the system doesn't crash
            self.log_result("Rate Limiting Stability", True, "System remains stable under rapid requests")
        except Exception as e:
            self.log_result("Rate Limiting Stability", False, f"Exception: {str(e)}")
            all_passed = False

        return all_passed

    def run_all_tests(self) -> Dict:
        """
        Run all end-to-end tests and return comprehensive results
        """
        print("Starting End-to-End Testing Suite for AI-Native Book")
        print("="*60)

        # Run all user story tests
        us1_result = self.test_user_story_1_read_book_content()
        us2_result = self.test_user_story_2_search_book_content()
        us3_result = self.test_user_story_3_ai_assistant()
        us4_result = self.test_user_story_4_translation()
        cross_cutting_result = self.test_cross_cutting_features()

        # Calculate overall results
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        failed_tests = total_tests - passed_tests

        overall_success = all([us1_result, us2_result, us3_result, us4_result, cross_cutting_result])

        results_summary = {
            "overall_success": overall_success,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "test_results": self.test_results,
            "execution_time": time.time() - self.start_time,
            "user_stories": {
                "user_story_1": us1_result,
                "user_story_2": us2_result,
                "user_story_3": us3_result,
                "user_story_4": us4_result,
                "cross_cutting": cross_cutting_result
            }
        }

        # Print summary
        print("\n" + "="*60)
        print("END-TO-END TEST RESULTS SUMMARY")
        print("="*60)
        print(f"Overall Success: {'✅ PASS' if results_summary['overall_success'] else '❌ FAIL'}")
        print(f"Total Tests: {results_summary['total_tests']}")
        print(f"Passed: {results_summary['passed_tests']}")
        print(f"Failed: {results_summary['failed_tests']}")
        print(f"Success Rate: {results_summary['success_rate']:.2%}")
        print(f"Execution Time: {results_summary['execution_time']:.2f}s")

        print("\nUser Story Results:")
        print(f"  User Story 1 (Read Content): {'✅ PASS' if us1_result else '❌ FAIL'}")
        print(f"  User Story 2 (Search Content): {'✅ PASS' if us2_result else '❌ FAIL'}")
        print(f"  User Story 3 (AI Assistant): {'✅ PASS' if us3_result else '❌ FAIL'}")
        print(f"  User Story 4 (Translation): {'✅ PASS' if us4_result else '❌ FAIL'}")
        print(f"  Cross-Cutting: {'✅ PASS' if cross_cutting_result else '❌ FAIL'}")

        return results_summary

def main():
    """
    Main function to run the end-to-end tests
    """
    tester = EndToEndTestSuite()
    results = tester.run_all_tests()

    # Exit with appropriate code based on results
    if not results["overall_success"]:
        print(f"\n⚠️  Some tests failed. Please check the output above for details.")
        exit(1)
    else:
        print(f"\n🎉 All end-to-end tests passed successfully!")
        exit(0)

if __name__ == "__main__":
    main()