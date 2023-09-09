from rest_framework import serializers
from .models import *


class BuyerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerDetails
        fields = "__all__"


class BuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = ['id', 'first_name', 'last_name',
                  'email', 'is_active', 'title', 'role']
