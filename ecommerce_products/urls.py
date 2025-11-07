from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ecommerce_products.views import ProductViewSet
from ecommerce_products.views import MerchantCreateView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('merchants/', MerchantCreateView.as_view(), name='merchant-create'),
]
