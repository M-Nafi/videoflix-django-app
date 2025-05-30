from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Read JWT from HttpOnly cookie instead of Authorization header.
    """
    def get_raw_token(self, header):
        request = self.request
        token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        return token or super().get_raw_token(header)