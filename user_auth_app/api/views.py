from requests import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from core import settings
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Retrieve and update the authenticated user's profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response =  super(request, *args, **kwargs)
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            value = access,
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value = refresh,
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        
        response.data = {'message': 'Login erfolgreich'}
        return response
        
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token =  request.COOKIES.get("refresh_token")
        
        if refresh_token is None:
            return Response(
                {"detail" : "Refresh token not found!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serialize = self.get_serializer(data={"refresh" : refresh_token})
        
        try: 
            serialize.is_valid(raise_exception=True)
        except:
            return Response(
                {"detail" : "Refresh token invalid!"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        access_token = serialize.validated_data.get('access')
        
        response = Response({'message': 'access Token refreshed'})
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            value = access_token,
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        
        return response