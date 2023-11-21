from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SavedRecipe
from .serializers import SavedRecipeSerializer
from rest_framework import viewsets
from .models import User
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound



class SavedRecipeView(APIView):
    serializer_class = SavedRecipeSerializer
    permission_classes = [IsAuthenticated]  # Use permission_classes as a class attribute

    def get_queryset(self):
        username = self.kwargs['username']
        return SavedRecipe.objects.filter(user__username=username)

    def perform_create(self, serializer):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        serializer.save(user=user)

    def delete(self, request, id):
        savedrecipe = self.saved_recipe(id)
        self.check_object_permissions(request, savedrecipe)
        savedrecipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    def get(self, request, username):
        queryset = SavedRecipe.objects.filter(user__username=username)
        serialized_data = []
        for recipe in queryset:
            serialized_data.append({
                'id': recipe.id,
                'url': recipe.url,  # Assuming 'url' is a string field in your SavedRecipe model
                'user': recipe.user.username  # Access the username from the related User model
            })
        return Response(serialized_data)
    
    def post(self, request, username):
        # Get the authenticated user
        user = request.user
        
        # Assuming you pass the 'username' in the URL to associate the SavedRecipe with the user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Assign the authenticated user to the SavedRecipe instance before saving
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListDetailView(APIView):
    def get_user(self, username):
        return get_object_or_404(User, username=username)

    def get_saved_recipe(self, user, pk):
        return get_object_or_404(SavedRecipe, user=user, pk=pk)

    def get(self, request, username, pk):
        user = self.get_user(username)
        shoppinglist = self.get_saved_recipe(user, pk)
        self.check_object_permissions(request, shoppinglist)
        serializer = SavedRecipeSerializer(shoppinglist)
        return Response(serializer.data)

    def delete(self, request, username, pk):
        user = self.get_user(username)
        savedrecipe = self.get_saved_recipe(user, pk)
        self.check_object_permissions(request, savedrecipe)
        savedrecipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, username, pk):
        user = self.get_user(username)
        savedrecipe = self.get_saved_recipe(user, pk)

        serializer = SavedRecipeSerializer(savedrecipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return a response with the id of the updated item
            return Response({'id': serializer.instance.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)