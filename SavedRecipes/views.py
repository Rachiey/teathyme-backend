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

class SavedRecipesView(APIView):
    def get(self, request):
        saved_recipes = SavedRecipe.objects.filter(user=request.user)
        serializer = SavedRecipeSerializer(saved_recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SavedRecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
