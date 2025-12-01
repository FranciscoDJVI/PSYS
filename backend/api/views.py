from rest_framework import viewsets
from api.models import Product, SellItem
from api.serializers import ProductSerializer, SellItemSerialiazer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SellItemViewSet(viewsets.ModelViewSet):
    queryset = SellItem.objects.all()
    serializer_class = SellItemSerialiazer
