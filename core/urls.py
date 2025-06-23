from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from user_auth_app.views import redirect_to_admin #redirect_to_schema
import user_auth_app.api.urls as api_urls
from user_auth_app.api.views import CookieTokenObtainPairView, CookieTokenRefreshView



#import __media_content_app.api.urls as media_urls

#from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    #only for production
    #path('', redirect_to_schema, name='root'),
    #path('api/', redirect_to_schema, name='root'),
    
    #dev settings
    path('', redirect_to_admin, name='root'),
    path('api/', redirect_to_admin, name='root'),
    path('admin/', admin.site.urls),
    
    # Djoser: registration, activation, password reset, JWT-Auth
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/jwt/', include('djoser.urls.jwt')),
    
    #simple-jwt with httpOnlyCookie
    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    
    # User-Profil
    path('api/auth/', include(api_urls)),
    #path('api/media/', include(media_urls)),
    
    ## API Schema & Doku
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
