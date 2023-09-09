from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = super(StandardResultsSetPagination,
                         self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response


class BuyerView(generics.ListAPIView):
    serializer_class = BuyerSerializer
    queryset = Buyer.objects.all()
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class BuyerUpdateView(generics.GenericAPIView):
    serializer_class = BuyerSerializer
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Buyer.objects.get(pk=pk)
        except Buyer.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        buyer_key = self.get_object(self.kwargs.get('pk_buyer', ''))
        serializer = self.serializer_class(buyer_key, data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_201_CREATED
            serializer.save()
            return Response(serializer.data, status=status_code)

    def get(self, request, *args, **kwargs):
        buyer = self.get_object(self.kwargs.get('pk_buyer', ''))
        serializer = BuyerSerializer(buyer)
        return Response(serializer.data)


class BuyerDetailsView(generics.GenericAPIView):
    serializer_class = BuyerDetailsSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            status_code = status.HTTP_201_CREATED
            serializer.save()
            return Response(serializer.data, status=status_code)

# update  Rep Details.


class BuyerDetailsUpdateView(generics.GenericAPIView):
    serializer_class = BuyerDetailsSerializer
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return BuyerDetails.objects.get(user_id=pk)
        except BuyerDetails.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        buyer_key = self.get_object(self.kwargs.get('pk_buyer', ''))
        serializer = self.serializer_class(buyer_key, data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_201_CREATED
            serializer.save()
            return Response(serializer.data, status=status_code)

    def get(self, request, *args, **kwargs):
        buyer = self.get_object(self.kwargs.get('pk_buyer', ''))
        serializer = BuyerDetailsSerializer(buyer)
        return Response(serializer.data)
