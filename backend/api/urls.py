from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, ProductViewSet, SellItemViewSet, SellViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router_sell_item = DefaultRouter()
router_sell_item.register(r"sellitems", SellItemViewSet)
router_sell = DefaultRouter()
router_sell.register(r"sells", SellViewSet)
router_user = DefaultRouter()
router_user.register(r'users', UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router_sell_item.urls)),
    path("", include(router_sell.urls)),
    path("", include(router_user.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
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
