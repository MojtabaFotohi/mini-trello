"""
Django models for List and Task entities.

This module defines the List and Task models, which represent lists and tasks within a board
in the application. Lists belong to a board, and tasks belong to a list, with additional
attributes for task management such as due dates and assigned users.
"""

from django.db import models
from django.conf import settings

class List(models.Model):
    """
    Represents a list within a board.

    Attributes:
        title (CharField): The title of the list, with a maximum length of 100 characters.
        board (ForeignKey): The board to which the list belongs, linked to the Board model.
                           Deleted lists are removed if the board is deleted (CASCADE).
        created_at (DateTimeField): Timestamp when the list was created, set automatically on creation.
        updated_at (DateTimeField): Timestamp when the list was last updated, updated automatically.
    """
    title = models.CharField(max_length=100)
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE, related_name='lists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the List instance.

        Returns:
            str: The title of the list.
        """
        return self.title

class Task(models.Model):
    """
    Represents a task within a list.

    Attributes:
        title (CharField): The title of the task, with a maximum length of 100 characters.
        description (TextField): An optional description of the task, can be blank.
        list (ForeignKey): The list to which the task belongs, linked to the List model.
                          Deleted tasks are removed if the list is deleted (CASCADE).
        due_date (DateTimeField): Optional due date for the task, can be null or blank.
        order (PositiveIntegerField): The order of the task within the list, defaults to 0.
        assigned_users (ManyToManyField): Users assigned to the task, linked to AUTH_USER_MODEL, can be blank.
        created_at (DateTimeField): Timestamp when the task was created, set automatically on creation.
        updated_at (DateTimeField): Timestamp when the task was last updated, updated automatically.
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the Task instance.

        Returns:
            str: The title of the task.
        """
        return self.title