import requests
from flask import current_app
import uuid

def create_order(amount, currency="USD"):
    # Mocking PayPal API response for hackathon demo
    return {
        "id": f"PAYPAL_ORDER_{uuid.uuid4().hex[:8].upper()}",
        "status": "CREATED"
    }

def capture_order(order_id):
    # Mocking capture response
    return {
        "id": f"PAYPAL_CAPTURE_{uuid.uuid4().hex[:8].upper()}",
        "status": "COMPLETED"
    }
