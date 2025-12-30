"""
Core services and abstractions.

This module provides environment-aware abstractions for common services:
- Cache (Redis)
- Logging (structured JSON logs)
- Monitoring (Sentry, APM)
- Payment (Stripe)

All services work with or without external providers configured.
Enable/disable services via environment variables in .env files.

Usage:
    from app.core import cache, get_logger, monitor, payment

    logger = get_logger(__name__)

    def get_user(user_id):
        # Try cache
        cached = cache.get(f"user:{user_id}")
        if cached:
            return cached

        # Query DB
        user = db.query(User).filter(User.id == user_id).first()

        # Store in cache
        cache.set(f"user:{user_id}", user.dict(), ttl=3600)

        logger.info("User fetched", extra={"user_id": user_id})
        return user
"""

from .cache import cache, CacheService
from .logger import get_logger, log_request, log_db_query, log_error, app_logger
from .monitoring import monitor, MonitoringService
from .payment import payment, PaymentService, PaymentStatus, PaymentError

__all__ = [
    # Cache
    "cache",
    "CacheService",

    # Logging
    "get_logger",
    "log_request",
    "log_db_query",
    "log_error",
    "app_logger",

    # Monitoring
    "monitor",
    "MonitoringService",

    # Payment
    "payment",
    "PaymentService",
    "PaymentStatus",
    "PaymentError",
]

__version__ = "1.0.0"
