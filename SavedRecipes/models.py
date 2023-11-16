from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_url = models.URLField()

    # Other fields related to recipes

    def __str__(self):
        return self.recipe_url