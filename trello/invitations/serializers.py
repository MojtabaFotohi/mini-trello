from rest_framework import serializers
from .models import Invitation
from django.contrib.auth import get_user_model

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'board', 'invited_user', 'status', 'created_at']
        read_only_fields = ['created_at']