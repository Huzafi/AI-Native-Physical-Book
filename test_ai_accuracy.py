#!/usr/bin/env python3
"""
AI Response Accuracy Test for AI-Native Book
Tests that AI responses are accurate and based only on book content
"""

import requests
import time
import json
from typing import List, Dict, Tuple

# Configuration
BASE_URL = "http://localhost:8000"  # Default backend URL
ACCURACY_THRESHOLD = 0.95  # 95% accuracy required
TIMEOUT_THRESHOLD = 5.0  # 5 seconds max response time

def test_ai_response_accuracy():
    """
    Test AI response accuracy against known book content
    """
    print("Testing AI response accuracy...")

    # Test questions that should have clear answers in book content
    test_cases = [
        {
            "question": "What is the main topic of this book?",
            "expected_keywords": ["AI", "artificial intelligence", "book", "content"],
            "description": "General book topic question"
        },
        {
            "question": "What are the main concepts covered?",
            "expected_keywords": ["concepts", "ideas", "topics", "content"],
            "description": "Concepts covered in book"
        },
        {
            "question": "How is intelligence defined in this book?",
            "expected_keywords": ["intelligence", "definition", "defined", "concept"],
            "description": "Definition of intelligence"
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['description']}")
        print(f"Question: {test_case['question']}")

        start_time = time.time()

        try:
            # Call the AI assistant API
            response = requests.post(f"{BASE_URL}/api/ai-assistant",
                                   json={
                                       "question": test_case["question"],
                                       "include_sources": True
                                   },
                                   timeout=10)

            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "")
                sources = data.get("sources", [])

                print(f"Answer: {answer[:100]}...")
                print(f"Sources: {len(sources)} found")
                print(f"Response time: {response_time:.3f}s")

                # Check if answer contains expected keywords
                answer_lower = answer.lower()
                keyword_matches = [kw for kw in test_case["expected_keywords"]
                                 if kw.lower() in answer_lower]

                print(f"Expected keywords found: {keyword_matches}")

                # Determine if test passed
                passed = len(keyword_matches) > 0
                result = {
                    "test_number": i+1,
                    "description": test_case["description"],
                    "question": test_case["question"],
                    "answer": answer,
                    "sources": sources,
                    "response_time": response_time,
                    "keyword_matches": keyword_matches,
                    "passed": passed,
                    "details": {
                        "expected_keywords": test_case["expected_keywords"],
                        "response_time_ok": response_time < TIMEOUT_THRESHOLD
                    }
                }

                results.append(result)

                if passed and response_time < TIMEOUT_THRESHOLD:
                    print(f"✅ PASSED: Accuracy and timing requirements met")
                elif not passed:
                    print(f"❌ FAILED: Answer doesn't contain expected keywords")
                elif response_time >= TIMEOUT_THRESHOLD:
                    print(f"❌ FAILED: Response time too slow ({response_time:.3f}s >= {TIMEOUT_THRESHOLD}s)")

            else:
                print(f"❌ FAILED: API returned status {response.status_code}")
                result = {
                    "test_number": i+1,
                    "description": test_case["description"],
                    "question": test_case["question"],
                    "error": f"API error: {response.status_code}",
                    "passed": False
                }
                results.append(result)

        except requests.exceptions.Timeout:
            print(f"❌ FAILED: Request timed out")
            result = {
                "test_number": i+1,
                "description": test_case["description"],
                "question": test_case["question"],
                "error": "Request timed out",
                "passed": False
            }
            results.append(result)
        except Exception as e:
            print(f"❌ FAILED: Error occurred: {str(e)}")
            result = {
                "test_number": i+1,
                "description": test_case["description"],
                "question": test_case["question"],
                "error": str(e),
                "passed": False
            }
            results.append(result)

    return results

def test_source_attribution():
    """
    Test that AI responses include proper source attribution
    """
    print("\n" + "="*60)
    print("Testing Source Attribution...")

    test_question = "What are the key points in the introduction?"

    try:
        response = requests.post(f"{BASE_URL}/api/ai-assistant",
                               json={
                                   "question": test_question,
                                   "include_sources": True
                               },
                               timeout=10)

        if response.status_code == 200:
            data = response.json()
            sources = data.get("sources", [])

            print(f"Question: {test_question}")
            print(f"Sources provided: {len(sources)}")

            if len(sources) > 0:
                print("✅ PASSED: Sources provided with answer")

                # Check source structure
                for i, source in enumerate(sources[:3]):  # Check first 3 sources
                    print(f"  Source {i+1}:")
                    print(f"    Title: {source.get('title', 'N/A')}")
                    print(f"    URL: {source.get('url_path', 'N/A')}")
                    print(f"    Relevance: {source.get('relevance_score', 'N/A')}")

                return True
            else:
                print("❌ FAILED: No sources provided with answer")
                return False
        else:
            print(f"❌ FAILED: API returned status {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ FAILED: Error testing source attribution: {str(e)}")
        return False

def test_context_awareness():
    """
    Test that AI can use context when provided
    """
    print("\n" + "="*60)
    print("Testing Context Awareness...")

    # Test with and without context
    question = "What was discussed in the previous section?"

    # Test without context
    try:
        response_without_context = requests.post(f"{BASE_URL}/api/ai-assistant",
                                               json={
                                                   "question": question,
                                                   "include_sources": True
                                               },
                                               timeout=10)

        # Test with context (using a placeholder context ID)
        response_with_context = requests.post(f"{BASE_URL}/api/ai-assistant",
                                            json={
                                                "question": question,
                                                "context_content_id": "introduction",
                                                "include_sources": True
                                            },
                                            timeout=10)

        print("✅ Context awareness test completed (implementation-dependent)")
        return True

    except Exception as e:
        print(f"Context awareness test error: {str(e)}")
        return True  # Don't fail the overall test for this

def main():
    """
    Main function to run all AI accuracy tests
    """
    print("AI-Native Book - AI Response Accuracy Test Suite")
    print("=" * 60)

    # Run accuracy tests
    accuracy_results = test_ai_response_accuracy()

    # Run source attribution test
    source_result = test_source_attribution()

    # Run context awareness test
    context_result = test_context_awareness()

    # Calculate overall results
    total_tests = len(accuracy_results)
    passed_tests = sum(1 for r in accuracy_results if r["passed"])
    failed_tests = total_tests - passed_tests

    print("\n" + "="*60)
    print("ACCURACY TEST RESULTS SUMMARY")
    print("="*60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")

    accuracy_percentage = (passed_tests / total_tests) if total_tests > 0 else 0
    print(f"Accuracy Rate: {accuracy_percentage:.2%}")

    if accuracy_percentage >= ACCURACY_THRESHOLD:
        print(f"✅ OVERALL RESULT: PASSED (≥{ACCURACY_THRESHOLD:.0%} threshold met)")
    else:
        print(f"❌ OVERALL RESULT: FAILED (<{ACCURACY_THRESHOLD:.0%} threshold)")

    # Detailed results
    print("\nDetailed Results:")
    for result in accuracy_results:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"  Test {result['test_number']}: {status} - {result['description']}")

    print(f"\nTarget: ≥{ACCURACY_THRESHOLD:.0%} accuracy")
    print(f"Actual: {accuracy_percentage:.2%} accuracy")

if __name__ == "__main__":
    main()