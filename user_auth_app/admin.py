from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user_auth_app.models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin class for CustomUser model that includes 'id', 'email',
    and shows important dates such as last_login and date_joined.
    """
    model = CustomUser
    list_display = ('id', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('id',)
    search_fields = ('email',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),  # <-- 'id' als readonly Field
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

