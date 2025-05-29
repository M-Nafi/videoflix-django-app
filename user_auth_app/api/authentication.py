from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Reads JWT access token not from Authorization Header but from HttpOnly-Cookie.
    """
    def get_raw_token(self, header):
        # Ignoriere Header, nutze stattdessen das Cookie
        request = self.request
        cookie_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        return cookie_token or super().get_raw_token(header)