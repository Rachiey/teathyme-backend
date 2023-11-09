from rest_framework import serializers
from .models import ShoppingListItem

class ShoppingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItem
        fields = '__all__'