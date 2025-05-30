from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

User = get_user_model()

class UserCreateSerializer(DjoserUserCreateSerializer):
    """
    Extend Djoser's create-serializer: require password retype.
    """
    re_password = serializers.CharField(write_only=True)

    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 're_password')
        extra_kwargs = {
            'password': {'write_only': True},
            're_password': {'write_only': True},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']