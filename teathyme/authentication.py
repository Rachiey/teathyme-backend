from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.utils import timezone
import pytz


from .models import Token

def get_auth_token(obj):
    token, created = Token.objects.get_or_create(user=obj)
    if created:
        # If the token was just created, set the `created` attribute
        token.created = timezone.now()
        token.save()
    return token.key

class ExpiringTokenAuthentication(TokenAuthentication):

    model = Token

    def authenticate_credentials(self, token_key):
        models = self.get_model()

        try:
            token = models.objects.select_related("user").get(key=token_key)
        except models.DoesNotExist:
            raise AuthenticationFailed(
                {"error": "Invalid or Inactive Token", "is_authenticated": False}
            )

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": "Invalid user", "is_authenticated": False}
            )

        utc_now = timezone.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - settings.TOKEN_TTL:
            raise AuthenticationFailed(
                {"error": "Token has expired", "is_authenticated": False}
            )
        return token.user, token
