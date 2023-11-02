from rest_framework import serializers
from .models import Ingredients

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'text', 'quantity', 'expiry_date', 'user')  # Include the 'user' field
