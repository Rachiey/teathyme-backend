from django.urls import path
from . import views

urlpatterns = [
    # Other URLs...
    path('saved-recipes/', views.SavedRecipesView.as_view(), name='saved_recipes'),
    path('<str:username>/', views.UserListView.as_view(), name='user-list'),
    # Other URLs...
]