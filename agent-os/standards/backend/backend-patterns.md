# Backend Patterns & Core Services

This document defines the patterns and abstractions that **ALL backend code MUST follow**.

## Core Services (ALWAYS USE THESE)

The project includes pre-built abstractions in `backend/app/core/` for common services. **ALWAYS use these abstractions** instead of directly importing external packages.

### Available Core Services

| Service | Import | Purpose | Enabled by default |
|---------|--------|---------|-------------------|
| **Cache** | `from app.core import cache` | Redis caching | No (enable via `REDIS_ENABLED=true`) |
| **Logger** | `from app.core import get_logger` | Structured JSON logging | Yes |
| **Monitoring** | `from app.core import monitor` | Error tracking (Sentry), APM | No (enable via `SENTRY_ENABLED=true`) |
| **Payment** | `from app.core import payment` | Payment processing (Stripe) | No (enable via `STRIPE_ENABLED=true`) |

---

## Why Use Core Service Abstractions?

### ✅ Benefits

1. **Environment-aware**: Services can be disabled in dev, enabled in prod
2. **No refactoring needed**: Enable/disable via `.env` without code changes
3. **Consistent patterns**: All agents use the same approach
4. **Easy testing**: Mock abstractions instead of external services
5. **No external dependencies in dev**: Works without Redis, Sentry, Stripe installed
6. **Production-ready**: Same code works in dev and prod

### ❌ Don't Do This

```python
# WRONG - Direct imports
import redis
redis_client = redis.Redis(url="...")

import stripe
stripe.api_key = "..."

import sentry_sdk
sentry_sdk.init(...)
```

### ✅ Do This Instead

```python
# CORRECT - Use abstractions
from app.core import cache, get_logger, monitor, payment

logger = get_logger(__name__)

def process_payment_with_cache(user_id, amount):
    # Cache
    cached_result = cache.get(f"payment:{user_id}")
    if cached_result:
        return cached_result

    # Monitoring
    try:
        # Payment
        intent = payment.create_payment_intent(amount=amount)

        # Log
        logger.info("Payment created", extra={
            "user_id": user_id,
            "amount": amount,
            "intent_id": intent["id"]
        })

        # Cache result
        cache.set(f"payment:{user_id}", intent, ttl=300)

        return intent

    except Exception as e:
        # Capture exception
        monitor.capture_exception(e, context={"user_id": user_id})
        logger.error("Payment failed", extra={"error": str(e)})
        raise
```

---

## Service Usage Patterns

### 1. Cache (`app.core.cache`)

**Purpose:** Improve performance by caching expensive operations (DB queries, API calls, computations).

**Common Patterns:**

#### Pattern A: Cache DB query results

```python
from app.core import cache, get_logger

logger = get_logger(__name__)

def get_user(user_id: int):
    # Try cache first
    cache_key = f"user:{user_id}"
    cached = cache.get(cache_key)

    if cached:
        logger.debug("Cache hit", extra={"key": cache_key})
        return cached

    # Cache miss - query database
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        # Cache for 1 hour
        cache.set(cache_key, user.dict(), ttl=3600)
        logger.debug("Cache miss, cached result", extra={"key": cache_key})

    return user
```

#### Pattern B: Cache expensive computations

```python
def calculate_user_statistics(user_id: int):
    cache_key = f"stats:{user_id}"
    cached = cache.get(cache_key)

    if cached:
        return cached

    # Expensive computation
    stats = {
        "total_orders": db.query(Order).filter(Order.user_id == user_id).count(),
        "total_spent": db.query(func.sum(Order.total)).filter(Order.user_id == user_id).scalar(),
        "avg_order": # ... complex calculation
    }

    # Cache for 30 minutes
    cache.set(cache_key, stats, ttl=1800)

    return stats
```

#### Pattern C: Invalidate cache on updates

```python
def update_user(user_id: int, data: dict):
    # Update database
    user = db.query(User).filter(User.id == user_id).first()
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()

    # Invalidate cache
    cache.delete(f"user:{user_id}")
    cache.delete(f"stats:{user_id}")

    logger.info("User updated and cache invalidated", extra={"user_id": user_id})

    return user
```

