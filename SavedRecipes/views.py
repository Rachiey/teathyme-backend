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
        # Get saved recipes for the current user (you'll need to implement the logic)
        saved_recipes = SavedRecipe.objects.filter(user=request.user)
        serializer = SavedRecipeSerializer(saved_recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Save a recipe for the current user
        serializer = SavedRecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class UserListView(generics.ListCreateAPIView):
    serializer_class = SavedRecipeSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return SavedRecipe.objects.filter(user__username=username)

    # def perform_create(self, serializer):
    #     username = self.kwargs['username']
    #     user = User.objects.get(username=username)
    #     serializer.save(user=user)

    @permission_classes([IsAuthenticated])    
    def delete(self, req, id):
        savedrecipe = self.get_savedrecipe(id)
        self.check_object_permissions(req, savedrecipe)
        savedrecipe.delete()
        return Response(status=204)
    