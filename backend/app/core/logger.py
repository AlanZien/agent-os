"""
Structured logging abstraction.

Provides JSON-formatted logging ready for log aggregation services (Logtail, Datadog, etc.).
Works in development and production with appropriate log levels.

Usage:
    from app.core.logger import get_logger

    logger = get_logger(__name__)

    logger.info("User created", extra={"user_id": 123, "email": "user@example.com"})
    logger.error("Payment failed", extra={"error": str(e), "amount": 1000})

Environment Variables:
    LOG_LEVEL: Logging level (DEBUG, INFO, WARN, ERROR) - default: INFO
    LOG_FORMAT: Output format (json or text) - default: json
    ENV: Environment (dev, staging, prod) - affects defaults
"""

import os
import logging
import sys
from typing import Optional


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (usually __name__ of the module)

    Returns:
        Configured logger instance

    Example:
        logger = get_logger(__name__)
        logger.info("Operation completed", extra={"user_id": 123})
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if logger.handlers:
        return logger

    # Get configuration from environment
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = os.getenv("LOG_FORMAT", "json").lower()
    env = os.getenv("ENV", "dev").lower()

    # Set log level
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARNING,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logger.setLevel(level_map.get(log_level, logging.INFO))

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    # Choose formatter based on format and environment
    if log_format == "json" or env in ["staging", "prod"]:
        # JSON formatter for production (structured logs)
        try:
            from pythonjsonlogger import jsonlogger

            formatter = jsonlogger.JsonFormatter(
                "%(asctime)s %(name)s %(levelname)s %(message)s",
                rename_fields={
                    "asctime": "timestamp",
                    "name": "logger",
                    "levelname": "level",
                },
            )
        except ImportError:
            # Fallback if pythonjsonlogger not installed
            print("⚠️ pythonjsonlogger not installed. Using text format.")
            print("   Install with: pip install python-json-logger")
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
    else:
        # Text formatter for development (human-readable)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Prevent propagation to root logger (avoid duplicate logs)
    logger.propagate = False

    return logger


# Example usage and patterns
def log_request(logger: logging.Logger, method: str, path: str, status: int, duration_ms: float):
    """
    Helper to log HTTP requests consistently.

    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status: HTTP status code
        duration_ms: Request duration in milliseconds

    Example:
        log_request(logger, "GET", "/api/users/123", 200, 45.2)
    """
    logger.info(
        "HTTP request",
        extra={
            "method": method,
            "path": path,
            "status_code": status,
            "duration_ms": round(duration_ms, 2),
        },
    )


def log_db_query(logger: logging.Logger, query: str, duration_ms: float, rows: Optional[int] = None):
    """
    Helper to log database queries consistently.

    Args:
        logger: Logger instance
        query: SQL query (or description)
        duration_ms: Query duration in milliseconds
        rows: Number of rows affected (optional)

    Example:
        log_db_query(logger, "SELECT * FROM users", 23.4, rows=150)
    """
    extra = {
        "query": query,
        "duration_ms": round(duration_ms, 2),
    }
    if rows is not None:
        extra["rows"] = rows

    logger.debug("Database query", extra=extra)


def log_error(logger: logging.Logger, error: Exception, context: Optional[dict] = None):
    """
    Helper to log errors consistently.

    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context (user_id, request_id, etc.)

    Example:
        try:
            process_payment()
        except Exception as e:
            log_error(logger, e, {"user_id": 123, "amount": 1000})
    """
    extra = {
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
    if context:
        extra.update(context)

    logger.error("Exception occurred", extra=extra, exc_info=True)


# Global application logger (use sparingly, prefer get_logger(__name__))
app_logger = get_logger("app")
