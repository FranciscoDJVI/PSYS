from django.db import transaction
from rest_framework import serializers
from api.models import User, Product, Sell, SellItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "is_staff", "is_authenticated")


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


class SellItemSerialiazer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price", read_only=True
    )

    class Meta:
        model = SellItem
        fields = (
            "product",
            "product_name",
            "product_price",
            "quantity",
            "sell_subtotal",
        )


class SellSerializer(serializers.ModelSerializer):
    sell_id = serializers.UUIDField(read_only=True)
    sells = SellItemSerialiazer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    user = serializers.CharField(source="user.username", read_only=True)

    @transaction.atomic
    def create(self, validated_data):
        sells_data = validated_data.pop("sells")

        # Validar stock ANTES de crear cualquier cosa
        for sell_item_data in sells_data:
            product = sell_item_data["product"]
            quantity = sell_item_data["quantity"]
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Stock insuficiente para {product.name}: disponible {product.stock}, solicitado {quantity}"
                )

        # Crear Sell solo después de validación
        sell = Sell.objects.create(**validated_data)

        # Crear SellItems
        for sell_item_data in sells_data:
            SellItem.objects.create(sell=sell, **sell_item_data)

        # Disminuir stock al final
        for sell_item_data in sells_data:
            product = sell_item_data["product"]
            quantity = sell_item_data["quantity"]
            product.decrease_stock(quantity)

        return sell

    def total(self, obj):
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
