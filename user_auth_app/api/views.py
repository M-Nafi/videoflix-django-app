from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .serializers import UserSerializer

User = get_user_model()

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD for the logged-in user only.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Obtain JWT tokens and set them as HttpOnly cookies.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            # set access token cookie
            response.set_cookie(
                settings.SIMPLE_JWT['AUTH_COOKIE'],
                data['access'],
                max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            # set refresh token cookie
            response.set_cookie(
                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                data['refresh'],
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.data = {'detail': 'Cookies set'}
        return response

class CookieTokenRefreshView(TokenRefreshView):
    """
    Refresh access token using HttpOnly refresh-cookie.
    """
    def post(self, request, *args, **kwargs):
        # inject refresh token from cookie into request data
        request.data['refresh'] = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            # update access token cookie
            response.set_cookie(
                settings.SIMPLE_JWT['AUTH_COOKIE'],
                data['access'],
                max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.data = {'detail': 'Access cookie refreshed'}
        return response

class LogoutView(APIView):
    """
    Clear the JWT cookies to logout.
    """
    def post(self, request):
        response = Response(status=204)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        return response