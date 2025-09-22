"""
Django REST Framework views for board-related API endpoints.

This module defines generic views for listing/creating boards and retrieving/updating/deleting individual boards.
Views ensure authentication and restrict access to boards owned or membership-based.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Board
from .serializers import BoardSerializer
from django.db.models import Q


class BoardListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating boards.

    Handles GET requests to list boards the user owns or is a member of,
    and POST requests to create new boards with the authenticated user as owner.
    Enforces a limit of 5 total boards per user (owned or joined).
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom creation logic to enforce board limit and set owner.

        Checks if the user has reached the maximum of 5 boards (owned or membership).
        Raises ValidationError if limit exceeded.
        Saves the serializer with the request user as owner.
        """
        max_boards = 5  # Board limit per user
        # Counting the total boards that the user owns or is a member of
        total_boards = Board.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct().count()
        if total_boards >= max_boards:
            raise ValidationError(f"Cannot create or join more than {max_boards} boards.")
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Filters queryset to boards owned by or where the user is a member.

        Returns:
            QuerySet: Boards accessible to the requesting user.
        """
        return Board.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user))


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific board.

    Restricts access to boards the user owns or is a member of.
    Supports GET, PUT/PATCH, and DELETE methods.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters queryset to boards owned by or where the user is a member.

        Ensures only accessible boards can be retrieved/updated/deleted.
        Returns:
            QuerySet: Boards accessible to the requesting user.
        """
        return Board.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user))