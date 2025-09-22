"""
Django REST Framework serializers for List and Task models.

This module defines serializers for the List and Task models, handling serialization
and deserialization for API interactions. Includes nested serialization for tasks within lists
and validation for assigned users.
"""

from rest_framework import serializers
from .models import List, Task
from django.contrib.auth import get_user_model

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Converts Task model instances to JSON and validates incoming data.
    Supports assigning multiple users to a task via their primary keys.

    Attributes:
        assigned_users (PrimaryKeyRelatedField): Field for assigning users to the task,
                                               allows multiple users, optional.
    """
    assigned_users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=get_user_model().objects.all(),
        required=False
    )

    class Meta:
        """
        Meta class for TaskSerializer.

        Defines the model to serialize, fields to include, and read-only fields.
        """
        model = Task
        fields = ['id', 'title', 'description', 'list', 'due_date', 'order', 'assigned_users', 'created_at', 'updated_at']
        read_only_fields = ['list', 'created_at', 'updated_at']

class ListSerializer(serializers.ModelSerializer):
    """
    Serializer for the List model.

    Converts List model instances to JSON and validates incoming data.
    Includes nested serialization for tasks associated with the list.

    Attributes:
        tasks (TaskSerializer): Nested serializer for tasks belonging to the list, read-only.
    """
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for ListSerializer.

        Defines the model to serialize, fields to include, and read-only fields.
        """
        model = List
        fields = ['id', 'title', 'board', 'tasks', 'created_at', 'updated_at']
        read_only_fields = ['board', 'created_at', 'updated_at']