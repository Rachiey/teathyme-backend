from django.db import models
from django.contrib.auth.models import User

class ShoppingListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    # Add other fields as needed