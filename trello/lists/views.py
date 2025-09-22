"""
Django REST Framework views for list and task-related API endpoints.

This module defines generic views for listing, creating, retrieving, updating, deleting lists and tasks,
and moving tasks between lists. Views enforce authentication and restrict access to boards where the user
is either the owner or a member.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import List, Task
from .serializers import ListSerializer, TaskSerializer
from boards.models import Board
from django.db.models import Q

class ListListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating lists within a board.

    Handles GET requests to list all lists in a specified board where the user is the owner or a member,
    and POST requests to create new lists in the specified board.
    """
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters queryset to lists within a specific board where the user is the owner or a member.

        Returns:
            QuerySet: Lists accessible to the requesting user for the specified board.
        """
        board_id = self.kwargs.get('board_id')
        return List.objects.filter(board__id=board_id).filter(
            Q(board__owner=self.request.user) | Q(board__members=self.request.user)
        )

    def perform_create(self, serializer):
        """
        Custom creation logic for lists.

        Ensures the user is the board owner or a member before creating a list.
        Associates the list with the specified board.

        Args:
            serializer: The serializer instance with validated data.

        Raises:
            PermissionDenied: If the user is neither the board owner nor a member.
        """
        board_id = self.kwargs.get('board_id')
        board = Board.objects.get(id=board_id)
        if board.owner != self.request.user and not board.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You don't have permission to create lists in this board.")
        serializer.save(board=board)

class ListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific list.

    Restricts access to lists within a board where the user is the owner or a member.
    Supports GET, PUT/PATCH, and DELETE methods.
    """
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters queryset to lists within a specific board where the user is the owner or a member.

        Returns:
            QuerySet: Lists accessible to the requesting user for the specified board.
        """
        board_id = self.kwargs.get('board_id')
        return List.objects.filter(board__id=board_id).filter(
            Q(board__owner=self.request.user) | Q(board__members=self.request.user)
        )

class TaskListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating tasks within a list.

    Handles GET requests to list all tasks in a specified list where the user is the board owner or a member,
    and POST requests to create new tasks in the specified list.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters queryset to tasks within a specific list where the user is the board owner or a member.

        Returns:
            QuerySet: Tasks accessible to the requesting user for the specified list.
        """
        list_id = self.kwargs.get('list_id')
        return Task.objects.filter(list__id=list_id).filter(
            Q(list__board__owner=self.request.user) | Q(list__board__members=self.request.user)
        )

    def perform_create(self, serializer):
        """
        Custom creation logic for tasks.

        Ensures the user is the board owner or a member before creating a task.
        Associates the task with the specified list.

        Args:
            serializer: The serializer instance with validated data.

        Raises:
            PermissionDenied: If the user is neither the board owner nor a member.
        """
        list_id = self.kwargs.get('list_id')
        list_obj = List.objects.get(id=list_id)
        if list_obj.board.owner != self.request.user and not list_obj.board.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You don't have permission to create tasks in this list.")
        serializer.save(list=list_obj)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific task.

    Restricts access to tasks within a list where the user is the board owner or a member.
    Supports GET, PUT/PATCH, and DELETE methods.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters queryset to tasks within a specific list where the user is the board owner or a member.

        Returns:
            QuerySet: Tasks accessible to the requesting user for the specified list.
        """
        list_id = self.kwargs.get('list_id')
        return Task.objects.filter(list__id=list_id).filter(
            Q(list__board__owner=self.request.user) | Q(list__board__members=self.request.user)
        )

class TaskMoveView(generics.UpdateAPIView):
    """
    API view for moving a task to a different list or updating its order.

    Updates the task's list and/or order based on provided data. Ensures the user has permission
    to move the task to the target list.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters queryset to tasks where the user is the board owner or a member.

        Returns:
            QuerySet: Tasks accessible to the requesting user.
        """
        return Task.objects.filter(
            Q(list__board__owner=self.request.user) | Q(list__board__members=self.request.user)
        )

    def perform_update(self, serializer):
        """
        Custom update logic for moving a task or updating its order.

        Validates that the user has permission to move the task to the new list (if provided).
        Updates the task's list and/or order based on the request data.

        Args:
            serializer: The serializer instance with validated data.

        Raises:
            PermissionDenied: If the user is neither the board owner nor a member of the target list's board.
        """
        new_list_id = self.request.data.get('list_id')
        new_order = self.request.data.get('order')
        if new_list_id:
            new_list = List.objects.get(id=new_list_id)
            if new_list.board.owner != self.request.user and not new_list.board.members.filter(id=self.request.user.id).exists():
                raise PermissionDenied("You don't have permission to move tasks to this list.")
            serializer.save(list=new_list)
        if new_order is not None:
            serializer.save(order=new_order)