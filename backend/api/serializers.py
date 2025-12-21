"""
Serializers for the e-commerce API.
"""

from api.constants import INSUFFICIENT_STOCK_MSG, INVALID_PAYMENT_TYPE_MSG
from api.models import User, Product, Sell, SellItem
from api.utils import validate_stock_availability
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Sum, F
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .utils import validate_stock_availability, validate_payment_type
from .exceptions import InsufficientStockError, InvalidPaymentTypeError

import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_staff",
            "password",
            "is_authenticated",
            "roles",
            "groups",
        )
        extra_kwargs = {"password": {"write_only" " True"}}

    def get_roles(self, obj):
        return [group.name for group in obj.groups.all()]

    def create(self, validated_data):
        groups_data = validated_data.pop("groups", [])

        user = User.objects.create_user(**validated_data)

        if groups_data:
            user.groups.set(groups_data)

        return user


class ProductSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        name = data.get("name")
        brand = data.get("brand")
        model = data.get("model")
        queryset = Product.objects.filter(name=name, brand=brand, model=model)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                "A product with the same name, brand, and model already exists."
            )
        return data


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
    sell_id = serializers.UUIDField(read_only=True)
    sells = SellItemSerializer(many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    user = serializers.CharField(source="user.username", read_only=True)

    def _validate_sell_data(self, sells_data, payment_type):
        validate_payment_type(payment_type)
        for sell_item_data in sells_data:
            product = sell_item_data["product"]
            quantity = sell_item_data["quantity"]
            validate_stock_availability(product, quantity)

    def _create_sell_and_items(self, data, sells_data):
        """Crea Sell y SellItems."""
        sell = Sell.objects.create(**data)
        for sell_item_data in sells_data:
            SellItem.objects.create(sell=sell, **sell_item_data)
        return sell

    def _update_stock(self, sells_data):
        """
        Docstring for _update_stock

        :param self: Description
        :param sells_data: Description
        """
        """Decrease stock of products using model's bulk method."""

        Product.bulk_decrease_stock(sells_data)

    @transaction.atomic
    def create(self, data):
        """
        Create a sale with validations and transaction.
        Args:
            data (dict): Sale data including items.
        Returns:
            Sell: Created Sell instance.
        Raises:
            serializers.ValidationError: If validation fails.
        """
        try:
            sells_data = data.pop("sells")
            payment_type = data.get("type_pay")

            self._validate_sell_data(sells_data, payment_type)

            sell = self._create_sell_and_items(data, sells_data)
            self._update_stock(sells_data)

            logger.info(f"Sell created successfully: {sell.sell_id}")
            return sell
        except (InsufficientStockError, InvalidPaymentTypeError) as e:
            logger.error(f"Error creating sell: {e}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error creating sell: {e}")
            sells_data = data.pop("sells")
            raise serializers.ValidationError(
                INSUFFICIENT_STOCK_MSG.format(
                    Product_name=sells_data[0]["product"].name,
                    available=sells_data[0]["product"].stock,
                    requested=sells_data[0]["quantity"],
                )
            )

    def total(self, obj) -> float:
        """Calculate total price for the sell.

        Args:
            obj: Sell instance.

        Returns:
            float: Total price."""
        sell_items = (
            obj.sells.aggregate(total=Sum(F("quantity") * F("product__price")))["total"]
            or 0.0
        )
        return sell_items

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

        data["user_data"] = {"username": self.user.username, "email": self.user.email}

        data["roles"] = [group.name for group in self.user.groups.all()]

        return data
