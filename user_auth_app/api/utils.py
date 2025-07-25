from django.conf import settings

def set_jwt_cookies(response, access_token, refresh_token=None):
    """Set JWT cookies based on SIMPLE_JWT settings."""
    
    jwt_settings = settings.SIMPLE_JWT
    
    response.set_cookie(
        key=jwt_settings.get('AUTH_COOKIE', 'access_token'),
        value=str(access_token),
        httponly=jwt_settings.get('AUTH_COOKIE_HTTP_ONLY', True),
        secure=jwt_settings.get('AUTH_COOKIE_SECURE', False),
        samesite=jwt_settings.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        path=jwt_settings.get('AUTH_COOKIE_PATH', '/'),
    )
    
    if refresh_token:
        response.set_cookie(
            key=jwt_settings.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
            value=str(refresh_token),
            httponly=jwt_settings.get('AUTH_COOKIE_HTTP_ONLY', True),
            secure=jwt_settings.get('AUTH_COOKIE_SECURE', False),
            samesite=jwt_settings.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            path=jwt_settings.get('AUTH_COOKIE_PATH', '/'),
        )

def clear_jwt_cookies(response):
    """Clear JWT cookies based on SIMPLE_JWT settings."""
    
    jwt_settings = settings.SIMPLE_JWT
    
    response.set_cookie(
        key=jwt_settings.get('AUTH_COOKIE', 'access_token'),
        value='',
        max_age=0,
        httponly=jwt_settings.get('AUTH_COOKIE_HTTP_ONLY', True),
        secure=jwt_settings.get('AUTH_COOKIE_SECURE', False),
        samesite=jwt_settings.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        path=jwt_settings.get('AUTH_COOKIE_PATH', '/'),
    )
    
    response.set_cookie(
        key=jwt_settings.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
        value='',
        max_age=0,
        httponly=jwt_settings.get('AUTH_COOKIE_HTTP_ONLY', True),
        secure=jwt_settings.get('AUTH_COOKIE_SECURE', False),
        samesite=jwt_settings.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        path=jwt_settings.get('AUTH_COOKIE_PATH', '/'),
    )

def get_refresh_token_from_request(request):
    """Get refresh token from cookies."""
    
    jwt_settings = settings.SIMPLE_JWT
    return request.COOKIES.get(
        jwt_settings.get('AUTH_COOKIE_REFRESH', 'refresh_token')
    )
