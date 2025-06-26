from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from user_auth_app.views import redirect_to_admin #redirect_to_schema
from user_auth_app.api.views import CookieTokenObtainPairView, CookieTokenRefreshView, CookieTokenVerifyView, LogoutView
import user_auth_app.api.urls as api_urls



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
    re_path(r'^api/', include('djoser.urls')),
    #re_path(r'^api/', include('djoser.urls.jwt')),
    
    #simple-jwt with httpOnlyCookie and Logout
    path('api/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/verify/', CookieTokenVerifyView.as_view(), name='token_verify'),
    path('api/logout/', LogoutView.as_view(), name='token_logout'),
    
    # User-Profil
    path('api/', include(api_urls)),
    #path('api/media/', include(media_urls)),
    
    ## API Schema & Doku
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
