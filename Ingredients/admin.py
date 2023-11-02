from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Ingredients

# Get the user model
User = get_user_model()

class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('text', 'quantity', 'expiry_date')


admin.site.register(Ingredients, IngredientsAdmin)
