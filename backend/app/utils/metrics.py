"""
Metrics collection and monitoring for AI-Native Book backend
"""
import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MetricsCollector:
    """
    Collects and manages application metrics
    """
    def __init__(self, retention_minutes=60):
        self.retention_seconds = retention_minutes * 60
        self.lock = threading.Lock()

        # Request metrics
        self.request_counts = defaultdict(int)
        self.response_times = defaultdict(lambda: deque(maxlen=1000))  # Keep last 1000 measurements
        self.status_codes = defaultdict(int)

        # Performance metrics
        self.performance_metrics = defaultdict(lambda: deque(maxlen=1000))

        # Error metrics
        self.error_counts = defaultdict(int)

        # Cache metrics
        self.cache_hits = 0
        self.cache_misses = 0

        # Search metrics
        self.search_queries = deque(maxlen=1000)

        # AI assistant metrics
        self.ai_requests = deque(maxlen=1000)

    def record_request(self, endpoint: str, method: str, response_time: float, status_code: int):
        """
        Record a request metric
        """
        with self.lock:
            key = f"{method}:{endpoint}"
            self.request_counts[key] += 1
            self.response_times[key].append(response_time)
            self.status_codes[status_code] += 1

    def record_performance_metric(self, metric_name: str, value: float, labels: Optional[Dict] = None):
        """
        Record a performance metric
        """
        with self.lock:
            key = metric_name
            if labels:
                key = f"{metric_name}_" + "_".join([f"{k}_{v}" for k, v in labels.items()])
            self.performance_metrics[key].append(value)

    def record_error(self, error_type: str, endpoint: str = None):
        """
        Record an error
        """
        with self.lock:
            key = error_type
            if endpoint:
                key = f"{error_type}:{endpoint}"
            self.error_counts[key] += 1

    def record_cache_operation(self, hit: bool):
        """
        Record a cache operation
        """
        with self.lock:
            if hit:
                self.cache_hits += 1
            else:
                self.cache_misses += 1

    def record_search_query(self, query: str, results_count: int, response_time: float):
        """
        Record a search query
        """
        with self.lock:
            self.search_queries.append({
                'query': query,
                'results_count': results_count,
                'response_time': response_time,
                'timestamp': datetime.now()
            })

    def record_ai_request(self, question: str, response_time: float, success: bool, tokens: int = 0):
        """
        Record an AI assistant request
        """
        with self.lock:
            self.ai_requests.append({
                'question_length': len(question),
                'response_time': response_time,
                'success': success,
                'tokens': tokens,
                'timestamp': datetime.now()
            })

    def get_request_rate(self, endpoint: str = None, method: str = None,
                        time_window_minutes: int = 1) -> float:
        """
        Get request rate for a specific endpoint/method in requests per minute
        """
        # This would require storing timestamps to calculate rates
        # For now, return a simple calculation based on counts
        with self.lock:
            if endpoint and method:
                key = f"{method}:{endpoint}"
                return self.request_counts[key] / time_window_minutes
            elif endpoint:
                # Sum all methods for this endpoint
                total = 0
                for k, v in self.request_counts.items():
                    if k.endswith(f":{endpoint}"):
                        total += v
                return total / time_window_minutes
            else:
                # Total rate across all endpoints
                return sum(self.request_counts.values()) / time_window_minutes

    def get_average_response_time(self, endpoint: str = None, method: str = None) -> float:
        """
        Get average response time for a specific endpoint/method
        """
        with self.lock:
            if endpoint and method:
                key = f"{method}:{endpoint}"
                times = self.response_times[key]
                return sum(times) / len(times) if times else 0.0
            elif endpoint:
                # Average across all methods for this endpoint
                total_time = 0
                total_count = 0
                for k, times in self.response_times.items():
                    if k.endswith(f":{endpoint}"):
                        total_time += sum(times)
                        total_count += len(times)
                return total_time / total_count if total_count > 0 else 0.0
            else:
                # Overall average
                total_time = 0
                total_count = 0
                for times in self.response_times.values():
                    total_time += sum(times)
                    total_count += len(times)
                return total_time / total_count if total_count > 0 else 0.0

    def get_error_rate(self) -> float:
        """
        Get overall error rate as percentage
        """
        with self.lock:
            total_requests = sum(self.request_counts.values())
            total_errors = sum(self.status_codes[k] for k in self.status_codes.keys() if k >= 400)
            return (total_errors / total_requests * 100) if total_requests > 0 else 0.0

    def get_cache_hit_rate(self) -> float:
        """
        Get cache hit rate as percentage
        """
        with self.lock:
            total_ops = self.cache_hits + self.cache_misses
            return (self.cache_hits / total_ops * 100) if total_ops > 0 else 0.0

    def get_metrics_summary(self) -> Dict:
        """
        Get a summary of all metrics
        """
        with self.lock:
            return {
                'timestamp': datetime.now().isoformat(),
                'request_counts': dict(self.request_counts),
                'status_codes': dict(self.status_codes),
                'error_counts': dict(self.error_counts),
                'cache': {
                    'hits': self.cache_hits,
                    'misses': self.cache_misses,
                    'hit_rate': self.get_cache_hit_rate()
                },
                'request_rate_per_minute': self.get_request_rate(),
                'average_response_time': self.get_average_response_time(),
                'error_rate_percent': self.get_error_rate(),
                'search_stats': {
                    'total_queries': len(self.search_queries),
                    'avg_response_time': sum(s['response_time'] for s in self.search_queries) / len(self.search_queries) if self.search_queries else 0,
                    'avg_results': sum(s['results_count'] for s in self.search_queries) / len(self.search_queries) if self.search_queries else 0
                },
                'ai_stats': {
                    'total_requests': len(self.ai_requests),
                    'avg_response_time': sum(a['response_time'] for a in self.ai_requests) / len(self.ai_requests) if self.ai_requests else 0,
                    'success_rate': sum(1 for a in self.ai_requests if a['success']) / len(self.ai_requests) * 100 if self.ai_requests else 0
                }
            }

