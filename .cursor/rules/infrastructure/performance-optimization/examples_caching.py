"""
Caching Pattern Example

This file demonstrates the generic cache-aside pattern for Redis and in-memory caching.
Reference this example from RULE.mdc using @examples_caching.py syntax.
"""

from typing import Any, Callable, TypeVar
from functools import wraps
import redis
import json

T = TypeVar('T')


# ============================================================================
# Cache-Aside Pattern
# ============================================================================

class CacheService:
    """
    Generic cache service pattern using cache-aside strategy.
    
    This demonstrates the cache-aside pattern:
    1. Check cache for data
    2. If miss, fetch from source
    3. Store in cache for future requests
    4. Return data to caller
    """
    
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        """
        Initialize cache service.
        
        Args:
            redis_client: Redis client instance
            ttl: Time-to-live for cached data in seconds
        """
        self.redis = redis_client
        self.ttl = ttl
    
    def get_or_fetch(
        self,
        key: str,
        fetch_func: Callable[[], T]
    ) -> T:
        """
        Get data from cache or fetch from source.
        
        This demonstrates the cache-aside pattern:
        - Check cache first
        - If cache miss, fetch from source
        - Store in cache for future requests
        
        Args:
            key: Cache key
            fetch_func: Function to fetch data if cache miss
            
        Returns:
            Cached or fetched data
        """
        # Check cache
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        
        # Cache miss - fetch from source
        data = fetch_func()
        
        # Store in cache
        self.redis.setex(
            key,
            self.ttl,
            json.dumps(data)
        )
        
        return data


# ============================================================================
# In-Memory Cache Decorator Pattern
# ============================================================================

def cache_result(max_size: int = 128):
    """
    Generic in-memory cache decorator pattern.
    
    This demonstrates the pattern for function result caching:
    - Cache function results in memory
    - Limit cache size to prevent memory issues
    - Use LRU eviction when cache is full
    
    Args:
        max_size: Maximum number of cached results
    """
    cache: dict = {}
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create cache key from function arguments
            cache_key = str((args, tuple(sorted(kwargs.items()))))
            
            # Check cache
            if cache_key in cache:
                return cache[cache_key]
            
            # Cache miss - execute function
            result = func(*args, **kwargs)
            
            # Store in cache (with size limit)
            if len(cache) >= max_size:
                # Remove oldest entry (simple FIFO)
                cache.pop(next(iter(cache)))
            
            cache[cache_key] = result
            return result
        
        return wrapper
    
    return decorator
