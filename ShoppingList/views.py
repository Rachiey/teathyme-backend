from rest_framework import viewsets
from .models import ShoppingListItem
from .serializers import ShoppingListItemSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status

class ShoppingListItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemSerializer



class UserListView(generics.ListCreateAPIView):
    serializer_class = ShoppingListItemSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return ShoppingListItem.objects.filter(user__username=username)

    def perform_create(self, serializer):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        serializer.save(user=user)

    @permission_classes([IsAuthenticated])    
    def delete(self, req, id):
        shoppinglist = self.get_shoppinglist(id)
        self.check_object_permissions(req, shoppinglist)
        shoppinglist.delete()
        return Response(status=204)
    

class UserListDetailView(APIView):
    def get(self, request, username, pk):
        # Handle GET request, retrieve the ingredient
        shoppinglist = get_object_or_404(ShoppingListItem, pk=pk)
        self.check_object_permissions(request, shoppinglist)
        serializer = ShoppingListItemSerializer(shoppinglist)
        return Response(serializer.data)

    def delete(self, request, username, pk):
        # Handle DELETE request, delete the ingredient
        shoppinglist = get_object_or_404(ShoppingListItem, pk=pk)
        self.check_object_permissions(request, shoppinglist)
        shoppinglist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # @cross_origin(allow_headers=['Content-Type'])
    def put(self, request, username, pk):
        try:
            shoppinglist = ShoppingListItem.objects.get(pk=pk)
        except ShoppingListItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ShoppingListItemSerializer(shoppinglist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data.id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)