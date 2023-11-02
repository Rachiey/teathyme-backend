from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    user_preferences = models.TextField(null=True, blank=True)
      # Add related_name to prevent clashes with the default User model
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_set'
    )


    def __str__(self):
        return self.username
