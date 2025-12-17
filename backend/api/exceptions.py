"""
Custom exceptions for the e-commerce API.
"""


class InsufficientStockError(Exception):
    """Raised when product stock is insufficient for a sale."""

    pass


class InvalidPaymentTypeError(Exception):
    """Raised when an invalid payment type is provided."""

    pass


class ProductNotFoundError(Exception):
    """Raised when a product is not found."""

    pass


class UserNotAuthenticatedError(Exception):
    """Raised when user is not authenticated for restricted actions."""

    pass
