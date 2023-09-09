from rest_framework import serializers

from .models import Seller, SellerDetails


class SellerDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerDetails
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    more = SellerDetailsSerializer()

    class Meta:
        model = Seller
        fields = ['id', 'first_name', 'last_name', 'role', 'gender', 'title', 'email', 'phone', 'more']

