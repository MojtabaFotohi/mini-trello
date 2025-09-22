"""
URL configuration for list and task-related endpoints.

This module defines the URL patterns for the list and task application, mapping API endpoints
to their respective views for listing, creating, retrieving, updating, deleting lists and tasks,
and moving tasks between lists.
"""

from django.urls import path
from .views import ListListCreateView, ListDetailView, TaskListCreateView, TaskDetailView, TaskMoveView

urlpatterns = [
    path('boards/<int:board_id>/lists/', ListListCreateView.as_view(), name='list-list-create'),  # Endpoint for listing or creating lists for a specific board
    path('boards/<int:board_id>/lists/<int:pk>/', ListDetailView.as_view(), name='list-detail'),  # Endpoint for retrieving, updating, or deleting a specific list
    path('lists/<int:list_id>/tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # Endpoint for listing or creating tasks for a specific list
    path('lists/<int:list_id>/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),  # Endpoint for retrieving, updating, or deleting a specific task
    path('tasks/<int:pk>/move/', TaskMoveView.as_view(), name='task-move'),  # Endpoint for moving a task to a different list
]