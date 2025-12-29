"""Caching utilities for the RAG Chatbot application."""

import time
import threading
from typing import Any, Optional, Dict
from functools import wraps
from datetime import datetime, timedelta


class InMemoryCache:
    """Simple in-memory cache with TTL (Time To Live) support."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                # Check if the entry has expired
                if entry['expires_at'] is None or entry['expires_at'] > datetime.utcnow():
                    return entry['value']
                else:
                    # Remove expired entry
                    del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set a value in the cache with an optional TTL."""
        with self._lock:
            expires_at = None
            if ttl_seconds:
                expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
            
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at
            }
    
    def delete(self, key: str) -> bool:
        """Delete a key from the cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self) -> None:
        """Remove all expired entries from the cache."""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry['expires_at'] and entry['expires_at'] <= datetime.utcnow()
            ]
            for key in expired_keys:
                del self._cache[key]


# Global cache instance
cache = InMemoryCache()


def cached(ttl_seconds: int = 300):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on function name and arguments
            cache_key = f"{func.__module__}.{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute the function and cache the result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            
            return result
        return wrapper
    return decorator


def cache_result(key: str, ttl_seconds: int = 300):
    """Decorator to cache function results with a custom key."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use the provided key
            cache_key = key
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute the function and cache the result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            
            return result
        return wrapper
    return decorator


def invalidate_cache(key: str):
    """Invalidate a specific cache key."""
    return cache.delete(key)


def invalidate_cache_pattern(pattern: str):
    """Invalidate cache keys matching a pattern."""
    with cache._lock:
        keys_to_delete = [key for key in cache._cache.keys() if pattern in key]
        for key in keys_to_delete:
            del cache._cache[key]