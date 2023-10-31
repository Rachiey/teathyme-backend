from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Ingredients
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'text', 'quantity', 'expiry_date')



# class UserSerializer(ModelSerializer):
#     class Meta:
#       model = User
#       fields = ['username', 'password']
#       extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User(
#             # email=validated_data['email'],
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

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
                # Handle authentication error (invalid credentials)
                raise AuthenticationFailed("Access denied: wrong username or password")

            # Valid user, add it to validated_data
            attrs['user'] = user
        else:
            # Handle missing fields error
            raise serializers.ValidationError("Both 'username' and 'password' are required.")

        return attrs
    
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            # Handle duplicate username error
            raise serializers.ValidationError("This username is already in use.")

        return value

    def validate(self, data):
        password1 = data.get('password')
        password2 = data.get('password2')

        if password1 != password2:
            # Handle password mismatch error
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        return user