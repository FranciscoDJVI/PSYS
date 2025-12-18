"""
Utility functions for common operations.
"""

from .exceptions import (
    InsufficientStockError,
    InvalidPaymentTypeError,
)
from .constants import PAYMENT_TYPES


def validate_stock_availability(product, quantity: int) -> None:

    if product.stock < quantity:
        raise InsufficientStockError(
            product_id=product.id,
            requested_quantity=quantity,
            available_quantity=product.stock
        )


def validate_payment_type(payment_type: str) -> None:

    if payment_type not in PAYMENT_TYPES:
        raise InvalidPaymentTypeError(
            payment_type,
            validate_types=PAYMENT_TYPES
        )
