from django.contrib import admin

from seller.models import Seller, SellerDetails

# Register your models here.


admin.site.register(Seller)
admin.site.register(SellerDetails)