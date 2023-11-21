from django.urls import path, include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'SavedRecipes', views.SavedRecipeView, 'SavedRecipes')

urlpatterns = [
    # path('<str:username>/', views.SavedRecipeView.as_view(), name='user-list'),
    path('<str:username>/', views.SavedRecipeView.as_view(), name='saved-recipes'),
    path('<str:username>/<int:pk>/', views.UserListDetailView.as_view(), name='savedrecipe-detail'),
]
