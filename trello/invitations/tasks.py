from celery import shared_task
from django.core.mail import send_mail
from django.utils.translation import activate, gettext_lazy as _
from django.conf import settings
from .models import Invitation

@shared_task
def send_invitation_email(invitation_id, invited_user_language):
    try:
        invitation = Invitation.objects.get(id=invitation_id)
        board = invitation.board
        invited_user = invitation.invited_user


        activate(invited_user_language)

        subject = _("Invitation to join {board_title}").format(board_title=board.title)
        message = _(
            "Hello {user_name},\n\n"
            "You have been invited to join the board '{board_title}' on Modern Trello.\n"
            "Please log in to accept or reject this invitation.\n\n"
            "Best regards,\nModern Trello Team"
        ).format(user_name=invited_user.name, board_title=board.title)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [invited_user.email],
            fail_silently=False,
        )
    except Invitation.DoesNotExist:
        pass  