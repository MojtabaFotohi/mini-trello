"""
Django REST Framework views for user-related operations.

This module defines views for user registration, profile management, JWT token authentication,
and testing translation functionality. Views handle language activation based on user preferences
and ensure proper session and response handling.
"""

from django.utils.translation import gettext as _
from django.utils import translation
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    Allows unauthenticated users to create a new account using the RegisterSerializer.
    Sets the user's preferred language in the session upon successful registration.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Custom creation logic for user registration.

        Saves the user and activates their preferred language in the session.

        Args:
            serializer: The serializer instance with validated data.

        Returns:
            User: The created User instance.
        """
        user = serializer.save()
        # Set language in session
        translation.activate(user.preferred_language)
        self.request.session['_language'] = user.preferred_language
        return user

    def create(self, request, *args, **kwargs):
        """
        Handles the creation request for a new user.

        Extends the default create method to include the user's preferred language in the response header.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing the serialized user data and language header.
        """
        response = super().create(request, *args, **kwargs)
        # Set language header in response
        if hasattr(request, 'session') and '_language' in request.session:
            response['X-User-Language'] = request.session['_language']
        return response

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profiles.

    Allows authenticated users to view or update their profile details.
    Updates the session language if the preferred language is changed.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves the authenticated user's profile.

        Activates the user's preferred language and updates the session.

        Returns:
            User: The authenticated User instance.
        """
        user = self.request.user
        # Set language based on current user
        translation.activate(user.preferred_language)
        self.request.session['_language'] = user.preferred_language
        return user

    def update(self, request, *args, **kwargs):
        """
        Handles the update request for the user profile.

        Updates the session and response header if the preferred language is changed.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing the updated serialized user data and language header.
        """
        response = super().update(request, *args, **kwargs)
        # If language is updated, save it in session
        user = self.get_object()
        if 'preferred_language' in request.data:
            new_language = request.data['preferred_language']
            translation.activate(new_language)
            request.session['_language'] = new_language
            response['X-User-Language'] = new_language
        return response

class CustomTokenObtainPairView(BaseTokenObtainPairView):
    """
    Custom API view for JWT token authentication.

    Authenticates users and returns a JWT token along with user details.
    Sets the user's preferred language in the session and response header.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles the token authentication request.

        Authenticates the user with provided credentials, generates a JWT token,
        and includes user details and a success message in the response.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing the token, user details, and language header,
                     or an error message if authentication fails.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            # Set language in session
            translation.activate(user.preferred_language)
            request.session['_language'] = user.preferred_language
            
            # Call parent method to generate token
            response = super().post(request, *args, **kwargs)
            
            # Add user information to response
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
    """
    API view for testing translation functionality.

    Returns a set of translated strings and language information for testing purposes.
    Accessible to all users (authenticated or not).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Handles GET requests to test translations.

        Returns the current language, session language, a set of translated strings,
        and the user's preferred language (if authenticated).

        Args:
            request: The HTTP request object.

        Returns:
            Response: A dictionary containing language details and translated strings.
        """
        current_language = translation.get_language()
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