#!/usr/bin/env python3
"""
AI Response Time Test for AI-Native Book
Tests that AI responses are delivered within 5 seconds
"""

import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
BASE_URL = "http://localhost:8000"  # Default backend URL
TIMEOUT_THRESHOLD = 5.0  # 5 seconds max response time
NUM_REQUESTS = 10  # Number of requests to test
CONCURRENT_WORKERS = 3  # Number of concurrent requests for load testing

def test_single_response_time(question: str) -> dict:
    """
    Test response time for a single AI request
    """
    start_time = time.time()

    try:
        response = requests.post(f"{BASE_URL}/api/ai-assistant",
                               json={
                                   "question": question,
                                   "include_sources": True
                               },
                               timeout=15)  # Higher timeout for the request itself

        actual_time = time.time() - start_time

        result = {
            "question": question,
            "response_time": actual_time,
            "status_code": response.status_code,
            "success": response.status_code == 200 and actual_time < TIMEOUT_THRESHOLD,
            "error": None if response.status_code == 200 else f"HTTP {response.status_code}"
        }

        return result

    except requests.exceptions.Timeout:
        actual_time = time.time() - start_time
        return {
            "question": question,
            "response_time": actual_time,
            "status_code": "TIMEOUT",
            "success": False,
            "error": "Request timed out"
        }
    except Exception as e:
        actual_time = time.time() - start_time
        return {
            "question": question,
            "response_time": actual_time,
            "status_code": "ERROR",
            "success": False,
            "error": str(e)
        }

def test_response_time_basic():
    """
    Test basic response times with simple questions
    """
    print("Testing basic AI response times...")

    test_questions = [
        "What is this book about?",
        "Summarize the main concepts",
        "Explain artificial intelligence briefly",
        "What are the key takeaways?",
        "How does this book approach AI?"
    ]

    results = []

    for i, question in enumerate(test_questions):
        print(f"  Question {i+1}/{len(test_questions)}: {question[:30]}...")

        result = test_single_response_time(question)
        results.append(result)

        status = "✅" if result["success"] else "❌"
        print(f"    {status} Time: {result['response_time']:.3f}s, Status: {result['status_code']}")

        if not result["success"]:
            print(f"      Error: {result['error']}")

    return results

def test_response_time_load():
    """
    Test response times under load with concurrent requests
    """
    print(f"\nTesting AI response times under load ({CONCURRENT_WORKERS} concurrent requests)...")

    test_questions = [
        "What is artificial intelligence?",
        "Explain machine learning concepts",
        "How does neural networks work?",
        "What are the ethical considerations?",
        "Describe the future of AI",
        "Explain perception in AI",
        "What is reasoning in AI?",
        "How does action work in AI systems?",
        "Compare human and machine intelligence",
        "What are the limitations?"
    ]

    results = []

    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        # Submit all tasks
        future_to_question = {
            executor.submit(test_single_response_time, q): q
            for q in test_questions
        }

        # Collect results as they complete
        for future in as_completed(future_to_question):
            result = future.result()
            results.append(result)

            status = "✅" if result["success"] else "❌"
            print(f"  {status} {result['question'][:30]}... - {result['response_time']:.3f}s")

    return results

def analyze_results(results: list) -> dict:
    """
    Analyze test results and return summary statistics
    """
    successful_results = [r for r in results if r["success"]]
    failed_results = [r for r in results if not r["success"]]

    response_times = [r["response_time"] for r in successful_results]

    if response_times:
        stats = {
            "total_requests": len(results),
            "successful_requests": len(successful_results),
            "failed_requests": len(failed_results),
            "success_rate": len(successful_results) / len(results) if results else 0,
            "avg_response_time": statistics.mean(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "median_response_time": statistics.median(response_times) if response_times else 0,
            "p95_response_time": sorted(response_times)[int(0.95 * len(response_times))] if response_times and len(response_times) > 1 else (response_times[0] if response_times else 0),
            "within_threshold": sum(1 for t in response_times if t < TIMEOUT_THRESHOLD),
            "exceeding_threshold": sum(1 for t in response_times if t >= TIMEOUT_THRESHOLD)
        }
    else:
        stats = {
            "total_requests": len(results),
            "successful_requests": 0,
            "failed_requests": len(results),
            "success_rate": 0,
            "avg_response_time": 0,
            "min_response_time": 0,
            "max_response_time": 0,
            "median_response_time": 0,
            "p95_response_time": 0,
            "within_threshold": 0,
            "exceeding_threshold": 0
        }

    return stats

def print_detailed_results(results: list):
    """
    Print detailed results for each test
    """
    print("\nDetailed Results:")
    print("-" * 80)
    print(f"{'Status':<8} {'Time (s)':<10} {'Question':<30} {'Error':<20}")
    print("-" * 80)

    for result in results:
        status = "PASS" if result["success"] else "FAIL"
        time_str = f"{result['response_time']:.3f}"
        question = result['question'][:27] + "..." if len(result['question']) > 30 else result['question']
        error = result['error'][:17] + "..." if result['error'] and len(result['error']) > 20 else (result['error'] or "")

        print(f"{status:<8} {time_str:<10} {question:<30} {error:<20}")

def main():
    """
    Main function to run all AI response time tests
    """
    print("AI-Native Book - AI Response Time Test Suite")
    print("=" * 80)
    print(f"Target: Responses within {TIMEOUT_THRESHOLD} seconds")
    print("=" * 80)

    # Run basic response time tests
    print("Running basic response time tests...")
    basic_results = test_response_time_basic()

    # Run load response time tests
    print("\nRunning load response time tests...")
    load_results = test_response_time_load()

    # Combine all results
    all_results = basic_results + load_results

    # Analyze results
    stats = analyze_results(all_results)

    # Print summary
    print("\n" + "=" * 80)
    print("RESPONSE TIME TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"Total Requests: {stats['total_requests']}")
    print(f"Successful Requests: {stats['successful_requests']}")
    print(f"Failed Requests: {stats['failed_requests']}")
    print(f"Success Rate: {stats['success_rate']:.2%}")
    print()
    print("Response Time Statistics:")
    print(f"  Average: {stats['avg_response_time']:.3f}s")
    print(f"  Minimum: {stats['min_response_time']:.3f}s")
    print(f"  Maximum: {stats['max_response_time']:.3f}s")
    print(f"  Median:  {stats['median_response_time']:.3f}s")
    print(f"  95th Percentile: {stats['p95_response_time']:.3f}s")
    print()
    print(f"Within {TIMEOUT_THRESHOLD}s: {stats['within_threshold']}")
    print(f"Exceeding {TIMEOUT_THRESHOLD}s: {stats['exceeding_threshold']}")
    print()

    # Determine overall pass/fail
    if stats['max_response_time'] < TIMEOUT_THRESHOLD:
        print(f"✅ OVERALL RESULT: PASSED (All responses <{TIMEOUT_THRESHOLD}s)")
    else:
        print(f"❌ OVERALL RESULT: FAILED (Max response {stats['max_response_time']:.3f}s >= {TIMEOUT_THRESHOLD}s)")

    if stats['avg_response_time'] < TIMEOUT_THRESHOLD:
        print(f"✅ AVERAGE PERFORMANCE: PASSED (Average {stats['avg_response_time']:.3f}s <{TIMEOUT_THRESHOLD}s)")
    else:
        print(f"❌ AVERAGE PERFORMANCE: FAILED (Average {stats['avg_response_time']:.3f}s >= {TIMEOUT_THRESHOLD}s)")

    # Print detailed results
    print_detailed_results(all_results)

if __name__ == "__main__":
    main()