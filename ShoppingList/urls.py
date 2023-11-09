# shopping_list/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'shopping-list', views.ShoppingListItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:username>/', views.UserListView.as_view(), name='user-list'),
    path('<str:username>/<int:pk>', views.UserListDetailView.as_view(), name='user-list-detail'),
]