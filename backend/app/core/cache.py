"""
Cache abstraction layer.

Provides caching functionality with optional Redis backend.
Works with or without Redis - controlled via environment variables.

Usage:
    from app.core.cache import cache

    # Set value
    cache.set("user:123", user_data, ttl=3600)

    # Get value
    user = cache.get("user:123")

    # Delete value
    cache.delete("user:123")

    # Clear all cache
    cache.clear()

Environment Variables:
    REDIS_ENABLED: Enable/disable Redis caching (default: false)
    REDIS_URL: Redis connection URL (required if REDIS_ENABLED=true)
"""

import os
import json
from typing import Any, Optional
from datetime import timedelta


class CacheService:
    """
    Cache service with optional Redis backend.

    Falls back to in-memory dict if Redis is disabled.
    Safe to use in development without Redis.
    """

    def __init__(self):
        self.enabled = os.getenv("REDIS_ENABLED", "false").lower() == "true"
        self._redis_client = None
        self._memory_cache = {}  # Fallback in-memory cache

        if self.enabled:
            try:
                import redis
                redis_url = os.getenv("REDIS_URL")
                if not redis_url:
                    raise ValueError("REDIS_URL not set but REDIS_ENABLED=true")

                self._redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True
                )
                # Test connection
                self._redis_client.ping()
                print("✅ Redis cache enabled and connected")
            except Exception as e:
                print(f"⚠️ Redis connection failed: {e}. Falling back to in-memory cache.")
                self.enabled = False
                self._redis_client = None
        else:
            print("ℹ️ Redis cache disabled. Using in-memory cache.")

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if self.enabled and self._redis_client:
            try:
                value = self._redis_client.get(key)
                if value:
                    # Try to deserialize JSON
                    try:
                        return json.loads(value)
                    except json.JSONDecodeError:
                        return value
                return None
            except Exception as e:
                print(f"⚠️ Redis get error: {e}")
                return None
        else:
            # In-memory cache
            return self._memory_cache.get(key)

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default: 1 hour)

        Returns:
            True if successful, False otherwise
        """
        if self.enabled and self._redis_client:
            try:
                # Serialize to JSON if not string
                if not isinstance(value, str):
                    value = json.dumps(value)

                self._redis_client.setex(key, ttl, value)
                return True
            except Exception as e:
                print(f"⚠️ Redis set error: {e}")
                return False
        else:
            # In-memory cache (no TTL support in simple dict)
            self._memory_cache[key] = value
            return True

    def delete(self, key: str) -> bool:
        """
        Delete value from cache.

        Args:
            key: Cache key to delete

        Returns:
            True if successful, False otherwise
        """
        if self.enabled and self._redis_client:
            try:
                self._redis_client.delete(key)
                return True
            except Exception as e:
                print(f"⚠️ Redis delete error: {e}")
                return False
        else:
            # In-memory cache
            if key in self._memory_cache:
                del self._memory_cache[key]
            return True

    def clear(self) -> bool:
        """
        Clear all cache entries.

        ⚠️ Use with caution in production!

        Returns:
            True if successful, False otherwise
        """
        if self.enabled and self._redis_client:
            try:
                self._redis_client.flushdb()
                return True
            except Exception as e:
                print(f"⚠️ Redis clear error: {e}")
                return False
        else:
            # In-memory cache
            self._memory_cache.clear()
            return True

    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key to check

        Returns:
            True if key exists, False otherwise
        """
        if self.enabled and self._redis_client:
            try:
                return bool(self._redis_client.exists(key))
            except Exception as e:
                print(f"⚠️ Redis exists error: {e}")
                return False
        else:
            return key in self._memory_cache

    def get_many(self, keys: list[str]) -> dict[str, Any]:
        """
        Get multiple values from cache.

        Args:
            keys: List of cache keys

        Returns:
            Dictionary of key: value pairs
        """
        result = {}
        for key in keys:
            value = self.get(key)
            if value is not None:
                result[key] = value
        return result

    def set_many(self, mapping: dict[str, Any], ttl: int = 3600) -> bool:
        """
        Set multiple values in cache.

        Args:
            mapping: Dictionary of key: value pairs
            ttl: Time to live in seconds

        Returns:
            True if all successful, False if any failed
        """
        success = True
        for key, value in mapping.items():
            if not self.set(key, value, ttl):
                success = False
        return success


# Global cache instance
cache = CacheService()
