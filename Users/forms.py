from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'