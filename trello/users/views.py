# users/views.py
from django.utils.translation import gettext as _
from django.utils import translation
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from django.contrib.auth import authenticate, login
from .models import User
from .serializers import UserSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()

        
        # تنظیم زبان در session
        translation.activate(user.preferred_language)
        self.request.session['_language'] = user.preferred_language
        
        return user
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # تنظیم header زبان در response
        if hasattr(request, 'session') and '_language' in request.session:
            response['X-User-Language'] = request.session['_language']
        return response

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        
        # تنظیم زبان بر اساس کاربر فعلی
        translation.activate(user.preferred_language)
        self.request.session['_language'] = user.preferred_language
        
        return user
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        
        # اگر زبان تغییر کرده باشد، آن را در session ذخیره کن
        user = self.get_object()
        if 'preferred_language' in request.data:
            new_language = request.data['preferred_language']
            translation.activate(new_language)
            request.session['_language'] = new_language
            response['X-User-Language'] = new_language
        
        return response

class CustomTokenObtainPairView(BaseTokenObtainPairView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            
            # تنظیم زبان در session
            translation.activate(user.preferred_language)
            request.session['_language'] = user.preferred_language
            
            # فراخوانی method parent برای تولید token
            response = super().post(request, *args, **kwargs)
            
            # اضافه کردن اطلاعات کاربر به response
            if response.status_code == 200:
                response.data.update({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'name': user.name,
                        'preferred_language': user.preferred_language
                    },
                    'message': _('Login successful')
                })
                response['X-User-Language'] = user.preferred_language
            
            return response
        
        return Response({
            'error': _('Invalid credentials'),
            'message': _('Please check your username and password')
        }, status=status.HTTP_401_UNAUTHORIZED)

class TestTranslationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        current_language = translation.get_language()
        
        # تست ترجمه‌ها
        return Response({
            "current_language": current_language,
            "session_language": request.session.get('_language'),
            "translations": {
                "welcome": _("Welcome to Modern Trello"),
                "board_created": _("Create Board"),
                "profile_updated": _("Profile updated"),
                "list_created": _("Add List"),
                "task_created": _("Add Task"),
                "login": _("Login"),
                "signup": _("Sign Up"),
                "logout": _("Logout"),
                "username": _("Username"),
                "password": _("Password"),
                "email": _("Email"),
                "cancel": _("Cancel"),
                "close": _("Close")
            },
            "user_language": request.user.preferred_language if request.user.is_authenticated else None
        })