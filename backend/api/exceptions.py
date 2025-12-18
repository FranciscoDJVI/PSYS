"""
Custom exceptions for the e-commerce API.
"""
from rest_framework.exceptions import APIException, ValidationError, NotFound, AuthenticationFailed


class InsufficientStockError(ValidationError):
    """Raised when product stock is insufficient for a sale."""

    def __init__(self, product_id, requested_quantity, available_quantity):
        self.product_id = product_id
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity
        super().__init__(
            detail=f"Insuficient stock for product {product_id}: requested {requested_quantity}, available {available_quantity}.",
            code='insufficient_stock')


class InvalidPaymentTypeError(Exception):
    """Raised when an invalid payment type is provided."""

    def __init__(self, payment_type, validate_types=None):
        self.payment_type = payment_type
        self.validate_types = validate_types or [
            "Efectivo", "Tarjeta credito", "Tarjeta debito", "Transferencia"]
        super().__init__(
            f"Invalid payment type '{payment_type}'. Valid types are: {', '.join(self.validate_types)}."
        )


class ProductNotFoundError(NotFound):
    def __init__(self, product_id=None):
        self.product_id = product_id
        detail = f"Product not found" + \
            (f" with ID {product_id}." if product_id else ".")
        super().__init__(detail=detail, code="product_not_found")
