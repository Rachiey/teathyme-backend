from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'ingredients', views.IngredientsView, 'ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('api/ingredients/<str:username>/', views.UserIngredientsView.as_view(), name='user-ingredients'),
    path('api/ingredients/<str:username>/<int:pk>/', views.IngredientDetailView.as_view(), name='delete-ingredient'),
    path('ingredients/api/ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient-detail'),

]