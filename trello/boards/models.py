"""
Django model for a Board entity.

This module defines the Board model, which represents a board in the application.
Each board has a title, an owner, members, a color, and timestamps for creation and updates.
"""

from django.db import models
from django.conf import settings

class Board(models.Model):
    """
    Represents a board in the application.

    Attributes:
        title (CharField): The title of the board, with a maximum length of 100 characters.
        owner (ForeignKey): The user who owns the board, linked to the AUTH_USER_MODEL.
                          Deleted boards are removed if the owner is deleted (CASCADE).
        members (ManyToManyField): Users who are members of the board, linked to AUTH_USER_MODEL.
        color (CharField): The color of the board in hexadecimal format, defaulting to white (#FFFFFF).
        created_at (DateTimeField): Timestamp when the board was created, set automatically on creation.
        updated_at (DateTimeField): Timestamp when the board was last updated, updated automatically.
    """
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='board_memberships')
    color = models.CharField(max_length=7, default='#FFFFFF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the Board instance.

        Returns:
            str: The title of the board.
        """
        return self.title