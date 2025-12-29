"""Monitoring and metrics collection for the RAG Chatbot application."""

import time
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
from collections import defaultdict, deque
import json
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class MetricType(Enum):
    """Types of metrics that can be collected."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """Represents a single metric."""
    name: str
    type: MetricType
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class MetricsCollector:
    """Collects and stores application metrics."""

    def __init__(self):
        self._metrics: Dict[str, Metric] = {}
        self._lock = threading.Lock()
        self._request_times = deque(maxlen=1000)  # Store last 1000 request times
        self._request_counter = 0
        self._error_counter = 0
        self._query_counter = 0
        self._response_times = deque(maxlen=1000)  # Store last 1000 response times

        # Set up logging for metrics
        self.logger = logging.getLogger(__name__ + ".metrics")

    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None, amount: float = 1.0):
        """Increment a counter metric."""
        labels = labels or {}
        key = f"{name}:{json.dumps(sorted(labels.items()))}"

        with self._lock:
            if key in self._metrics:
                self._metrics[key].value += amount
            else:
                self._metrics[key] = Metric(
                    name=name,
                    type=MetricType.COUNTER,
                    value=amount,
                    labels=labels
                )

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric to a specific value."""
        labels = labels or {}
        key = f"{name}:{json.dumps(sorted(labels.items()))}"

        with self._lock:
            self._metrics[key] = Metric(
                name=name,
                type=MetricType.GAUGE,
                value=value,
                labels=labels
            )

    def record_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a value in a histogram."""
        labels = labels or {}
        key = f"{name}:{json.dumps(sorted(labels.items()))}"

        with self._lock:
            # For histograms, we'll store the value in a special way
            # In a real implementation, you'd have buckets and counts
            if key in self._metrics:
                # Update existing histogram
                current_value = self._metrics[key].value
                self._metrics[key] = Metric(
                    name=name,
                    type=MetricType.HISTOGRAM,
                    value=(current_value + value) / 2,  # Simple average
                    labels=labels
                )
            else:
                self._metrics[key] = Metric(
                    name=name,
                    type=MetricType.HISTOGRAM,
                    value=value,
                    labels=labels
                )

    def record_request_time(self, duration: float):
        """Record the time it took to process a request."""
        with self._lock:
            self._request_times.append(duration)
            self._request_counter += 1

    def record_response_time(self, duration: float):
        """Record the time it took to generate a response."""
        with self._lock:
            self._response_times.append(duration)
            self._query_counter += 1

    def increment_error_counter(self):
        """Increment the error counter."""
        with self._lock:
            self._error_counter += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        with self._lock:
            # Calculate derived metrics
            avg_request_time = sum(self._request_times) / len(self._request_times) if self._request_times else 0
            avg_response_time = sum(self._response_times) / len(self._response_times) if self._response_times else 0
            error_rate = self._error_counter / self._request_counter if self._request_counter > 0 else 0

            # Add calculated metrics
            calculated_metrics = {
                "avg_request_time": avg_request_time,
                "avg_response_time": avg_response_time,
                "error_rate": error_rate,
                "request_count": self._request_counter,
                "error_count": self._error_counter,
                "query_count": self._query_counter
            }

            # Return both stored and calculated metrics
            result = {
                "stored_metrics": {k: {
                    "name": v.name,
                    "type": v.type.value,
                    "value": v.value,
                    "labels": v.labels,
                    "timestamp": v.timestamp.isoformat()
                } for k, v in self._metrics.items()},
                "calculated_metrics": calculated_metrics
            }

            return result

    def log_metrics(self):
        """Log current metrics to the application log."""
        metrics = self.get_metrics()
        self.logger.info(f"Application Metrics: {json.dumps(metrics, indent=2)}")


# Global metrics collector instance
metrics_collector = MetricsCollector()


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect metrics for FastAPI requests."""

    def __init__(self, app):
        super().__init__(app)
        self.collector = metrics_collector

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as e:
            # Increment error counter if an exception occurs
            self.collector.increment_error_counter()
            raise e
        finally:
            # Record request processing time
            duration = time.time() - start_time
            self.collector.record_request_time(duration)

            # Add metrics to response headers (optional)
            response.headers["X-Request-Duration"] = str(duration)

        return response


def monitor_function(func):
    """Decorator to monitor function execution time."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            metrics_collector.record_response_time(duration)
            # Also increment query counter for monitored functions
            if 'query' in func.__name__.lower() or 'search' in func.__name__.lower():
                metrics_collector.increment_counter("function_calls", {"function": func.__name__})
    return wrapper


def log_api_metrics(endpoint: str, method: str, response_time: float, status_code: int):
    """Log metrics for API endpoint calls."""
    metrics_collector.increment_counter("api_requests", {"endpoint": endpoint, "method": method, "status": str(status_code)})
    metrics_collector.record_histogram("api_response_time", response_time, {"endpoint": endpoint, "method": method})


def log_query_metrics(query_type: str, response_time: float, confidence_score: float):
    """Log metrics for query processing."""
    metrics_collector.increment_counter("queries_processed", {"type": query_type})
    metrics_collector.record_histogram("query_response_time", response_time, {"type": query_type})
    metrics_collector.record_histogram("query_confidence", confidence_score, {"type": query_type})