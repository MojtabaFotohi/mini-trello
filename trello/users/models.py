from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
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
        return self.username