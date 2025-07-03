from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.test import APIRequestFactory
from djoser.views import UserViewSet
from core import settings
from .serializers import UserSerializer

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
    """
    Handle user login by issuing JWT tokens in secure HTTP-only cookies.
    """
    def post(self, request, *args, **kwargs):
        try:
            
            response =  super().post(request, *args, **kwargs)
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
        
            response.data = {'message': 'Login successful'}
            return response
        except:
            return Response({'message': 'Login not successful'})
        
class CookieTokenRefreshView(TokenRefreshView):
    """
    Refresh the JWT access token using the refresh token from cookies.
    """
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
    
class CookieTokenVerifyView(TokenVerifyView):
    """
    Verify the JWT stored in HTTP-only cookies without returning token data.
    """
    def post(self, request, *args, **kwargs):
        access_token =  request.COOKIES.get("access_token")
        
        if access_token is None:
            return Response(
                {"detail" : "Access token not found!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serialize = self.get_serializer(data={"access" : access_token})
        
        try: 
            serialize.is_valid(raise_exception=True)
            return Response({'message': 'Access Token is valid'})
        except:
            return Response(
                {"detail" : "Access token invalid!"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    
class LogoutView(APIView):
    """
    Log out the user by clearing JWT cookies.
    """
    def post(self, request, format=None):
        try:
            response = Response()
            response.delete_cookie('access_token', path='/', samesite="None")
            response.delete_cookie('refresh_token', path='/', samesite="None")
            response.data = {'message': 'Logout successful'}
            return response
        except:
            return Response(
                {'detail': 'Logout fails!'},
            )

class ActivationRedirectView(APIView):
    """
    Accepts GET /activate/<uid>/<token>/, internally invokes
    the Djoser activation action (which expects POST),
    then redirects to the frontend login page.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, uid, token):
        factory = APIRequestFactory()
        data = {'uid': uid, 'token': token}
        post_req = factory.post(
            '/users/activation/', data, format='json',
            HTTP_HOST=request.get_host()
        )
        view = UserViewSet.as_view({'post': 'activation'})
        response = view(post_req)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return redirect(settings.FRONTEND_LOGIN_URL)
        return redirect(f"{settings.FRONTEND_LOGIN_URL}?activation_failed=1")

