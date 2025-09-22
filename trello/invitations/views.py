from django.db import models
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Invitation
from .serializers import InvitationSerializer
from boards.models import Board
from django.contrib.auth import get_user_model
from .tasks import send_invitation_email
from django.db.models import Q

User = get_user_model()

class InvitationListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating invitations.

    Handles GET requests to list invitations where the user is either the board owner or the invited user,
    and POST requests to create new invitations for a board, with validation for board ownership,
    member limits, and duplicate invitations.
    """
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters queryset to invitations where the user is either the board owner or the invited user.

        Returns:
            QuerySet: Invitations accessible to the requesting user.
        """
        return Invitation.objects.filter(
            models.Q(board__owner=self.request.user) | models.Q(invited_user=self.request.user)
        )

    def perform_create(self, serializer):
        """
        Custom creation logic for invitations.

        Validates board ownership, checks for duplicate invitations, enforces board member limits (10),
        and ensures the invited user does not exceed the maximum board limit (5).
        Sends an email notification for the invitation using a Celery task.

        Args:
            serializer: The serializer instance with validated data.

        Raises:
            ValidationError: If the board doesn't exist, the user isn't the owner, the invited user is
                            already a member, a duplicate invitation exists, or limits are exceeded.
        """
        board_id = self.request.data.get('board')
        try:
            board = Board.objects.get(id=board_id, owner=self.request.user)
        except Board.DoesNotExist:
            raise ValidationError(f"Board with id {board_id} does not exist or you are not the owner.")

        invited_user = serializer.validated_data['invited_user']
        if board.members.filter(id=invited_user.id).exists():
            raise ValidationError("User is already a member of this board.")
        
        if Invitation.objects.filter(board=board, invited_user=invited_user, status='pending').exists():
            raise ValidationError("An invitation for this user to this board already exists.")

        if board.members.count() >= 10:
            raise ValidationError("Cannot add more than 10 members to a board.")
        
        # Check the invited user's board limit (5 boards)
        max_boards = 5
        total_boards = Board.objects.filter(
            Q(owner=invited_user) | Q(members=invited_user)
        ).distinct().count()
        if total_boards >= max_boards:
            raise ValidationError(f"User cannot be a member of more than {max_boards} boards.")

        invitation = serializer.save(board=board)
        send_invitation_email.delay(invitation.id, invited_user.preferred_language)

class InvitationAcceptView(generics.UpdateAPIView):
    """
    API view for accepting an invitation.

    Updates the invitation status to 'accepted' and adds the invited user to the board's members.
    Ensures the user can only accept their own invitations and enforces board and user limits.
    """
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.all()

    def perform_update(self, serializer):
        """
        Custom update logic for accepting an invitation.

        Validates that the user is the invited user, the invitation is pending, the board has not
        reached its member limit (10), and the user has not exceeded their board limit (5).
        Adds the user to the board's members and updates the invitation status.

        Args:
            serializer: The serializer instance with validated data.

        Raises:
            ValidationError: If the user is not the invited user, the invitation is already processed,
                            or board/user limits are exceeded.
        """
        invitation = self.get_object()
        if invitation.invited_user != self.request.user:
            raise ValidationError("You can only accept your own invitations.")
        if invitation.status != 'pending':
            raise ValidationError("This invitation is already processed.")
        
        board = invitation.board
        if board.members.count() >= 10:
            raise ValidationError("Cannot add more than 10 members to a board.")
        
        # Check the user's board limit (5 boards) at the time of accepting the invitation
        max_boards = 5
        total_boards = Board.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct().count()
        if total_boards >= max_boards:
            raise ValidationError(f"User cannot be a member of more than {max_boards} boards.")
        
        board.members.add(invitation.invited_user)
        serializer.save(status='accepted')

    def update(self, request, *args, **kwargs):
        """
        Handles the update request for accepting an invitation.

        Updates the invitation status to 'accepted' and returns the serialized data.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized invitation data.
        """
        data = {'status': 'accepted'}
        serializer = self.get_serializer(self.get_object(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class InvitationRejectView(generics.UpdateAPIView):
    """
    API view for rejecting an invitation.

    Updates the invitation status to 'rejected'. Ensures the user can only reject their own
    invitations and that the invitation is still pending.
    """
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.all()

    def perform_update(self, serializer):
        """
        Custom update logic for rejecting an invitation.

        Validates that the user is the invited user and the invitation is pending.
        Updates the invitation status to 'rejected'.

        Args:
            serializer: The serializer instance with validated data.

        Raises:
            ValidationError: If the user is not the invited user or the invitation is already processed.
        """
        invitation = self.get_object()
        if invitation.invited_user != self.request.user:
            raise ValidationError("You can only reject your own invitations.")
        if invitation.status != 'pending':
            raise ValidationError("This invitation is already processed.")
        
        serializer.save(status='rejected')

    def update(self, request, *args, **kwargs):
        """
        Handles the update request for rejecting an invitation.

        Updates the invitation status to 'rejected' and returns the serialized data.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized invitation data.
        """
        data = {'status': 'rejected'}
        serializer = self.get_serializer(self.get_object(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)