---

### 2. Logger (`app.core.get_logger`)

**Purpose:** Structured logging ready for production (JSON format, log aggregation).

**Common Patterns:**

#### Pattern A: Initialize logger per module

```python
# At top of file
from app.core import get_logger

logger = get_logger(__name__)  # Uses module name

# Use throughout file
def my_function():
    logger.info("Function started")
    # ...
    logger.info("Function completed", extra={"result_count": count})
```

#### Pattern B: Log with structured data

```python
# GOOD - Structured (searchable in log aggregation)
logger.info("User login", extra={
    "user_id": user.id,
    "email": user.email,
    "ip_address": request.client.host,
    "user_agent": request.headers.get("user-agent")
})

# BAD - Unstructured (hard to search)
logger.info(f"User {user.email} logged in from {request.client.host}")
```

#### Pattern C: Log levels appropriately

```python
# DEBUG - Detailed info for development
logger.debug("Database query executed", extra={"query": sql, "duration_ms": 23.4})

# INFO - General information
logger.info("User created", extra={"user_id": user.id})

# WARNING - Something unusual but not an error
logger.warning("Rate limit approaching", extra={"user_id": user.id, "count": 95, "limit": 100})

# ERROR - Something went wrong
logger.error("Payment failed", extra={"error": str(e), "amount": amount})

# CRITICAL - System is in danger
logger.critical("Database connection lost", extra={"attempt": retry_count})
```

#### Pattern D: Use helper functions

```python
from app.core import log_request, log_db_query, log_error

# Log HTTP requests
log_request(logger, "GET", "/api/users/123", 200, duration_ms=45.2)

# Log database queries
log_db_query(logger, "SELECT * FROM users WHERE id = ?", duration_ms=23.4, rows=1)

# Log errors with context
try:
    process_payment()
except Exception as e:
    log_error(logger, e, context={"user_id": 123, "amount": 1000})
```

---

### 3. Monitoring (`app.core.monitor`)

**Purpose:** Track errors, performance, and user experience.

**Common Patterns:**

#### Pattern A: Capture exceptions

```python
from app.core import monitor, get_logger

logger = get_logger(__name__)

def risky_operation(user_id: int):
    try:
        result = external_api.call()
        return result

    except ExternalAPIError as e:
        # Capture in Sentry with context
        monitor.capture_exception(e, context={
            "user_id": user_id,
            "api": "external_api",
            "operation": "risky_operation"
        })

        # Also log locally
        logger.error("External API failed", extra={"error": str(e)})

        # Re-raise or handle
        raise
```

#### Pattern B: Track user context

```python
# Set user context at login
def login(user: User):
    # Set for monitoring
    monitor.set_user(
        user_id=str(user.id),
        email=user.email,
        username=user.username
    )

    # Now all errors will include user info
    logger.info("User logged in", extra={"user_id": user.id})
```

#### Pattern C: Add breadcrumbs for debugging

```python
def process_checkout(cart_id: int):
    monitor.add_breadcrumb("Checkout started", category="commerce", data={"cart_id": cart_id})

    cart = get_cart(cart_id)
    monitor.add_breadcrumb("Cart loaded", category="db", data={"items": len(cart.items)})

    total = calculate_total(cart)
    monitor.add_breadcrumb("Total calculated", category="compute", data={"total": total})

    try:
        payment_intent = payment.create_payment_intent(amount=total)
        monitor.add_breadcrumb("Payment created", category="payment", data={"intent_id": payment_intent["id"]})

    except Exception as e:
        # If error occurs, Sentry shows all breadcrumbs leading to it
        monitor.capture_exception(e)
        raise
```

#### Pattern D: Performance tracing

```python
def get_dashboard_data(user_id: int):
    # Trace performance of expensive operation
    with monitor.trace("dashboard_data_load"):
        user_stats = get_user_statistics(user_id)

        with monitor.trace("recent_orders_query"):
            recent_orders = get_recent_orders(user_id, limit=10)

        with monitor.trace("recommendations_compute"):
            recommendations = calculate_recommendations(user_id)

    return {
        "stats": user_stats,
        "orders": recent_orders,
        "recommendations": recommendations
    }
```

