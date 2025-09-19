from django.utils.translation import gettext as _
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from django.utils import translation
from .models import User
from .serializers import UserSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        print(f"Registered user: {user.username}, Language: {user.preferred_language}")  # دیباگ
        translation.activate(user.preferred_language)
        self.request.session['_language'] = user.preferred_language
        print(f"Session language set to: {self.request.session.get('_language')}")  # دیباگ

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print(f"Profile accessed, User language: {self.request.user.preferred_language}")  # دیباگ
        return self.request.user

class TokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print(f"Login user: {user.username}, Language: {user.preferred_language}")  # دیباگ
            translation.activate(user.preferred_language)
            request.session['_language'] = user.preferred_language
            print(f"Session language after login: {request.session.get('_language')}")  # دیباگ
            response = super().post(request, *args, **kwargs)
            return response
        print("Login failed: Invalid credentials")  # دیباگ
        return Response({'error': _('Invalid credentials')}, status=401)

class TestTranslationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        current_language = translation.get_language()
        print(f"TestTranslationView, Current language: {current_language}")  # دیباگ
        return Response({
            "welcome": _("Welcome to Modern Trello"),
            "board_created": _("Create Board"),
            "profile_updated": _("Profile updated"),
            "list_created": _("Add List"),
            "task_created": _("Add Task"),
            "current_language": current_language
        })