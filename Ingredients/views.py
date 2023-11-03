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
from django.http import JsonResponse
from rest_framework.generics import DestroyAPIView



from .serializers import IngredientsSerializer
from .models import Ingredients
from Users.serializers import LoginSerializer


from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny


from .models import User
from rest_framework import generics

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
    def delete(self, req, id):
        ingredient = self.get_ingredient(id)
        self.check_object_permissions(req, ingredient)
        ingredient.delete()
        return Response(status=204)
    

class IngredientDetailView(APIView):
    def get(self, request, username, pk):
        # Handle GET request, retrieve the ingredient
        ingredient = get_object_or_404(Ingredients, pk=pk)
        self.check_object_permissions(request, ingredient)
        serializer = IngredientsSerializer(ingredient)
        return Response(serializer.data)

    def delete(self, request, username, pk):
        # Handle DELETE request, delete the ingredient
        ingredient = get_object_or_404(Ingredients, pk=pk)
        self.check_object_permissions(request, ingredient)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


# def delete_ingredient(request, username, item_id):
#     try:
#         # First, check if the ingredient exists and belongs to the specified user
#         ingredient = get_object_or_404(Ingredients, id=item_id, user__username=username)

#         # Check if the request method is DELETE
#         if request.method == 'DELETE':
#             # Delete the ingredient
#             ingredient.delete()
#             return JsonResponse({'message': 'Ingredient deleted successfully'})
#         else:
#             # If the request method is not DELETE, return a Bad Request response
#             return JsonResponse({'message': 'Invalid request method'}, status=400)
#     except Ingredients.DoesNotExist:
#         # If the ingredient is not found, return a Not Found response
#         return JsonResponse({'message': 'Ingredient not found'}, status=404)