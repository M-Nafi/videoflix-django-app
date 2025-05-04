from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import UserSerializer

User = get_user_model()

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    Sets the csrftoken cookie and returns a JSON response.
    """
    return JsonResponse({'detail': 'CSRF cookie set'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for the CustomUser model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


