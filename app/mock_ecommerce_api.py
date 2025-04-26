# app/mock_ecommerce_api.py
from typing import Dict, Optional

MOCK_ORDERS = {
    "12345": {"status": "Shipped", "tracking": "UPS12345678"},
    "54321": {"status": "Processing", "tracking": None},
    "98765": {"status": "Delivered", "tracking": "FEDEX987654"},
}

def get_order_info(order_id: str) -> Dict[str, Optional[str]]:
    """Fetches mock order information."""
    # Basic validation to ensure order_id is digits
    if not order_id or not order_id.isdigit():
         return {"status": "Invalid Order ID format. Please provide numbers only.", "tracking": None}
    return MOCK_ORDERS.get(order_id, {"status": "Order Not Found", "tracking": None})