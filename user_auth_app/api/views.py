from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserSerializer

User = get_user_model()

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for the CustomUser model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class LogoutView(APIView):
    """
    Clears the HttpOnly JWT cookie to logout the user.
    """
    def post(self, request):
        response = Response(status=204)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        return response