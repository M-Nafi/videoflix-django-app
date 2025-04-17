from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom Admin for the CustomUser model (AUTH_USER_MODEL),
    shows e-mail instead of user name and important data.
    """
    model = User

    list_display = ('id', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    search_fields = ('email',)
    ordering = ('id',)

    readonly_fields = ('id', 'date_joined', 'last_login')

    fieldsets = (
        (None, {
            'fields': ('id', 'email', 'password'),
            'description': _('Verwende das E-Mail-Feld als Login-Identifier.')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
admin.site.register(User, CustomUserAdmin)