---

### 4. Payment (`app.core.payment`)

**Purpose:** Process payments securely via Stripe.

**Common Patterns:**

#### Pattern A: Create payment intent

```python
from app.core import payment, monitor, get_logger

logger = get_logger(__name__)

def create_order_payment(order_id: int, amount: int):
    try:
        intent = payment.create_payment_intent(
            amount=amount,  # In cents
            currency="usd",
            metadata={
                "order_id": str(order_id),
                "user_id": str(current_user.id)
            }
        )

        logger.info("Payment intent created", extra={
            "order_id": order_id,
            "amount": amount,
            "intent_id": intent["id"]
        })

        return intent

    except PaymentError as e:
        monitor.capture_exception(e, context={"order_id": order_id})
        logger.error("Payment creation failed", extra={"error": str(e)})
        raise
```

#### Pattern B: Create customer first (for recurring payments)

```python
def setup_customer_payment(user: User):
    # Create Stripe customer
    customer = payment.create_customer(
        email=user.email,
        name=user.full_name,
        metadata={"user_id": str(user.id)}
    )

    # Save customer ID to database
    user.stripe_customer_id = customer["id"]
    db.commit()

    # Now create payment intent with customer
    intent = payment.create_payment_intent(
        amount=1000,
        customer_id=customer["id"]
    )

    return intent
```

#### Pattern C: Handle refunds

```python
def refund_order(order_id: int, reason: str = None):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order.payment_intent_id:
        raise ValueError("Order has no payment intent")

    # Full refund
    refund = payment.create_refund(
        payment_intent_id=order.payment_intent_id,
        reason=reason
    )

    # Update order status
    order.status = "refunded"
    order.refund_id = refund["id"]
    db.commit()

    logger.info("Order refunded", extra={
        "order_id": order_id,
        "amount": order.total,
        "refund_id": refund["id"]
    })

    return refund
```

#### Pattern D: Verify webhooks

```python
from fastapi import Request, HTTPException

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    # Verify signature
    if not payment.verify_webhook_signature(payload, signature):
        raise HTTPException(400, "Invalid webhook signature")

    # Process webhook
    event = json.loads(payload)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        order_id = payment_intent["metadata"]["order_id"]

        # Update order status
        order = db.query(Order).filter(Order.id == order_id).first()
        order.status = "paid"
        db.commit()

        logger.info("Payment succeeded via webhook", extra={"order_id": order_id})

    return {"status": "ok"}
```

---

## Service Activation

Services are controlled via environment variables in `.env` files:

### Development (.env.dev)
```bash
# Disable all optional services in dev
REDIS_ENABLED=false
SENTRY_ENABLED=false
STRIPE_ENABLED=false

# Logging (always enabled)
LOG_LEVEL=DEBUG
LOG_FORMAT=text  # Human-readable in dev
```

### Staging (.env.staging)
```bash
# Enable monitoring in staging
REDIS_ENABLED=true
REDIS_URL=redis://staging-redis:6379

SENTRY_ENABLED=true
SENTRY_DSN=https://...@sentry.io/staging
SENTRY_ENVIRONMENT=staging

# Stripe test mode
STRIPE_ENABLED=true
STRIPE_SECRET_KEY=sk_test_...

LOG_LEVEL=INFO
LOG_FORMAT=json  # Structured logs
```

### Production (.env.prod)
```bash
# Enable all services in production
REDIS_ENABLED=true
REDIS_URL=redis://prod-redis:6379

SENTRY_ENABLED=true
SENTRY_DSN=https://...@sentry.io/prod
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1

# Stripe LIVE mode
STRIPE_ENABLED=true
STRIPE_SECRET_KEY=sk_live_...  # REAL MONEY!

LOG_LEVEL=WARN  # Only warnings and errors
LOG_FORMAT=json
```

---

## Complete Example: E-commerce Endpoint

