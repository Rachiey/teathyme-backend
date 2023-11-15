from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Ingredients
from .serializers import IngredientsSerializer
from Users.serializers import LoginSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from .models import User
import logging

logger = logging.getLogger('my_logger')

class UserIngredientsView(generics.ListCreateAPIView):
    serializer_class = IngredientsSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Ingredients.objects.filter(user__username=username)

    def perform_create(self, serializer):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        serializer.save(user=user)

    @permission_classes([IsAuthenticated])    
    def delete(self, request, id):
        ingredient = self.get_ingredient(id)
        self.check_object_permissions(request, ingredient)
        ingredient.delete()
        return Response(status=204)

class IngredientDetailView(APIView):
    def get(self, request, username, pk):
        ingredient = get_object_or_404(Ingredients, pk=pk)
        self.check_object_permissions(request, ingredient)
        serializer = IngredientsSerializer(ingredient)
        return Response(serializer.data)

    def delete(self, request, username, pk):
        ingredient = get_object_or_404(Ingredients, pk=pk)
        self.check_object_permissions(request, ingredient)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, username, pk):
        try:
            ingredient = Ingredients.objects.get(pk=pk)
        except Ingredients.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IngredientsSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IngredientsView(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @permission_classes([IsAuthenticated])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def index(request):
        data = User.objects.all()
        serialized = LoginSerializer(data, many=True)
        if request.user.is_superuser:
            return Response({"data": serialized.data})
        else:
            resp_data = serialized.data
            resp = [{"username": d["username"]} for d in resp_data]
            return Response({"data": resp})
