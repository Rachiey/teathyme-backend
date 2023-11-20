from django.urls import path
from . import views

urlpatterns = [
    path('', views.SavedRecipeView.as_view(), name='saved_recipes'),
    path('<str:username>/', views.UserListView.as_view(), name='user-list'),
    path('<str:username>/<int:pk>/', views.SavedRecipeView.as_view(), name='user-list-detail'),
]
