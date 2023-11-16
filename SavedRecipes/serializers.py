from rest_framework import serializers
from .models import SavedRecipe

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class SavedRecipeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = SavedRecipe
        fields = ['id', 'url', 'user']  # Adjust fields as needed