```python
from fastapi import APIRouter, HTTPException, Depends
from app.core import cache, get_logger, monitor, payment
from app.models import Order, User

router = APIRouter()
logger = get_logger(__name__)

@router.post("/orders/{order_id}/checkout")
async def checkout_order(order_id: int, current_user: User = Depends(get_current_user)):
    # Set user context for monitoring
    monitor.set_user(user_id=str(current_user.id), email=current_user.email)

    # Add breadcrumb
    monitor.add_breadcrumb("Checkout started", category="commerce", data={"order_id": order_id})

    try:
        # Check cache for order total (avoid recalculation)
        cache_key = f"order_total:{order_id}"
        total = cache.get(cache_key)

        if not total:
            # Calculate total (expensive operation)
            with monitor.trace("calculate_order_total"):
                order = db.query(Order).filter(Order.id == order_id).first()
                if not order:
                    raise HTTPException(404, "Order not found")

                total = sum(item.price * item.quantity for item in order.items)

                # Cache for 5 minutes
                cache.set(cache_key, total, ttl=300)

            logger.debug("Order total calculated", extra={"order_id": order_id, "total": total})
        else:
            logger.debug("Order total from cache", extra={"order_id": order_id})

        # Create payment intent
        intent = payment.create_payment_intent(
            amount=int(total * 100),  # Convert to cents
            currency="usd",
            metadata={
                "order_id": str(order_id),
                "user_id": str(current_user.id)
            }
        )

        # Log success
        logger.info("Checkout completed", extra={
            "order_id": order_id,
            "user_id": current_user.id,
            "total": total,
            "intent_id": intent["id"]
        })

        return {
            "order_id": order_id,
            "total": total,
            "client_secret": intent["client_secret"]
        }

    except PaymentError as e:
        # Capture payment errors
        monitor.capture_exception(e, context={
            "order_id": order_id,
            "user_id": current_user.id
        })
        logger.error("Payment failed", extra={"error": str(e)})
        raise HTTPException(500, "Payment processing failed")

    except Exception as e:
        # Capture all other errors
        monitor.capture_exception(e)
        logger.error("Checkout failed", extra={"error": str(e)})
        raise HTTPException(500, "Internal server error")
```

---

## Agent Instructions

**When implementing backend code:**

1. ✅ **ALWAYS import from `app.core`**
   ```python
   from app.core import cache, get_logger, monitor, payment
   ```

2. ✅ **NEVER import external packages directly**
   - ❌ `import redis`
   - ❌ `import stripe`
   - ❌ `import sentry_sdk`

3. ✅ **Initialize logger at module level**
   ```python
   logger = get_logger(__name__)
   ```

4. ✅ **Use cache for expensive operations**
   - DB queries
   - API calls
   - Computations

5. ✅ **Log with structured data (extra={})**
   ```python
   logger.info("Event", extra={"key": "value"})
   ```

6. ✅ **Capture exceptions with context**
   ```python
   monitor.capture_exception(e, context={"user_id": 123})
   ```

7. ✅ **Test code works with services disabled**
   - Code should run in dev without Redis, Sentry, Stripe
   - Use ENABLED=false environment variables

---

## Testing Patterns

### Unit Tests

Mock the core services:

```python
from unittest.mock import patch, MagicMock

def test_get_user_with_cache():
    with patch('app.core.cache.get') as mock_get:
        mock_get.return_value = {"id": 123, "name": "Test"}

        result = get_user(123)

        assert result["id"] == 123
        mock_get.assert_called_once_with("user:123")
```

### Integration Tests

Use test mode (services disabled):

```python
import os

def test_payment_creation():
    # Ensure test mode
    os.environ["STRIPE_ENABLED"] = "false"

    # Payment abstraction returns test data
    intent = payment.create_payment_intent(amount=1000)

    assert intent["test_mode"] is True
    assert intent["amount"] == 1000
```

---

## Related Documentation

- Environment Configuration: `@agent-os/standards/global/environments.md`
- Global Standards: `@agent-os/standards/global-standards.md`
- Security: `@agent-os/standards/global/security.md`
