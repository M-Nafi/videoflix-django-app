
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    TokenVerifyView,
    LogoutView,
)

router = DefaultRouter()
router.register(r'users/me', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('jwt/create/', CookieTokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', CookieTokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
    path('jwt/logout/', LogoutView.as_view(), name='jwt_logout'),
]