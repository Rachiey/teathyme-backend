from django.urls import include, path
from . import views
# from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import *
from teathyme import views
from .views import ObtainAuthToken
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Ingredientss', views.IngredientsView, 'Ingredients')

urlpatterns = [
    path('', views.index, name="user-index"),
    path('<str:username>/', views.UserDetail.as_view(), name="individual-user"),
    path('auth/register/', include('rest_auth.registration.urls')),
    path('auth/', include('rest_auth.urls')),
    path('teathyme/auth/login/', ObtainAuthToken.as_view(), name='login'),
    path('api-auth/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/Ingredientss/', include(router.urls)),
    path('api/Ingredientss/<str:username>/', views.UserIngredientsView.as_view(), name='user-ingredients'),
]