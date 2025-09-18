from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    preferred_language = models.CharField(max_length=10, choices=[('en', 'English'), ('fa', 'Persian')], default='en')

    def __str__(self):
        return self.username