from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_auth_app.views import redirect_to_admin #redirect_to_schema
import user_auth_app.api.urls as api_urls
#from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # path('', redirect_to_schema, name='root'), only for production
    
    path('', redirect_to_admin, name='root'),
    path('admin/', admin.site.urls),
    #path('api/', redirect_to_schema, name='root'), only for production
    path('api/', redirect_to_admin, name='root'),
    
    # Djoser-Basis-Endpunkte:
    # Registrierung, Aktivierung, Passwort-Reset
    path('api/auth/', include('djoser.urls')),
    
    # Djoser-JWT-Endpunkte:
    # Login (Token erstellen), Refresh, Verify
    path('api/auth/', include('djoser.urls.jwt')),
    
    # Ihre zusätzlichen API-Routen:
    # - Benutzerprofil (/users/profile/)
    # - Logout (/jwt/logout/)
    path('api/auth/', include(api_urls)),
    
    ## API Schema & Doku
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
