"""
Constants used across the API.
"""

# Payment types
PAYMENT_TYPES = ["Efectivo", "Tarjeta credito",
                 "Tarjeta debito", "Transferencia"]

# Default pagination
DEFAULT_PAGE_SIZE = 5
MAX_PAGE_SIZE = 10

# Stock limits
MAX_STOCK_QUANTITY = 10000

# Error messages
INSUFFICIENT_STOCK_MSG = "Stock insuficiente para {product_name}: disponible {available}, solicitado {requested}"
INVALID_PAYMENT_TYPE_MSG = "Tipo de pago inválido. Debe ser uno de: {valid_types}"
