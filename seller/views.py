from rest_framework import viewsets

from .models import Seller, SellerDetails
from .serializers import SellerSerializer, SellerDetailsSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerDetailsViewSet(viewsets.ModelViewSet):
    queryset = SellerDetails.objects.all()
    serializer_class = SellerDetailsSerializer



