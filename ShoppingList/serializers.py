from rest_framework import serializers
from .models import ShoppingListItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ShoppingListItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = ShoppingListItem
        fields = ['id', 'item', 'user']