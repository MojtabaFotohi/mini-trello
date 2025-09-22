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
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class InvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.filter(
            models.Q(board__owner=self.request.user) | models.Q(invited_user=self.request.user)
        )

    def perform_create(self, serializer):
        logger.debug(f"Request data: {self.request.data}")
        board_id = self.request.data.get('board')
        try:
            board = Board.objects.get(id=board_id, owner=self.request.user)
            logger.debug(f"Found board: {board}")
        except Board.DoesNotExist:
            logger.error(f"Board with id {board_id} does not exist or user is not owner")
            raise ValidationError(f"Board with id {board_id} does not exist or you are not the owner.")

        invited_user = serializer.validated_data['invited_user']
        logger.debug(f"Invited user: {invited_user}")
        
        if Invitation.objects.filter(board=board, invited_user=invited_user, status='pending').exists():
            logger.error(f"Duplicate invitation for user {invited_user} to board {board}")
            raise ValidationError("An invitation for this user to this board already exists.")

        if board.members.count() >= 10:
            logger.error(f"Board {board} has reached maximum members (10)")
            raise ValidationError("Cannot add more than 10 members to a board.")
        
        if invited_user.board_memberships.count() >= 20:
            logger.error(f"User {invited_user} has reached maximum board memberships (20)")
            raise ValidationError("User cannot be a member of more than 20 boards.")

        invitation = serializer.save(board=board)
        logger.debug(f"Created invitation: {invitation}")
        send_invitation_email.delay(invitation.id, invited_user.preferred_language)

class InvitationAcceptView(generics.UpdateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.all()

    def perform_update(self, serializer):
        invitation = self.get_object()
        if invitation.invited_user != self.request.user:
            raise ValidationError("You can only accept your own invitations.")
        if invitation.status != 'pending':
            raise ValidationError("This invitation is already processed.")
        
        board = invitation.board
        if board.members.count() >= 10:
            raise ValidationError("Cannot add more than 10 members to a board.")
        if invitation.invited_user.board_memberships.count() >= 20:
            raise ValidationError("User cannot be a member of more than 20 boards.")
        
        board.members.add(invitation.invited_user)
        serializer.save(status='accepted')

    def update(self, request, *args, **kwargs):
        data = {'status': 'accepted'}
        serializer = self.get_serializer(self.get_object(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class InvitationRejectView(generics.UpdateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.all()

    def perform_update(self, serializer):
        invitation = self.get_object()
        if invitation.invited_user != self.request.user:
            raise ValidationError("You can only reject your own invitations.")
        if invitation.status != 'pending':
            raise ValidationError("This invitation is already processed.")
        
        serializer.save(status='rejected')

    def update(self, request, *args, **kwargs):
        data = {'status': 'rejected'}
        serializer = self.get_serializer(self.get_object(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)