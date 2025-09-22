"""
Django model for a custom User entity.

This module defines a custom User model that extends Django's AbstractUser,
adding fields for name, unique email, and preferred language.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Adds fields for name, unique email, and preferred language to the default Django user model.

    Attributes:
        name (CharField): The user's full name, with a maximum length of 100 characters, optional.
        email (EmailField): The user's email address, must be unique.
        preferred_language (CharField): The user's preferred language, with predefined choices
                                       (English, Persian, Arabic, German, French), defaults to English ('en').
    """
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    preferred_language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('fa', 'Persian'),
            ('ar', 'Arabic'),
            ('de', 'German'),
            ('fr', 'French'),
        ],
        default='en'
    )

    def __str__(self):
        """
        Returns the string representation of the User instance.

        Returns:
            str: The username of the user.
        """
        return self.username