from rest_framework import serializers
from .models import SavedRecipe
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
# class SavedRecipeSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source='user.username', read_only=True)
class SavedRecipeSerializer(serializers.ModelSerializer):
   user = serializers.CharField(source='user.username', read_only=True)
   url = serializers.CharField()  # Or use URLField if you want URL validation
   class Meta:
        model = SavedRecipe
        fields = ['id', 'url', 'user'] 