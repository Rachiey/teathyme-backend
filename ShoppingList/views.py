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
    def get_user(self, username):
        return get_object_or_404(User, username=username)

    def get_shopping_list_item(self, user, pk):
        return get_object_or_404(ShoppingListItem, user=user, pk=pk)

    def get(self, request, username, pk):
        user = self.get_user(username)
        shoppinglist = self.get_shopping_list_item(user, pk)
        self.check_object_permissions(request, shoppinglist)
        serializer = ShoppingListItemSerializer(shoppinglist)
        return Response(serializer.data)

    def delete(self, request, username, pk):
        user = self.get_user(username)
        shoppinglist = self.get_shopping_list_item(user, pk)
        self.check_object_permissions(request, shoppinglist)
        shoppinglist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, username, pk):
        user = self.get_user(username)
        shoppinglist = self.get_shopping_list_item(user, pk)

        serializer = ShoppingListItemSerializer(shoppinglist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return a response with the id of the updated item
            return Response({'id': serializer.instance.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)