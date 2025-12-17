from django.db import transaction
from rest_framework import serializers
from api.models import User, Product, Sell, SellItem
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "is_staff",
            "password",
            "is_authenticated",
            "roles"
        )

    def get_roles(self, obj):
        return [group.name for group in obj.groups.all()]


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
    def create(self, data):
        sells_data = data.pop("sells")

        # Validate
        for sell_item_data in sells_data:
            product = sell_item_data["product"]
            quantity = sell_item_data["quantity"]
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Stock insuficiente para {product.name}: disponible {product.stock}, solicitado {quantity}"
                )

        # Create after validation
        sell = Sell.objects.create(**data)

        # Create SellItems
        for sell_item_data in sells_data:
            SellItem.objects.create(sell=sell, **sell_item_data)

        # Decrease stock
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


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_data'] = {
            'username': self.user.username,
            'email': self.user.email
        }

        data['roles'] = [group.name for group in self.user.groups.all()]

        return data
