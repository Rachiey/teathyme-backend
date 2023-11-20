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

# class SavedRecipesView(APIView):
#     def get(self, request):
#         saved_recipes = SavedRecipe.objects.filter(user=request.user)
#         serializer = SavedRecipeSerializer(saved_recipes, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = SavedRecipeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavedRecipeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavedRecipeSerializer
    permission_classes = [IsAuthenticated]
  
  

    def get_queryset(self):
        username = self.kwargs['username']
        return SavedRecipe.objects.filter(user__username=username)

    def get_object(self):
        username = self.kwargs['username']
        pk = self.kwargs['pk']
        return get_object_or_404(SavedRecipe, user__username=username, pk=pk)

    def get(self, request, username, pk):
        
        saved_recipe = self.get_object()
        self.check_object_permissions(request, saved_recipe)
        serializer = SavedRecipeSerializer(saved_recipe)
        return Response(serializer.data)

    def put(self, request, username, pk):
        saved_recipe = self.get_object()
        self.check_object_permissions(request, saved_recipe)
        serializer = SavedRecipeSerializer(saved_recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, pk):
        saved_recipe = self.get_object()
        self.check_object_permissions(request, saved_recipe)
        saved_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
from rest_framework.exceptions import NotFound

class UserListView(generics.RetrieveDestroyAPIView):
    serializer_class = SavedRecipeSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return SavedRecipe.objects.filter(user__username=username)

    @permission_classes([IsAuthenticated])    
    def delete(self, request, id):
        saved_recipe = self.get_object(id)
        self.check_object_permissions(request, saved_recipe)
        saved_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        try:
            # Assuming 'id' is retrieved from the URL kwargs
            id = self.kwargs['id']
            return SavedRecipe.objects.get(id=id)
        except SavedRecipe.DoesNotExist:
            raise NotFound()
        
    def perform_create(self, serializer):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        serializer.save(user=user)

# class SavedRecipeDetailView(APIView):
#     def get_user(self, username):
#         return get_object_or_404(User, username=username)

#     def get_saved_recipe(self, user, pk):
#         return get_object_or_404(SavedRecipe, user=user, pk=pk)

#     def get(self, request, username, pk):
#         user = self.get_user(username)
#         savedrecipe = self.get_saved_recipe(user, pk)
#         self.check_object_permissions(request, savedrecipe)
#         serializer = SavedRecipeSerializer(savedrecipe)
#         return Response(serializer.data)

#     def delete(self, request, username, pk):
#         user = self.get_user(username)
#         savedrecipe = self.get_saved_recipe(user, pk)
#         self.check_object_permissions(request, savedrecipe)
#         savedrecipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def put(self, request, username, pk):
#         user = self.get_user(username)
#         shoppinglist = self.get_saved_recipe(user, pk)

#         serializer = SavedRecipeSerializer(shoppinglist, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # Return a response with the id of the updated item
#             return Response({'id': serializer.instance.id})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)