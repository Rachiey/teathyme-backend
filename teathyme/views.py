import logging
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken  # Import the ObtainAuthToken view
from rest_framework import permissions
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed


from .serializers import IngredientsSerializer
from .models import Ingredients
from .serializers import LoginSerializer
from .serializers import RegisterSerializer

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout

from .models import User
from .permissions import IsUserOrAdminOrReadOnly


logger = logging.getLogger('my_logger') 

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class IngredientsView(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

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
    # Delete the default token when logging out
    request.auth.delete()
    logout(request)
    return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class LoginView(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # Log the request data
        logger.info(f"Request data: {request.data}")

        try:
            # The ObtainAuthToken view handles token creation and login.
            # You don't need to implement this logic here anymore.
            return super(LoginView, self).post(request, format)
        except AuthenticationFailed as e:
            logger.error(f"Authentication failed: {e}")
            return Response({'detail': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)