"""
Monitoring and error tracking abstraction.

Provides error tracking (Sentry) and Application Performance Monitoring (APM).
Works with or without monitoring services - controlled via environment variables.

Usage:
    from app.core.monitoring import monitor

    # Track exception
    try:
        risky_operation()
    except Exception as e:
        monitor.capture_exception(e, context={"user_id": 123})

    # Track custom event
    monitor.capture_message("Payment processed", level="info", extra={"amount": 1000})

    # Track performance
    with monitor.trace("database_query"):
        result = db.query(...)

Environment Variables:
    SENTRY_ENABLED: Enable/disable Sentry (default: false)
    SENTRY_DSN: Sentry DSN (required if SENTRY_ENABLED=true)
    SENTRY_ENVIRONMENT: Environment name (dev, staging, prod)
    SENTRY_TRACES_SAMPLE_RATE: Performance monitoring sample rate (0.0-1.0)
"""

import os
from typing import Any, Optional, Dict
from contextlib import contextmanager


class MonitoringService:
    """
    Monitoring service with optional Sentry backend.

    Safe to use without Sentry configured - no-ops if disabled.
    """

    def __init__(self):
        self.enabled = os.getenv("SENTRY_ENABLED", "false").lower() == "true"
        self._sentry = None

        if self.enabled:
            try:
                import sentry_sdk

                dsn = os.getenv("SENTRY_DSN")
                if not dsn:
                    raise ValueError("SENTRY_DSN not set but SENTRY_ENABLED=true")

                environment = os.getenv("SENTRY_ENVIRONMENT", os.getenv("ENV", "development"))
                traces_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1"))
                release = os.getenv("SENTRY_RELEASE", "unknown")

                sentry_sdk.init(
                    dsn=dsn,
                    environment=environment,
                    traces_sample_rate=traces_sample_rate,
                    release=release,
                    send_default_pii=False,  # Don't send PII by default
                )

                self._sentry = sentry_sdk
                print(f"✅ Sentry monitoring enabled (env: {environment})")
            except Exception as e:
                print(f"⚠️ Sentry initialization failed: {e}. Monitoring disabled.")
                self.enabled = False
                self._sentry = None
        else:
            print("ℹ️ Sentry monitoring disabled.")

    def capture_exception(
        self,
        exception: Exception,
        context: Optional[Dict[str, Any]] = None,
        level: str = "error"
    ) -> Optional[str]:
        """
        Capture and report an exception.

        Args:
            exception: The exception to capture
            context: Additional context (user_id, request_id, etc.)
            level: Error level (error, warning, info)

        Returns:
            Event ID if sent to Sentry, None otherwise

        Example:
            try:
                process_payment(amount=1000)
            except PaymentError as e:
                monitor.capture_exception(e, context={"user_id": 123, "amount": 1000})
        """
        if not self.enabled or not self._sentry:
            # In development, just print the error
            print(f"❌ Exception: {type(exception).__name__}: {exception}")
            if context:
                print(f"   Context: {context}")
            return None

        # Add context to Sentry scope
        with self._sentry.push_scope() as scope:
            scope.level = level
            if context:
                for key, value in context.items():
                    scope.set_context(key, {"value": value})

            event_id = self._sentry.capture_exception(exception)
            return event_id

    def capture_message(
        self,
        message: str,
        level: str = "info",
        extra: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Capture a custom message/event.

        Args:
            message: Message to capture
            level: Log level (debug, info, warning, error, fatal)
            extra: Additional data

        Returns:
            Event ID if sent to Sentry, None otherwise

        Example:
            monitor.capture_message(
                "Payment threshold exceeded",
                level="warning",
                extra={"amount": 10000, "threshold": 5000}
            )
        """
        if not self.enabled or not self._sentry:
            print(f"ℹ️ Message: {message}")
            if extra:
                print(f"   Extra: {extra}")
            return None

        with self._sentry.push_scope() as scope:
            scope.level = level
            if extra:
                scope.set_context("extra", extra)

            event_id = self._sentry.capture_message(message)
            return event_id

    def set_user(self, user_id: str, email: Optional[str] = None, username: Optional[str] = None):
        """
        Set user context for error tracking.

        Args:
            user_id: User identifier
            email: User email (optional)
            username: User name (optional)

        Example:
            monitor.set_user(user_id="123", email="user@example.com")
        """
        if not self.enabled or not self._sentry:
            return

        user_data = {"id": user_id}
        if email:
            user_data["email"] = email
        if username:
            user_data["username"] = username

        self._sentry.set_user(user_data)

    def set_context(self, key: str, value: Dict[str, Any]):
        """
        Add custom context to error reports.

        Args:
            key: Context key
            value: Context data

        Example:
            monitor.set_context("payment", {
                "method": "stripe",
                "amount": 1000,
                "currency": "usd"
            })
        """
        if not self.enabled or not self._sentry:
            return

        self._sentry.set_context(key, value)

    def add_breadcrumb(self, message: str, category: str = "default", level: str = "info", data: Optional[Dict] = None):
        """
        Add a breadcrumb (trail of events leading to error).

        Args:
            message: Breadcrumb message
            category: Category (navigation, http, db, etc.)
            level: Level (debug, info, warning, error)
            data: Additional data

        Example:
            monitor.add_breadcrumb("User clicked payment button", category="ui", data={"button_id": "pay-now"})
            monitor.add_breadcrumb("Payment API called", category="http", data={"endpoint": "/api/payments"})
            # If error occurs, Sentry shows these breadcrumbs
        """
        if not self.enabled or not self._sentry:
            return

        self._sentry.add_breadcrumb(
            message=message,
            category=category,
            level=level,
            data=data or {}
        )

    @contextmanager
    def trace(self, operation: str):
        """
        Context manager for performance tracing.

        Args:
            operation: Operation name

        Example:
            with monitor.trace("database_query"):
                users = db.query(User).all()

            with monitor.trace("api_call"):
                response = requests.post(url, data=payload)
        """
        if not self.enabled or not self._sentry:
            # No-op if monitoring disabled
            yield
            return

        transaction = self._sentry.start_transaction(op=operation, name=operation)
        try:
            yield transaction
        finally:
            transaction.finish()


# Global monitoring instance
monitor = MonitoringService()
