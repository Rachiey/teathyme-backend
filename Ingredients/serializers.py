from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Ingredients
from rest_framework.exceptions import AuthenticationFailed


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'text', 'quantity', 'expiry_date', 'user')