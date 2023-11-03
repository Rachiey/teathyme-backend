from rest_framework import serializers
from .models import Ingredients
from django.contrib.auth.models import User

class IngredientsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)  # Accept the username as input

    class Meta:
        model = Ingredients
        fields = ('id', 'text', 'quantity', 'expiry_date', 'user')

    def create(self, validated_data):
        username = validated_data.pop('user')
        user = User.objects.get(username=username)
        ingredient = Ingredients.objects.create(user=user, **validated_data)
        return ingredient