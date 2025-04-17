from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer

User = get_user_model()

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for the CustomUser model.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
