from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

# from django.contrib.auth import get_user_model
# User = get_user_model()

class NewUserForm(UserCreationForm):
    # email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'