from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from Ingredients.models import Ingredients
from Ingredients.serializers import IngredientsSerializer

from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise AuthenticationFailed("Access denied: wrong username or password")

            attrs['user'] = user
        else:
            raise serializers.ValidationError("Both 'username' and 'password' are required.")

        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',)
    
    def validate(self, data):
        password1 = data.get('password')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        return user
    

class UserSerializer(serializers.ModelSerializer):
    num_ingredients = serializers.SerializerMethodField()
    ingredient_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'num_ingredients', 'ingredient_list']

    def get_num_ingredients(self, user):
        # Count the number of ingredients for the user
        return user.ingredients.count()

    def get_ingredient_list(self, user):
        # Get a list of ingredient data for the user
        ingredients = Ingredients.objects.filter(user=user)
        return IngredientsSerializer(ingredients, many=True).data
