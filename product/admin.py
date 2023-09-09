from django.contrib import admin
from .models import Product, ProductCategory, ProductSpecification, ProductVariant

admin.site.site_header = 'Shop-Konekt Admin'
admin.site.site_title = 'Shop-Konekt Admin Portal'
admin.site.index_title = 'Welcome to Shop-Konekt Admin Portal'
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSpecification)


@admin.register(ProductVariant)
class ProductVariant(admin.ModelAdmin):
    list_display = [field.name for field in ProductVariant._meta.get_fields()]
    prepopulated_fields = {"sku": ("size", "color")}
