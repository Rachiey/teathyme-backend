from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import NewUserForm, ChangeUserForm
from .models import Ingredients

# Get the user model
User = get_user_model()

class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('text', 'quantity', 'expiry_date')

class CustomUserAdmin(UserAdmin):
    add_form = NewUserForm
    form = ChangeUserForm
    model = User
    list_display = ['username']

# Register your User model with the custom admin class
admin.site.register(User, CustomUserAdmin)

# Register your Ingredients model
admin.site.register(Ingredients, IngredientsAdmin)
