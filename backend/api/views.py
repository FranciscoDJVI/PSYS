from rest_framework import viewsets
from api.models import Product, SellItem, Sell
from api.serializers import ProductSerializer, SellItemSerialiazer, SellSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()


class SellItemViewSet(viewsets.ModelViewSet):
    queryset = SellItem.objects.all()
    serializer_class = SellItemSerialiazer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()


class SellViewSet(viewsets.ModelViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()
