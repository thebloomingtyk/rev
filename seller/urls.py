from django.urls import path, include
from rest_framework import routers
from .views import SellerDetailsViewSet, SellerViewSet

router = routers.DefaultRouter()
router.register(r'sellers', SellerViewSet)
router.register(r'seller-details', SellerDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
