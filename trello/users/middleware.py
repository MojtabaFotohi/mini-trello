# users/middleware.py
from django.utils import translation
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # تنظیم زبان بر اساس کاربر
        user_language = self.get_user_language(request)
        if user_language:
            translation.activate(user_language)
            request.LANGUAGE_CODE = user_language
        else:
            # اگر کاربر وارد نشده، از زبان پیش‌فرض یا session استفاده کن
            session_language = request.session.get('_language')
            if session_language:
                translation.activate(session_language)
                request.LANGUAGE_CODE = session_language

        response = self.get_response(request)
        
        # Deactivate translation to prevent memory leaks
        translation.deactivate()
        
        return response

    def get_user_language(self, request):
        """تشخیص زبان کاربر از JWT token یا session"""
        try:
            # بررسی JWT token
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(
                jwt_auth.get_raw_token(jwt_auth.get_header(request))
            )
            user = jwt_auth.get_user(validated_token)
            if user and hasattr(user, 'preferred_language'):
                return user.preferred_language
        except (InvalidToken, TokenError, AttributeError, TypeError):
            pass
        
        # بررسی session-based authentication
        if request.user.is_authenticated and hasattr(request.user, 'preferred_language'):
            return request.user.preferred_language
        
        return None