from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    This serializer validates the input data (email, password, and repeated password)
    and creates a new user with the given email and password.
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        email = self.validated_data['email']

        if password != repeated_password:
            raise serializers.ValidationError({'password-error': 'Enter the password correctly!'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email-error': 'This E-Mail address already exists.'})

        user = User(email=email)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login requests.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError('Must include "email" and "password".', code='authorization')

        attrs['user'] = user
        return attrs

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Returns id, email, date_joined and last_login.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']
