"""
URL configuration for the board-related endpoints.

This module defines the URL patterns for the board application, mapping API endpoints
to their respective views for listing, creating, retrieving, updating, and deleting boards.
"""

from django.urls import path
from .views import BoardListCreateView, BoardDetailView

urlpatterns = [
    path('', BoardListCreateView.as_view(), name='board-list-create'),  # Endpoint for listing all boards or creating a new board
    path('<int:pk>/', BoardDetailView.as_view(), name='board-detail'),  # Endpoint for retrieving, updating, or deleting a specific board by its primary key
]