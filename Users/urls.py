from django.urls import include, path
from . import views
from django.contrib.auth.views import LogoutView
from .views import *
from Users import views
from .views import ObtainAuthToken

urlpatterns = [
    path('', views.index, name="user-index"),
    path('<str:username>/', views.UserDetail.as_view(), name="individual-user"),
    path('auth/register/', include('rest_auth.registration.urls')),
    path('auth/', include('rest_auth.urls')),
    path('auth/login/', ObtainAuthToken.as_view(), name='login'),
    path('api-auth/logout/', LogoutView.as_view(), name='api_logout'),
]