import logging
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken  # Import the ObtainAuthToken view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed


from .serializers import IngredientsSerializer
from .models import Ingredients
from Users.serializers import LoginSerializer


from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny


from .models import User
from rest_framework import generics

class UserIngredientsView(generics.ListCreateAPIView):
    serializer_class = IngredientsSerializer

    def get_queryset(self):
        # Retrieve the username from the URL
        username = self.kwargs['username']
        
        # Filter ingredients for the specified user
        return Ingredients.objects.filter(user__username=username)

    def perform_create(self, serializer):
        # Override the default create behavior to associate ingredients with the user
        username = self.kwargs['username']
        user = self.request.user  # You can use request.user to get the authenticated user
        serializer.save(user=user)
    
    # Optional: Handle other HTTP methods like PUT, PATCH, DELETE
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


logger = logging.getLogger('my_logger') 

class IngredientsView(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

    # Remove the existing create and update actions, we'll override the default methods

    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        # Get the serializer with user data and create the ingredient
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Associate the ingredient with the currently logged-in user
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @permission_classes([IsAuthenticated])
    def update(self, request, *args, **kwargs):
        # Use the provided 'pk' in the URL to retrieve the instance
        instance = self.get_object()
        # Check if the user is the owner of the ingredient
        if request.user == instance.user:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            # If the user is not the owner, return a 403 Forbidden response
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
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
