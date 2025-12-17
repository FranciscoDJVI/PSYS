"""
Utility functions for common operations.
"""

from .exceptions import InsufficientStockError, InvalidPaymentTypeError
from .constants import INSUFFICIENT_STOCK_MSG, INVALID_PAYMENT_TYPE_MSG, PAYMENT_TYPES


def validate_stock_availability(product, quantity: int) -> None:
    """
    Validate if the product has enough stock for the requested quantity.

    Args:
        product: Product instance.
        quantity (int): Requested quantity.

    Raises:
        InsufficientStockError: If stock is insufficient.
    """
    if product.stock < quantity:
        raise InsufficientStockError(
            INSUFFICIENT_STOCK_MSG.format(
                product_name=product.name, available=product.stock, requested=quantity
            )
        )


def validate_payment_type(payment_type: str) -> None:
    """
    Validate if the payment type is valid.

    Args:
        payment_type (str): Payment type to validate.

    Raises:
        InvalidPaymentTypeError: If payment type is invalid.
    """
    if payment_type not in PAYMENT_TYPES:
        raise InvalidPaymentTypeError(
            INVALID_PAYMENT_TYPE_MSG.format(valid_types=", ".join(PAYMENT_TYPES))
        )
