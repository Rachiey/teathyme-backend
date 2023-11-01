from datetime import date, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework.authtoken.views import ObtainAuthToken


class User(AbstractUser):
    user_preferences = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username


# class CustomObtainAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})

class Ingredients(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    
    EXPIRATION_STATUS_EXPIRED = "expired"
    EXPIRATION_STATUS_TODAY = "today"
    EXPIRATION_STATUS_TOMORROW = "tomorrow"
    EXPIRATION_STATUS_FUTURE = "future"

    EXPIRATION_STATUS_CHOICES = [
        (EXPIRATION_STATUS_EXPIRED, "Expired"),
        (EXPIRATION_STATUS_TODAY, "Today"),
        (EXPIRATION_STATUS_TOMORROW, "Tomorrow"),
        (EXPIRATION_STATUS_FUTURE, "In the future"),
    ]

    def calculate_expires_in(self):
        today = date.today()
        if self.expiry_date < today:
            return self.EXPIRATION_STATUS_EXPIRED
        elif self.expiry_date == today:
            return self.EXPIRATION_STATUS_TODAY
        elif self.expiry_date == today + timedelta(days=1):
            return self.EXPIRATION_STATUS_TOMORROW
        else:
            return self.EXPIRATION_STATUS_FUTURE

    def save(self, *args, **kwargs):
        # Calculate and set the expiresIn value before saving
        self.expiresIn = self.calculate_expires_in()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

