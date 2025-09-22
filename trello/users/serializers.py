"""
Django REST Framework serializers for user-related operations.

This module defines serializers for user registration and user profile serialization.
The RegisterSerializer handles user creation with validation, while the UserSerializer
provides a read-only representation of user data.
"""

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles the creation of new user accounts, including validation of the preferred language
    and secure password handling.

    Attributes:
        None: Inherits fields from Meta class.
    """
    class Meta:
        """
        Meta class for RegisterSerializer.

        Defines the model to serialize, fields to include, and additional field options.
        """
        model = User
        fields = ['id', 'username', 'email', 'password', 'name', 'preferred_language']
        extra_kwargs = {
            'password': {'write_only': True},  # Password is write-only
            'id': {'read_only': True},  # ID is read-only
            'preferred_language': {'required': False, 'default': 'en'}  # Preferred language is optional, defaults to 'en'
        }

    def validate_preferred_language(self, value):
        """
        Validates the preferred language field.

        Ensures the provided language code is one of the valid choices defined in the User model.

        Args:
            value (str): The language code to validate.

        Returns:
            str: The validated language code.

        Raises:
            serializers.ValidationError: If the language code is not valid.
        """
        valid_languages = [lang[0] for lang in User._meta.get_field('preferred_language').choices]
        if value not in valid_languages:
            raise serializers.ValidationError("Invalid language code")
        return value

    def create(self, validated_data):
        """
        Creates a new user instance.

        Uses Django's create_user method to securely create a user with the provided data,
        ensuring password hashing and proper initialization.

        Args:
            validated_data (dict): Validated data containing user details.

        Returns:
            User: The created User instance.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            preferred_language=validated_data.get('preferred_language', 'en')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.

    Provides a read-only representation of user details for API responses.

    Attributes:
        None: Inherits fields from Meta class.
    """
    class Meta:
        """
        Meta class for UserSerializer.

        Defines the model to serialize and fields to include.
        """
        model = User
        fields = ['id', 'username', 'email', 'name', 'preferred_language']