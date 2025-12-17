"""
Views for the e-commerce API.
"""

import logging
from rest_framework import filters, generics, viewsets, serializers
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F
from api.models import Product, SellItem, Sell, User
from api.serializers import (
    CustomObtainPairSerializer,
    UserSerializer,
    ProductSerializer,
    SellItemSerializer,
    SellSerializer,
)
from api.filters import (
    ProductFilter,
    InStockFilter,
    SellFilter,
)
from .exceptions import ProductNotFoundError

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model with filters and search.
    """

    queryset = Product.objects.order_by("pk")
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
    pagination_class.page_size = 5
    pagination_class.page_query_param = "pagenum"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 10

    def get_permissions(self):
        """
        Set permissions based on request method.
        """
        self.permission_classes = [AllowAny]
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a product with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Product.DoesNotExist:
            logger.warning(f"Product not found: {kwargs.get('pk')}")
            return Response(
                {"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving product: {e}")
            return Response(
                {"error": "Error interno."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# viewsets for obtain all products for request of client.
# without pagination
class ProductAllAPIView(ProductViewSet):
    """
    ViewSet for all products without pagination.
    """

    pagination_class = None


class SellItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SellItem model.
    """

    queryset = SellItem.objects.all()
    serializer_class = SellItemSerializer

    def get_permissions(self):
        """
        Set permissions based on request method.
        """
        self.permission_classes = [AllowAny]
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        return super().get_permissions()


class SellViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Sell model with custom permissions and total sales.
    """

    queryset = Sell.objects.all()
    serializer_class = SellSerializer

    filterset_class = SellFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """
        Set permissions based on request method.
        """
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Perform create with user assignment.
        """
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            logger.error(f"Error creating sell: {e}")
            raise

    def create(self, request, *args, **kwargs):
        """
        Create sell with error handling.
        """
        try:
            return super().create(request, *args, **kwargs)

        except Exception as e:
            logger.error(f"Unexpected error in sell creation: {e}")
            return Response(
                {"error": "Error interno al crear venta."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List sells with total sales amount.
        """
        try:
            response = super().list(request, *args, **kwargs)
            total_sales = (
                SellItem.objects.aggregate(
                    total=Sum(F("product__price") * F("quantity"))
                )["total"]
                or 0
            )
            response.data["total_sales"] = total_sales
            return response
        except Exception as e:
            logger.error(f"Error listing sells: {e}")
            return Response(
                {"error": "Error interno al listar ventas."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer
