from rest_framework import serializers
from .models import Invitation
from boards.serializers import BoardSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class InvitationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invitation model.

    Handles conversion of Invitation model instances to JSON and validates incoming data.
    Supports inviting users by email and includes nested serialization for the board.

    Attributes:
        invited_user_email (EmailField): Write-only field for the email of the invited user.
        board (BoardSerializer): Serializer for the board associated with the invitation, read-only.
    """
    invited_user_email = serializers.EmailField(write_only=True, required=False)
    board = BoardSerializer(read_only=True)

    class Meta:
        """
        Meta class for InvitationSerializer.

        Defines the model to serialize, fields to include, and read-only fields.
        """
        model = Invitation
        fields = ['id', 'board', 'invited_user', 'invited_user_email', 'status', 'created_at']
        read_only_fields = ['invited_user', 'created_at', 'board']

    def validate(self, data):
        """
        Validates the incoming data for creating or updating invitations.

        Ensures that either invited_user or invited_user_email is provided, but not both.
        If invited_user_email is provided, it attempts to find a matching user by email.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: Validated data with invited_user set if email is provided.

        Raises:
            serializers.ValidationError: If validation fails due to missing or conflicting fields,
                                        or if no/single user is found for the provided email.
        """
        if self.context.get('request').method in ['POST']:
            if 'invited_user_email' in data and 'invited_user' in data:
                raise serializers.ValidationError("Provide either invited_user or invited_user_email, not both.")
            if 'invited_user_email' not in data and 'invited_user' not in data:
                raise serializers.ValidationError("Either invited_user or invited_user_email is required.")
            
            if 'invited_user_email' in data:
                email = data['invited_user_email'].lower().strip()
                try:
                    data['invited_user'] = User.objects.get(email__iexact=email)
                except User.DoesNotExist:
                    raise serializers.ValidationError(f"No user found with email: {email}")
                except User.MultipleObjectsReturned:
                    raise serializers.ValidationError(f"Multiple users found with email: {email}")
        
        return data

    def create(self, validated_data):
        """
        Creates a new Invitation instance.

        Removes the invited_user_email from validated_data (as it is write-only)
        and creates the invitation with the remaining validated data.

        Args:
            validated_data (dict): Validated data for creating the invitation.

        Returns:
            Invitation: The created Invitation instance.
        """
        validated_data.pop('invited_user_email', None)
        return Invitation.objects.create(**validated_data)