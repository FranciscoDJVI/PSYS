from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, SellItemViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register(r"product", ProductViewSet)
router_sell_item = DefaultRouter()
router_sell_item.register(r"sellitems", SellItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router_sell_item.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
