from rest_framework import serializers
from api.models import Product, SellItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "brand", "model", "sizes", "description", "price", "stock")


class SellItemSerialiazer(serializers.ModelSerializer):
    prodduct_name = serializers.CharField(max_length=200)
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price"
    )

    class Meta:
        model = SellItem
        fields = (
            "prodduct_name",
            "product_price",
            "quantity",
            "sell_subtotal",
        )
