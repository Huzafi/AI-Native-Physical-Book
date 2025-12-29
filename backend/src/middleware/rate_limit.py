"""Rate limiting middleware for the RAG Chatbot application."""

import time
from typing import Dict
from fastapi import Request, HTTPException
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, requests: int = 100, window: int = 60):
        """
        Initialize the rate limiter.
        
        Args:
            requests: Number of requests allowed per window
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.requests_log: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.
        
        Args:
            identifier: Unique identifier for the requester (e.g., IP address)
            
        Returns:
            True if the request is allowed, False otherwise
        """
        current_time = time.time()
        
        # Remove old requests outside the window
        self.requests_log[identifier] = [
            req_time for req_time in self.requests_log[identifier]
            if current_time - req_time < self.window
        ]
        
        # Check if the number of requests is within the limit
        if len(self.requests_log[identifier]) < self.requests:
            # Add the current request to the log
            self.requests_log[identifier].append(current_time)
            return True
        
        return False


# Create a global rate limiter instance
rate_limiter = RateLimiter(requests=100, window=60)  # 100 requests per minute


async def rate_limit_middleware(request: Request, call_next):
    """Middleware to enforce rate limiting."""
    # Get the client IP address
    client_ip = request.client.host
    
    # Check if the request is allowed
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Rate limit exceeded. Please try again later."
                }
            }
        )
    
    response = await call_next(request)
    return response