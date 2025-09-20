# users/context_processors.py (یا یک app دیگر)
from django.utils import translation

def user_language_context(request):
    """Context processor برای اضافه کردن اطلاعات زبان به تمام templates"""
    
    context = {
        'current_language_code': translation.get_language(),
        'user_authenticated': request.user.is_authenticated,
    }
    
    # اگر کاربر لاگین باشد، زبان او را اضافه کن
    if request.user.is_authenticated and hasattr(request.user, 'preferred_language'):
        context['user_preferred_language'] = request.user.preferred_language
        # تنظیم زبان فعال بر اساس تنظیمات کاربر
        if request.user.preferred_language != translation.get_language():
            translation.activate(request.user.preferred_language)
            request.session['_language'] = request.user.preferred_language
            context['current_language_code'] = request.user.preferred_language
    else:
        context['user_preferred_language'] = 'en'
    
    return context