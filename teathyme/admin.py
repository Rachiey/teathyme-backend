from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import NewUserForm, ChangeUserForm
from .models import Ingredients, Token, User

# User = get_user_model()


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('text', 'quantity', 'expiry_date')


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = NewUserForm
    form = ChangeUserForm
    model = User
    list_display = ['username']

# admin.site.register(User, CustomUserAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Token)
   

# Register your models here.

admin.site.register(Ingredients, IngredientsAdmin)