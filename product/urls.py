# from django.urls import path
# from .views import (
#     ProductListCreateView, ProductDetailView,
#     ProductCategoryListCreateView, ProductCategoryDetailView,
#     ProductSpecificationListCreateView, ProductSpecificationDetailView,
#     ProductVariantListCreateView, ProductVariantDetailView,
# )

# urlpatterns = [
#     path('products/', ProductListCreateView.as_view(), name='product-list-create'),
#     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

#     path('categories/', ProductCategoryListCreateView.as_view(), name='category-list-create'),
#     path('categories/<int:pk>/', ProductCategoryDetailView.as_view(), name='category-detail'),

#     path('specifications/', ProductSpecificationListCreateView.as_view(), name='specification-list-create'),
#     path('specifications/<int:pk>/', ProductSpecificationDetailView.as_view(), name='specification-detail'),

#     path('variants/', ProductVariantListCreateView.as_view(), name='variant-list-create'),
#     path('variants/<int:pk>/', ProductVariantDetailView.as_view(), name='variant-detail'),
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductViewSet, ProductSpecificationViewSet, ProductVariantViewSet 

router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-specifications', ProductSpecificationViewSet)
router.register(r'product-variants', ProductVariantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
