"""
Django model for an Invitation entity.

This module defines the Invitation model, which represents an invitation to join a board
in the application. Each invitation links a user to a board and tracks its status.
"""

from django.db import models
from django.conf import settings

class Invitation(models.Model):
    """
    Represents an invitation to join a board.

    Attributes:
        board (ForeignKey): The board to which the invitation is related, linked to the Board model.
                           Deleted invitations are removed if the board is deleted (CASCADE).
        invited_user (ForeignKey): The user who is invited, linked to the AUTH_USER_MODEL.
                                  Deleted invitations are removed if the user is deleted (CASCADE).
        created_at (DateTimeField): Timestamp when the invitation was created, set automatically on creation.
        status (CharField): The status of the invitation, with choices 'pending', 'accepted', or 'rejected'.
                           Defaults to 'pending'.
    """
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )

    def __str__(self):
        """
        Returns the string representation of the Invitation instance.

        Returns:
            str: A description of the invitation, including the board and invited user.
        """
        return f"Invitation to {self.board} for {self.invited_user}"