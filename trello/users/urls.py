"""
URL configuration for user-related endpoints.

This module defines the URL patterns for user management and authentication,
mapping API endpoints to their respective views for registration, profile management,
and testing translation functionality.
"""

from django.urls import path
from .views import RegisterView, ProfileView, TestTranslationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Endpoint for user registration
    path('profile/', ProfileView.as_view(), name='profile'),  # Endpoint for retrieving or updating user profile
    path('test-translation/', TestTranslationView.as_view(), name='test-translation'),  # Endpoint for testing translation functionality
]