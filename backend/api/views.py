from rest_framework import viewsets
from api.models import Product, SellItem, Sell
from api.serializers import ProductSerializer, SellItemSerialiazer, SellSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SellItemViewSet(viewsets.ModelViewSet):
    queryset = SellItem.objects.all()
    serializer_class = SellItemSerialiazer


class SellViewSet(viewsets.ModelViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
