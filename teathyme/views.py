from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import IngredientsSerializer
from .models import Ingredients
from .serializers import LoginSerializer
from .serializers import RegisterSerializer

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import views

from .models import User
from .permissions import IsUserOrAdminOrReadOnly
from .utils import custom_create_token



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class IngredientsView(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        # Create a token for the authenticated user
        token = custom_create_token(self, Token, user)

        # You can include the token in your response
        response_data = {
            'token': token.key,
            'user_id': user.id
        }

        return Response(response_data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(req):
    data = User.objects.all()
    serialized = LoginSerializer(data, many=True)
    if req.user.is_superuser:
        return Response({"data": serialized.data})
    else:
        resp_data = serialized.data
        resp = [{"username": d["username"]} for d in resp_data]
        return Response({"data": resp})

class UserDetail(APIView):
    permission_classes = [IsUserOrAdminOrReadOnly]

    def get_user(self, username):
        return get_object_or_404(User, username__iexact=username)

    def get(self, req, username):
        user = self.get_user(username)
        self.check_object_permissions(req, user)
        serialized = LoginSerializer(user)
        return Response({"data": serialized.data})

    def put(self, req, username):
        user = self.get_user(username)
        self.check_object_permissions(req, user)
        serialized = LoginSerializer(user, data=req.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response({"data": serialized.data})
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, req, username):
        return self.put(req, username)

    def delete(self, req, username):
        user = self.get_user(username)
        self.check_object_permissions(req, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    token.delete()
    logout(request)
    return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)



# @api_view(['POST'])
# def custom_login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(request, username=username, password=password)

#     if user is not None:
#         login(request, user)
#         token, created = Token.objects.get_or_create(user=user)

#         # Check for an existing token or create a new one
#         try:
#             token = Token.objects.get(user=user)
#         except Token.DoesNotExist:
#             token = Token.objects.create(user=user)

#         return Response({'token': token.key})
#     else:
#         return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
