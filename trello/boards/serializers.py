"""
Django REST Framework serializer for the Board model.

This module defines the BoardSerializer, which handles serialization and deserialization
of Board model instances for API interactions.
"""

from rest_framework import serializers
from .models import Board
from users.serializers import UserSerializer

class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for the Board model.

    This serializer converts Board model instances to JSON format and validates incoming data.
    It includes nested serialization for the owner and members using UserSerializer.

    Attributes:
        owner (UserSerializer): Serializer for the board's owner, read-only.
        members (UserSerializer): Serializer for the board's members, supports multiple users, read-only.
    """
    owner = UserSerializer(read_only=True)  # Uses UserSerializer for owner representation
    members = UserSerializer(many=True, read_only=True)  # Uses UserSerializer for members, handling multiple users

    class Meta:
        """
        Meta class for BoardSerializer.

        Defines the model to serialize, fields to include, and read-only fields.
        """
        model = Board
        fields = ['id', 'title', 'owner', 'members', 'color', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']