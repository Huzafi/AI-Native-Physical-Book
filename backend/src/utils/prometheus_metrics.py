"""Prometheus metrics integration for the RAG Chatbot application."""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
import time
import asyncio
from typing import Optional


# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'active_requests',
    'Number of active requests',
)

QUERY_COUNT = Counter(
    'query_requests_total',
    'Total number of query requests',
    ['type']
)

QUERY_DURATION = Histogram(
    'query_duration_seconds',
    'Duration of query processing in seconds',
    ['type']
)

ERROR_COUNT = Counter(
    'error_count_total',
    'Total number of errors',
    ['type']
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Prometheus metrics middleware for FastAPI."""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method
        path = request.url.path
        
        # Increment active requests gauge
        ACTIVE_REQUESTS.inc()
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
        except Exception as e:
            # Increment error counter
            ERROR_COUNT.labels(type=type(e).__name__).inc()
            raise e
        finally:
            # Record request duration
            duration = time.time() - start_time
            
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status_code=response.status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=path
            ).observe(duration)
            
            # Decrement active requests gauge
            ACTIVE_REQUESTS.dec()
        
        return response


def get_metrics():
    """Get Prometheus metrics in text format."""
    return Response(generate_latest(REGISTRY), media_type="text/plain")


def increment_query_counter(query_type: str):
    """Increment the query counter."""
    QUERY_COUNT.labels(type=query_type).inc()


def record_query_duration(query_type: str, duration: float):
    """Record query duration."""
    QUERY_DURATION.labels(type=query_type).observe(duration)


def increment_error_counter(error_type: str):
    """Increment the error counter."""
    ERROR_COUNT.labels(type=error_type).inc()