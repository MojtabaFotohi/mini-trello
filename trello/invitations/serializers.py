from rest_framework import serializers
from .models import Invitation
from boards.serializers import BoardSerializer  # اضافه شده
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class InvitationSerializer(serializers.ModelSerializer):
    invited_user_email = serializers.EmailField(write_only=True, required=False)
    board = BoardSerializer(read_only=True)  # تغییر به BoardSerializer
    
    class Meta:
        model = Invitation
        fields = ['id', 'board', 'invited_user', 'invited_user_email', 'status', 'created_at']
        read_only_fields = ['invited_user', 'created_at', 'board']

    def validate(self, data):
        logger.debug(f"Validating data: {data}")
        if self.context.get('request').method in ['POST']:
            if 'invited_user_email' in data and 'invited_user' in data:
                raise serializers.ValidationError("Provide either invited_user or invited_user_email, not both.")
            if 'invited_user_email' not in data and 'invited_user' not in data:
                raise serializers.ValidationError("Either invited_user or invited_user_email is required.")
            
            if 'invited_user_email' in data:
                email = data['invited_user_email'].lower().strip()
                logger.debug(f"Searching for user with email: {email}")
                try:
                    data['invited_user'] = User.objects.get(email__iexact=email)
                    logger.debug(f"Found user: {data['invited_user']}")
                except User.DoesNotExist:
                    logger.error(f"No user found with email: {email}")
                    raise serializers.ValidationError(f"No user found with email: {email}")
                except User.MultipleObjectsReturned:
                    logger.error(f"Multiple users found with email: {email}")
                    raise serializers.ValidationError(f"Multiple users found with email: {email}")
        
        return data

    def create(self, validated_data):
        validated_data.pop('invited_user_email', None)
        logger.debug(f"Creating invitation with validated_data: {validated_data}")
        return Invitation.objects.create(**validated_data)