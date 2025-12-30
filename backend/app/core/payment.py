"""
Payment processing abstraction.

Provides payment functionality with optional Stripe backend.
Works in test mode without real Stripe account.

Usage:
    from app.core.payment import payment

    # Create payment intent
    intent = payment.create_payment_intent(amount=1000, currency="usd")

    # Create customer
    customer = payment.create_customer(email="user@example.com")

    # Refund payment
    refund = payment.create_refund(payment_intent_id="pi_xxx", amount=500)

Environment Variables:
    STRIPE_ENABLED: Enable/disable Stripe (default: false)
    STRIPE_SECRET_KEY: Stripe API secret key (required if STRIPE_ENABLED=true)
    STRIPE_PUBLISHABLE_KEY: Stripe publishable key (for frontend)
    STRIPE_WEBHOOK_SECRET: Webhook signing secret (optional)
"""

import os
from typing import Any, Dict, Optional
from enum import Enum


class PaymentStatus(str, Enum):
    """Payment status enum."""
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"


class PaymentService:
    """
    Payment service with optional Stripe backend.

    Falls back to test mode if Stripe is disabled.
    """

    def __init__(self):
        self.enabled = os.getenv("STRIPE_ENABLED", "false").lower() == "true"
        self._stripe = None
        self._test_mode = not self.enabled

        if self.enabled:
            try:
                import stripe

                secret_key = os.getenv("STRIPE_SECRET_KEY")
                if not secret_key:
                    raise ValueError("STRIPE_SECRET_KEY not set but STRIPE_ENABLED=true")

                stripe.api_key = secret_key
                self._stripe = stripe

                # Determine if using test or live keys
                if secret_key.startswith("sk_test_"):
                    print("✅ Stripe enabled (TEST mode)")
                elif secret_key.startswith("sk_live_"):
                    print("✅ Stripe enabled (LIVE mode - real money!)")
                else:
                    print("⚠️ Stripe key format unrecognized")

            except Exception as e:
                print(f"⚠️ Stripe initialization failed: {e}. Using test mode.")
                self.enabled = False
                self._stripe = None
                self._test_mode = True
        else:
            print("ℹ️ Stripe payments disabled. Using test mode.")

    def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        metadata: Optional[Dict[str, Any]] = None,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a payment intent.

        Args:
            amount: Amount in smallest currency unit (cents for USD)
            currency: Currency code (usd, eur, etc.)
            metadata: Additional metadata (order_id, user_id, etc.)
            customer_id: Stripe customer ID (optional)

        Returns:
            Payment intent object

        Example:
            intent = payment.create_payment_intent(
                amount=1000,  # $10.00
                currency="usd",
                metadata={"order_id": "123", "user_id": "456"}
            )
        """
        if self._test_mode:
            # Test mode - simulate success
            return {
                "id": f"pi_test_{os.urandom(12).hex()}",
                "amount": amount,
                "currency": currency,
                "status": "succeeded",
                "client_secret": "test_secret",
                "metadata": metadata or {},
                "test_mode": True
            }

        try:
            params = {
                "amount": amount,
                "currency": currency,
                "metadata": metadata or {},
            }

            if customer_id:
                params["customer"] = customer_id

            intent = self._stripe.PaymentIntent.create(**params)
            return {
                "id": intent.id,
                "amount": intent.amount,
                "currency": intent.currency,
                "status": intent.status,
                "client_secret": intent.client_secret,
                "metadata": intent.metadata,
                "test_mode": False
            }

        except Exception as e:
            raise PaymentError(f"Failed to create payment intent: {str(e)}")

    def retrieve_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Retrieve a payment intent by ID.

        Args:
            payment_intent_id: Payment intent ID

        Returns:
            Payment intent object
        """
        if self._test_mode:
            return {
                "id": payment_intent_id,
                "status": "succeeded",
                "test_mode": True
            }

        try:
            intent = self._stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "id": intent.id,
                "amount": intent.amount,
                "currency": intent.currency,
                "status": intent.status,
                "metadata": intent.metadata,
                "test_mode": False
            }
        except Exception as e:
            raise PaymentError(f"Failed to retrieve payment intent: {str(e)}")

    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe customer.

        Args:
            email: Customer email
            name: Customer name (optional)
            metadata: Additional metadata

        Returns:
            Customer object

        Example:
            customer = payment.create_customer(
                email="user@example.com",
                name="John Doe",
                metadata={"user_id": "123"}
            )
        """
        if self._test_mode:
            return {
                "id": f"cus_test_{os.urandom(12).hex()}",
                "email": email,
                "name": name,
                "metadata": metadata or {},
                "test_mode": True
            }

        try:
            params = {
                "email": email,
                "metadata": metadata or {},
            }

            if name:
                params["name"] = name

            customer = self._stripe.Customer.create(**params)
            return {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "metadata": customer.metadata,
                "test_mode": False
            }

        except Exception as e:
            raise PaymentError(f"Failed to create customer: {str(e)}")

    def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a refund for a payment.

        Args:
            payment_intent_id: Payment intent ID to refund
            amount: Amount to refund (None for full refund)
            reason: Refund reason (optional)

        Returns:
            Refund object

        Example:
            # Full refund
            refund = payment.create_refund(payment_intent_id="pi_xxx")

            # Partial refund
            refund = payment.create_refund(
                payment_intent_id="pi_xxx",
                amount=500,  # Refund $5.00
                reason="Customer request"
            )
        """
        if self._test_mode:
            return {
                "id": f"re_test_{os.urandom(12).hex()}",
                "payment_intent": payment_intent_id,
                "amount": amount,
                "status": "succeeded",
                "reason": reason,
                "test_mode": True
            }

        try:
            params = {
                "payment_intent": payment_intent_id,
            }

            if amount:
                params["amount"] = amount

            if reason:
                params["reason"] = reason

            refund = self._stripe.Refund.create(**params)
            return {
                "id": refund.id,
                "payment_intent": refund.payment_intent,
                "amount": refund.amount,
                "status": refund.status,
                "reason": refund.reason,
                "test_mode": False
            }

        except Exception as e:
            raise PaymentError(f"Failed to create refund: {str(e)}")

    def verify_webhook_signature(self, payload: bytes, signature: str, secret: Optional[str] = None) -> bool:
        """
        Verify Stripe webhook signature.

        Args:
            payload: Raw webhook payload (bytes)
            signature: Stripe-Signature header value
            secret: Webhook secret (uses STRIPE_WEBHOOK_SECRET env var if not provided)

        Returns:
            True if signature is valid, False otherwise

        Example:
            # In FastAPI endpoint
            @app.post("/webhooks/stripe")
            async def stripe_webhook(request: Request):
                payload = await request.body()
                signature = request.headers.get("stripe-signature")

                if not payment.verify_webhook_signature(payload, signature):
                    raise HTTPException(400, "Invalid signature")

                # Process webhook...
        """
        if self._test_mode:
            # In test mode, always return True
            return True

        webhook_secret = secret or os.getenv("STRIPE_WEBHOOK_SECRET")
        if not webhook_secret:
            print("⚠️ STRIPE_WEBHOOK_SECRET not set, cannot verify webhook")
            return False

        try:
            self._stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            return True
        except Exception as e:
            print(f"⚠️ Webhook signature verification failed: {e}")
            return False


class PaymentError(Exception):
    """Payment processing error."""
    pass


# Global payment instance
payment = PaymentService()
