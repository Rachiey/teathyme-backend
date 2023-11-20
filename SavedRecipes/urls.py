from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'savedrecipes', views.SavedRecipeView, 'savedrecipes')

urlpatterns = [
    path('', include(router.urls)),
    path('<str:username>/', views.SavedRecipeView.as_view(), name='user-list'),
    path('<str:username>/<int:pk>/', views.UserListDetailView.as_view(), name='user-list-detail'),
]
