from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    # Zeige im Listen-View E-Mail, Aktiviert-Status, An‐/Abmelde-Zeit
    list_display = ('email','is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    list_filter  = ('is_active',)

    # Da wir username nicht mehr nutzen, reduzieren wir die Felder
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1','password2','is_active','is_staff','is_superuser'),
        }),
    )

    ordering = ('email',)
    search_fields = ('email',)