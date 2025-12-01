from rest_framework import serializers
from api.models import Product, Sell, SellItem


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


class SellSerializer(serializers.ModelSerializer):
    sell_id = serializers.UUIDField(read_only=True)
    # Raltionship with SellItemSerialiazer for  many sellitems.
    sell_items = SellItemSerialiazer(many=True, required=False)

    def total(self, obj):
        sell_items = obj.objects.all()
        return sum(sell_item.item_subtotal for sell_item in sell_items)

    class Meta:
        model = Sell
        fields = (
            "sell_id",
            "status",
            "created_at",
            "sell_items",
        )
