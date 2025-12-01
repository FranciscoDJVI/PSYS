from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Product, SellItem, Sell, User
from api.serializers import (
    UserSerializer,
    ProductSerializer,
    SellItemSerialiazer,
    SellSerializer
)
from api.filters import (
    ProductFilter,
    InStockFilter,
    SellFilter,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_clases = ProductFilter
    filter_backends = [DjangoFilterBackend, InStockFilter]

    search_fields = ['name', 'description']

    pagination_class = PageNumberPagination
    pagination_class.page_size = 2

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

    filter_class = SellFilter
    filter_backends = [
        DjangoFilterBackend
    ]

    search_class = ['sell_id', 'status']

    pagination_class = PageNumberPagination
    pagination_class.page_size = 2

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()