# Global metrics collector instance
metrics = MetricsCollector()

def time_request(endpoint: str, method: str):
    """
    Decorator to time requests and record metrics
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                response_time = time.time() - start_time
                metrics.record_request(endpoint, method, response_time, 200)  # Assuming success
                return result
            except Exception as e:
                response_time = time.time() - start_time
                metrics.record_request(endpoint, method, response_time, 500)  # Error status
                metrics.record_error(type(e).__name__, endpoint)
                raise
        return wrapper
    return decorator

def record_performance(metric_name: str, labels: Optional[Dict] = None):
    """
    Decorator to record performance metrics
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                metrics.record_performance_metric(metric_name, execution_time, labels)
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                metrics.record_performance_metric(f"{metric_name}_error", execution_time, labels)
                raise
        return wrapper
    return decorator

def monitor_search():
    """
    Decorator to monitor search functionality
    """
    def decorator(func):
        def wrapper(query, *args, **kwargs):
            start_time = time.time()
            try:
                result = func(query, *args, **kwargs)
                response_time = time.time() - start_time
                metrics.record_search_query(query, len(result) if isinstance(result, list) else 0, response_time)
                return result
            except Exception as e:
                response_time = time.time() - start_time
                metrics.record_search_query(query, 0, response_time)
                metrics.record_error(f"search_{type(e).__name__}", "search")
                raise
        return wrapper
    return decorator

def monitor_ai_assistant():
    """
    Decorator to monitor AI assistant functionality
    """
    def decorator(func):
        def wrapper(question, *args, **kwargs):
            start_time = time.time()
            try:
                result = func(question, *args, **kwargs)
                response_time = time.time() - start_time
                # For now, we'll just record the basic request; token count would come from actual AI service
                metrics.record_ai_request(question, response_time, True)
                return result
            except Exception as e:
                response_time = time.time() - start_time
                metrics.record_ai_request(question, response_time, False)
                metrics.record_error(f"ai_{type(e).__name__}", "ai_assistant")
                raise
        return wrapper
    return decorator

# Example usage functions
def log_request_middleware(request, call_next):
    """
    Example middleware to log and time requests
    """
    start_time = time.time()
    response = call_next(request)
    response_time = time.time() - start_time

    metrics.record_request(
        endpoint=str(request.url.path),
        method=request.method,
        response_time=response_time,
        status_code=response.status_code
    )

    return response

def get_health_metrics():
    """
    Get health-related metrics for the health check endpoint
    """
    summary = metrics.get_metrics_summary()

    # Determine health status based on metrics
    error_rate = summary['error_rate_percent']
    avg_response_time = summary['average_response_time']

    if error_rate > 10 or avg_response_time > 5.0:  # More than 10% errors or >5s avg response
        status = "unhealthy"
    elif error_rate > 5 or avg_response_time > 2.0:  # More than 5% errors or >2s avg response
        status = "degraded"
    else:
        status = "healthy"

    return {
        "status": status,
        "metrics": summary
    }