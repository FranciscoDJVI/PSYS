"""
Constants used across the API.
"""

# Payment types
PAYMENT_TYPES = ["Efectivo", "Tarjeta credito", "Tarjeta debito", "Transferencia"]
# Request actions

# Default pagination
DEFAULT_PAGE_SIZE = 5
MAX_PAGE_SIZE = 10

# Stock limits
MAX_STOCK_QUANTITY = 10000

# Error messages
INSUFFICIENT_STOCK_MSG = "Insuficient stock for {product_name}: disponible {available}, requested {requested}"
INVALID_PAYMENT_TYPE_MSG = "Invalid type payment. Must be one of: {valid_types}"
