from django.urls import path
from . import views

urlpatterns = [
    # Other URLs...
    path('', views.SavedRecipesView.as_view(), name='saved_recipes'),
    path('<str:username>/', views.UserListView.as_view(), name='user-list'),
    path('<str:username>/<int:pk>/', views.SavedRecipeDetailView.as_view(), name='user-list-detail'),
    # Other URLs...
]