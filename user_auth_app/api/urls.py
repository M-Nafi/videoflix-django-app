
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, LogoutView

router = DefaultRouter()
# URL /api/auth/users/me/ für GET, PUT/PATCH, DELETE
router.register(r'users/profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    # Router-URLs: users/profile/
    path('', include(router.urls)),
    # Optional: Logout löscht das JWT-Cookie
    path('jwt/logout/', LogoutView.as_view(), name='jwt_logout'),
]