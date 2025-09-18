from django.utils.translation import gettext as _
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class TestTranslationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "welcome": _("Welcome"),
            "board_created": _("Board created"),
            "profile_updated": _("Profile updated"),
            "list_created": _("List created"),
            "task_created": _("Task created")
        })