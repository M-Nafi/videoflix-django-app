from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from user_auth_app.api.views import get_csrf_token
from user_auth_app.views import redirect_to_admin #redirect_to_schema
#from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # path('', redirect_to_schema, name='root'), only for production
    
    path('', redirect_to_admin, name='root'),
    path('admin/', admin.site.urls),
    #path('api/', redirect_to_schema, name='root'), only for production
    path('api/', redirect_to_admin, name='root'),
    #path('api/', include('user_auth_app.api.urls')), für mögliches Profile Edite
    
     # Djoser-Basis-Endpunkte
    path('api/auth/', include('djoser.urls')),           # Registration, Activation, Reset :contentReference[oaicite:8]{index=8}
    path('api/auth/', include('djoser.urls.jwt')),       # JWT Obtain/Refresh/Verify :contentReference[oaicite:9]{index=9}

    
    ## API Schema & Doku
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
