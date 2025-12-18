"""
Views for the e-commerce API.
"""


from api.exceptions import ProductNotFoundError
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
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.db.models import Sum, F
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from . import mixins
from functools import lru_cache
import logging


logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet, mixins.AdminOnlyMixin):
    """
    ViewSet for User model.
    """

    queryset = User.objects.prefetch_related("groups").select_related()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet, mixins.PermissionMixin):
    """
    ViewSet for Product model with filters and search.
    """

    queryset = Product.objects.prefetch_related().all().order_by("name")
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

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a product with error handling.
        """

        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            logger.warning(f"Product not found: {kwargs.get('pk')}")

            raise ProductNotFoundError(product_id=kwargs.get("pk"))

        except Exception as e:
            logger.error(f"Error retrieving product: {e}")

            return Response(
                {"error": "Internal error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @lru_cache(maxsize=128)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# viewsets for obtain all products for request of client.
# without pagination
class ProductAllAPIView(ProductViewSet):
    """
    ViewSet for all products without pagination.
    """

    pagination_class = None


class SellItemViewSet(viewsets.ModelViewSet, mixins.PermissionMixin):
    """
    ViewSet for SellItem model.
    """

    queryset = SellItem.objects.all()
    serializer_class = SellItemSerializer


class SellViewSet(viewsets.ModelViewSet, mixins.AuthenticatedUserMixin):
    """
    ViewSet for Sell model with custom permissions and total sales.
    """

    queryset = Sell.objects.prefetch_related("sells__product").annotate(
        total_price=Sum(F("sells__quantity") * F("sells__product__price"))
    )
    serializer_class = SellSerializer

    filterset_class = SellFilter
    filter_backends = [DjangoFilterBackend]

    search_fields = ["sell_id"]
    ordering_fields = ["created_at", "type_pay"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

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
                {"error": "Internal error to created sale."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List sells with total sales amount.
        """
        try:
            response = super().list(request, *args, **kwargs)
            # Get the filtered queryset
            queryset = self.filter_queryset(self.get_queryset())
            total_sales = (
                SellItem.objects.filter(sell__in=queryset).aggregate(
                    total=Sum(F("product__price") * F("quantity"))
                )["total"]
                or 0
            )
            response.data["total_sales"] = total_sales
            return response
        except Exception as e:
            logger.error(f"Error listing sells: {e}")
            return Response(
                {"error": "Internal error to list sales."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer
