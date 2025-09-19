from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Invitation
from .serializers import InvitationSerializer
from boards.models import Board
from django.contrib.auth import get_user_model

User = get_user_model()

class InvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.filter(board__owner=self.request.user)

    def perform_create(self, serializer):
        board_id = self.request.data.get('board')
        invited_user_id = self.request.data.get('invited_user')
        board = Board.objects.get(id=board_id, owner=self.request.user)
        invited_user = User.objects.get(id=invited_user_id)

        # محدودیت M: حداکثر ۱۰ عضو در برد
        if board.members.count() >= 10:
            raise ValidationError("Cannot add more than 10 members to a board.")
        # محدودیت K: حداکثر ۲۰ عضویت برای کاربر
        if invited_user.board_memberships.count() >= 20:
            raise ValidationError("User cannot be a member of more than 20 boards.")

        serializer.save(board=board, invited_user=invited_user)

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
        # محدودیت M: چک کردن تعداد اعضا قبل از پذیرش
        if board.members.count() >= 10:
            raise ValidationError("Cannot add more than 10 members to a board.")
        # محدودیت K: چک کردن تعداد عضویت‌ها
        if invitation.invited_user.board_memberships.count() >= 20:
            raise ValidationError("User cannot be a member of more than 20 boards.")
        
        # اضافه کردن کاربر به اعضای برد
        board.members.add(invitation.invited_user)
        serializer.save(status='accepted')