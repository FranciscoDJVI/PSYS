"""
Serializers for the e-commerce API.
"""

import logging
from django.db import transaction
from rest_framework import serializers
from api.models import User, Product, Sell, SellItem
from .utils import validate_stock_availability, validate_payment_type
from .exceptions import InsufficientStockError, InvalidPaymentTypeError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "is_staff", "password",
                  "is_authenticated", "roles")

    def get_roles(self, obj):
        return [group.name for group in obj.groups.all()]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "brand",
            "model",
            "sizes",
            "description",
            "price",
            "stock",
        )


class SellItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price", read_only=True
    )

    class Meta:
        model = SellItem
        fields = (
            "sell",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "sell_subtotal",
        )
        extra_kwargs = {"sell": {"required": False}}


class SellSerializer(serializers.ModelSerializer):
    """
    Serializer for Sell model with nested SellItems.
    """

    sell_id = serializers.UUIDField(read_only=True)
    sells = SellItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    user = serializers.CharField(source="user.username", read_only=True)

    @transaction.atomic
    def create(self, data):
        """
        Create a Sell with nested SellItems, validating stock and payment type.
        """
        try:
            sells_data = data.pop("sells")
            payment_type = data.get("type_pay")

            # Validate payment type
            validate_payment_type(payment_type)

            # Validate stock for all items
            for sell_item_data in sells_data:
                product = sell_item_data["product"]
                quantity = sell_item_data["quantity"]
                validate_stock_availability(product, quantity)

            # Create Sell
            sell = Sell.objects.create(**data)

            # Create SellItems and decrease stock
            for sell_item_data in sells_data:
                SellItem.objects.create(sell=sell, **sell_item_data)
                product = sell_item_data["product"]
                quantity = sell_item_data["quantity"]
                product.decrease_stock(quantity)

            logger.info(f"Sell created successfully: {sell.sell_id}")
            return sell
        except (InsufficientStockError, InvalidPaymentTypeError) as e:
            logger.error(f"Error creating sell: {e}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error creating sell: {e}")
            raise serializers.ValidationError(
                "Error interno al crear la venta.")

    def total(self, obj) -> float:
        """
        Calculate total price for the sell.

        Args:
            obj: Sell instance.

        Returns:
            float: Total price.
        """
        sell_items = obj.sells.all()
        return sum(sell_item.sell_subtotal for sell_item in sell_items)

    class Meta:
        model = Sell
        fields = (
            "sell_id",
            "user",
            "created_at",
            "sells",
            "total_price",
            "type_pay",
        )

    def validate_type_pay(self, value: str) -> str:
        """
        Validate payment type.

        Args:
            value (str): Payment type.

        Returns:
            str: Validated payment type.

        Raises:
            serializers.ValidationError: If invalid.
        """
        try:
            validate_payment_type(value)
            return value
        except InvalidPaymentTypeError as e:
            raise serializers.ValidationError(str(e))


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user_data"] = {
            "username": self.user.username, "email": self.user.email}

        data["roles"] = [group.name for group in self.user.groups.all()]

        return data
