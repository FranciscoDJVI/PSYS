from rest_framework import serializers
from api.models import User, Product, Sell, SellItem
from datetime import datetime


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

    def create(self, validated_data):
        sells_data = validated_data.pop("sells")
        sell = Sell.objects.create(**validated_data)
        for sell_item_data in sells_data:
            SellItem.objects.create(sell=sell, **sell_item_data)
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
