"""
Context processor for adding language-related information to all templates.

This module defines a context processor that provides the current language code,
user authentication status, and the user's preferred language to all templates.
It also activates the user's preferred language if they are authenticated.
"""

from django.utils import translation

def user_language_context(request):
    """
    Context processor to add language information to all templates.

    Adds the current language code, user authentication status, and the user's preferred
    language to the template context. If the user is authenticated and has a preferred
    language, it activates that language and updates the session.

    Args:
        request: The HTTP request object.

    Returns:
        dict: A dictionary containing the current language code, authentication status,
              and the user's preferred language.
    """
    context = {
        'current_language_code': translation.get_language(),  # Current active language code
        'user_authenticated': request.user.is_authenticated,  # Boolean indicating if the user is authenticated
    }
    
    # If the user is authenticated and has a preferred language, add it to the context
    if request.user.is_authenticated and hasattr(request.user, 'preferred_language'):
        context['user_preferred_language'] = request.user.preferred_language
        # Activate the user's preferred language if it differs from the current language
        if request.user.preferred_language != translation.get_language():
            translation.activate(request.user.preferred_language)
            request.session['_language'] = request.user.preferred_language
            context['current_language_code'] = request.user.preferred_language
    else:
        context['user_preferred_language'] = 'en'  # Default to English if not authenticated or no preferred language
    
    return context