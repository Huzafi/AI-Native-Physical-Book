#!/usr/bin/env python3
"""
Performance testing script for AI-Native Book
Tests content loading performance to ensure <2s load times
"""

import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Configuration
BASE_URL = "http://localhost:8000"  # Default backend URL
NUM_REQUESTS = 10  # Number of requests to test
CONCURRENT_WORKERS = 3  # Number of concurrent requests

def test_content_loading_performance():
    """
    Test content loading performance from the backend API
    """
    print("Testing content loading performance...")

    # Test GET /api/content endpoint
    content_times = []

    for i in range(NUM_REQUESTS):
        start_time = time.time()
        try:
            response = requests.get(f"{BASE_URL}/api/content")
            response_time = time.time() - start_time

            if response.status_code == 200:
                content_times.append(response_time)
                print(f"Request {i+1}: {response_time:.3f}s - SUCCESS")
            else:
                print(f"Request {i+1}: {response_time:.3f}s - FAILED (Status: {response.status_code})")
        except Exception as e:
            response_time = time.time() - start_time
            print(f"Request {i+1}: {response_time:.3f}s - ERROR: {str(e)}")

    if content_times:
        avg_time = statistics.mean(content_times)
        min_time = min(content_times)
        max_time = max(content_times)
        p95_time = sorted(content_times)[int(0.95 * len(content_times))] if len(content_times) > 0 else 0

        print(f"\nContent Loading Performance Results:")
        print(f"Successful requests: {len(content_times)}/{NUM_REQUESTS}")
        print(f"Average response time: {avg_time:.3f}s")
        print(f"Min response time: {min_time:.3f}s")
        print(f"Max response time: {max_time:.3f}s")
        print(f"95th percentile: {p95_time:.3f}s")

        if max_time < 2.0:
            print("✅ PASSED: Max response time < 2s")
        else:
            print("❌ FAILED: Max response time >= 2s")

        if avg_time < 2.0:
            print("✅ PASSED: Average response time < 2s")
        else:
            print("❌ FAILED: Average response time >= 2s")

    return content_times

def test_concurrent_content_loading():
    """
    Test concurrent content loading to simulate multiple users
    """
    print(f"\nTesting concurrent content loading with {CONCURRENT_WORKERS} workers...")

    def single_request():
        start_time = time.time()
        try:
            response = requests.get(f"{BASE_URL}/api/content")
            response_time = time.time() - start_time
            return response_time, response.status_code
        except Exception as e:
            response_time = time.time() - start_time
            return response_time, str(e)

    concurrent_times = []

    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        futures = [executor.submit(single_request) for _ in range(CONCURRENT_WORKERS * 2)]

        for future in as_completed(futures):
            response_time, status = future.result()
            concurrent_times.append(response_time)
            print(f"Concurrent request: {response_time:.3f}s - Status: {status}")

    if concurrent_times:
        avg_time = statistics.mean(concurrent_times)
        max_time = max(concurrent_times)

        print(f"\nConcurrent Loading Results:")
        print(f"Average response time: {avg_time:.3f}s")
        print(f"Max response time: {max_time:.3f}s")

        if max_time < 2.0:
            print("✅ PASSED: Concurrent max response time < 2s")
        else:
            print("❌ FAILED: Concurrent max response time >= 2s")

    return concurrent_times

def test_specific_content_loading():
    """
    Test loading specific content items if available
    """
    print("\nTesting specific content loading...")

    # First, get the list of available content
    try:
        response = requests.get(f"{BASE_URL}/api/content")
        if response.status_code == 200:
            content_list = response.json()
            if content_list and 'items' in content_list and len(content_list['items']) > 0:
                # Test loading the first few content items
                for i, item in enumerate(content_list['items'][:3]):  # Test first 3 items
                    content_id = item.get('id')
                    if content_id:
                        start_time = time.time()
                        detail_response = requests.get(f"{BASE_URL}/api/content/{content_id}")
                        response_time = time.time() - start_time

                        print(f"Content '{item.get('title', content_id)}': {response_time:.3f}s - Status: {detail_response.status_code}")

                        if response_time > 2.0:
                            print(f"  ❌ FAILED: Response time >= 2s")
                        else:
                            print(f"  ✅ PASSED: Response time < 2s")
            else:
                print("No content items found to test")
        else:
            print(f"Failed to get content list: {response.status_code}")
    except Exception as e:
        print(f"Error testing specific content: {str(e)}")

def main():
    """
    Main function to run all performance tests
    """
    print("AI-Native Book Performance Test Suite")
    print("=" * 50)

    # Test sequential content loading
    content_times = test_content_loading_performance()

    # Test concurrent loading
    concurrent_times = test_concurrent_content_loading()

    # Test specific content loading
    test_specific_content_loading()

    print("\n" + "=" * 50)
    print("Performance Test Complete")

    # Summary
    if content_times:
        avg_time = statistics.mean(content_times)
        max_time = max(content_times)

        print(f"Overall Summary:")
        print(f"- Average response time: {avg_time:.3f}s")
        print(f"- Max response time: {max_time:.3f}s")
        print(f"- Performance goal (<2s): {'✅ ACHIEVED' if max_time < 2.0 else '❌ NOT MET'}")

if __name__ == "__main__":
    main()