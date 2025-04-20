from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings
from allauth.account.models import EmailAddress

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if EmailAddress.objects.filter(email__iexact=email, verified=True).exists():
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.')
                )
        return email
    
    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        return attrs
    
    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
        }
    
    def save(self, request):
        username = self.validated_data.get('email', '')
        self.validated_data['username'] = username
        return super().save(request)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']