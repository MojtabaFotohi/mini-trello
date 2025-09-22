"""
Django middleware for handling user language preferences.

This module defines a middleware that sets the active language based on the authenticated
user's preferred language, either from a JWT token or session-based authentication.
It ensures the language is activated for each request and deactivated afterward to prevent memory leaks.
"""

from django.utils import translation
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

class UserLanguageMiddleware:
    """
    Middleware to set the active language based on user preferences.

    Activates the user's preferred language for each request, either from a JWT token or session.
    Falls back to the session language or default if no user language is found.
    Deactivates translation after processing to prevent memory leaks.
    """
    def __init__(self, get_response):
        """
        Initializes the middleware with the get_response callable.

        Args:
            get_response: The next middleware or view in the request-response cycle.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Processes each request to set the active language.

        Sets the language based on the user's preferred language (from JWT or session).
        If no user is authenticated, uses the session language if available.
        Deactivates translation after processing the response.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The response from the next middleware or view.
        """
        # Set language based on user
        user_language = self.get_user_language(request)
        if user_language:
            translation.activate(user_language)
            request.LANGUAGE_CODE = user_language
        else:
            # If user is not authenticated, use session language if available
            session_language = request.session.get('_language')
            if session_language:
                translation.activate(session_language)
                request.LANGUAGE_CODE = session_language

        response = self.get_response(request)
        
        # Deactivate translation to prevent memory leaks
        translation.deactivate()
        
        return response

    def get_user_language(self, request):
        """
        Determines the user's preferred language from JWT token or session.

        Checks for a valid JWT token first, then falls back to session-based authentication.
        Returns the user's preferred language if available, otherwise None.

        Args:
            request: The HTTP request object.

        Returns:
            str or None: The user's preferred language code, or None if not found.

        Raises:
            None: Handles exceptions gracefully by returning None.
        """
        try:
            # Check JWT token for user language
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(
                jwt_auth.get_raw_token(jwt_auth.get_header(request))
            )
            user = jwt_auth.get_user(validated_token)
            if user and hasattr(user, 'preferred_language'):
                return user.preferred_language
        except (InvalidToken, TokenError, AttributeError, TypeError):
            pass
        
        # Check session-based authentication for user language
        if request.user.is_authenticated and hasattr(request.user, 'preferred_language'):
            return request.user.preferred_language
        
        return None