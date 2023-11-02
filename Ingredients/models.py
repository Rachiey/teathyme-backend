from datetime import date, timedelta
from django.db import models

from Users.models import User


class Ingredients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    quantity = models.IntegerField()
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

