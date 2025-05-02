from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductView, FavoriteViewSet, UserViewSet, CategoryViewSet, ProductFilter, BasketViewSet, LoginViewSet, MyTokenObtainPairView, UserDetailsView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r"products", ProductView, basename='products')
router.register(r"filter", ProductFilter, basename='products_filter')
router.register(r"favorite", FavoriteViewSet, basename='favorites')
router.register(r"users", UserViewSet, basename='users')
router.register(r"category", CategoryViewSet, basename='categorys')
router.register(r"basket", BasketViewSet, basename="Basket")

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version="v1",
        description="API documentation for the e-commerce store",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('me/', UserDetailsView.as_view(), name='user-details'),
    # path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
    # path('favorites/<int:product_id>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)