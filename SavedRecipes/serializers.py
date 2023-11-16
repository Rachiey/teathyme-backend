from rest_framework import serializers
from .models import SavedRecipe

class SavedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipe
        fields = ['id', 'url', 'user']  # Adjust fields as needed