import django_filters
from api.models import Product, Sell, SellItem
from rest_framework import filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "contains"],
            "price": ["exact", "lt", "gt", "range"],
            "stock": ["exact", "lt", "gt", "range"],
        }


class InStockFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        in_stock = request.query_params.get("in_stock", None)
        if in_stock == "true":
            return queryset.filter(stock__gt=0)
        return queryset


class SellFilter(django_filters.FilterSet):
    class Meta:
        model = Sell
        fields = {
            "sell_id": ["exact"],
            "user": ["exact"],
            "type_pay": ["exact", "icontains"],
            "created_at": ["exact", "range", "lt", "gt"],
        }
