from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Product, SellItem, Sell, User
from api.serializers import (
    UserSerializer,
    ProductSerializer,
    SellItemSerialiazer,
    SellSerializer,
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
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer

    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilter,
    ]

    ordering_fields = ["name", "price", "stock"]

    search_fields = ["name", "description"]

    pagination_class = PageNumberPagination
    pagination_class.page_index = 2
    pagination_class.page_query_param = 'pagenum'
    # size of number pages for the client
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 5

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
    filter_backends = [DjangoFilterBackend]

    ordering_class = ["total_price"]

    search_class = ["sell_id", "status"]


    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()
