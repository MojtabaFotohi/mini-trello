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
        if board.members.filter(id=invited_user.id).exists():
            logger.error(f"User {invited_user} is already a member of board {board}")
            raise ValidationError("User is already a member of this board.")
        logger.debug(f"Invited user: {invited_user}")
        
        if Invitation.objects.filter(board=board, invited_user=invited_user, status='pending').exists():
            logger.error(f"Duplicate invitation for user {invited_user} to board {board}")
            raise ValidationError("An invitation for this user to this board already exists.")

        if board.members.count() >= 10:
            logger.error(f"Board {board} has reached maximum members (10)")
            raise ValidationError("Cannot add more than 10 members to a board.")
        
        # چک کردن لیمیت ۵ بورد برای invited_user
        max_boards = 5
        total_boards = Board.objects.filter(
            Q(owner=invited_user) | Q(members=invited_user)
        ).distinct().count()
        if total_boards >= max_boards:
            logger.error(f"User {invited_user} has reached maximum board limit ({max_boards})")
            raise ValidationError(f"User cannot be a member of more than {max_boards} boards.")

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
        
        # چک کردن لیمیت ۵ بورد برای کاربر در زمان پذیرش دعوت‌نامه
        max_boards = 5
        total_boards = Board.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct().count()
        if total_boards >= max_boards:
            raise ValidationError(f"User cannot be a member of more than {max_boards} boards.")
        
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
