"""
URL configuration for invitation-related endpoints.

This module defines the URL patterns for the invitation application, mapping API endpoints
to their respective views for listing, creating, accepting, and rejecting invitations.
"""

from django.urls import path
from .views import InvitationListCreateView, InvitationAcceptView, InvitationRejectView

urlpatterns = [
    path('', InvitationListCreateView.as_view(), name='invitation-list-create'),  # Endpoint for listing all invitations or creating a new invitation
    path('<int:pk>/accept/', InvitationAcceptView.as_view(), name='invitation-accept'),  # Endpoint for accepting an invitation by its primary key
    path('<int:pk>/reject/', InvitationRejectView.as_view(), name='invitation-reject'),  # Endpoint for rejecting an invitation by its primary key
]