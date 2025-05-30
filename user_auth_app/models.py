from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model using email as the unique identifier.
    """
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The e-mail address must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('A superuser must be a staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('A superuser must have is_superuser')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom user model that replaces the default username field with an email address.
    """
    username = None
    email = models.EmailField('E-Mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []     

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
