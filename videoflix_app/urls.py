from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.registration.views import VerifyEmailView
from user_auth_app.api.views import get_csrf_token
from allauth.account.views import ConfirmEmailView
from user_auth_app.views import redirect_to_admin #redirect_to_schema
#from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # path('', redirect_to_schema, name='root'), only for production
    
    path('', redirect_to_admin, name='root'),
    path('admin/', admin.site.urls),
    #path('api/', redirect_to_schema, name='root'), only for production
    path('api/', redirect_to_admin, name='root'),
    #path('api/', include('user_auth_app.api.urls')), für mögliches Profile Edite
    path('api/media/', include('media_content_app.api.urls')),
    # path('api/user/', include('user_auth_app.api.urls')), für mögliches Profile Edite
    
    # Neuer CSRF-Endpoint
    path('api/auth/csrf/', get_csrf_token, name='get_csrf_token'),
    
    #GET‑Bestätigung über Link in der E‑Mail
    re_path(
        r'^api/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        ConfirmEmailView.as_view(template_name='account/email_confirm.html'),
        name='account_confirm_email'
    ),
    # Optional: Alias für dj-rest-auth VerifyEmailView
    # path(
    #     'api/auth/account-confirm-email/',
    #     VerifyEmailView.as_view(),
    #     name='account_email_verification_sent'
    # ),
    
    # 1) dj-rest-auth Login/Logout/Password
    path('api/auth/', include('dj_rest_auth.urls')),

    # 2) dj-rest-auth Registration + E‑Mail‑Bestätigung (POST)
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    ## API Schema & Doku
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
