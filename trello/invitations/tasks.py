"""
Celery task for sending invitation emails.

This module defines a Celery task to send an email notification to a user
when they receive an invitation to join a board.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.utils.translation import activate, gettext_lazy as _
from django.conf import settings
from .models import Invitation

@shared_task
def send_invitation_email(invitation_id, invited_user_language):
    """
    Sends an email to the invited user for a board invitation.

    Activates the user's preferred language for translation, constructs the email
    subject and message, and sends the email. If the invitation does not exist,
    the task silently fails.

    Args:
        invitation_id (int): The ID of the Invitation instance.
        invited_user_language (str): The language code for the invited user's preferred language.

    Raises:
        None: If the invitation is not found, the task silently passes.
    """
    try:
        invitation = Invitation.objects.get(id=invitation_id)
        board = invitation.board
        invited_user = invitation.invited_user

        # Activate the invited user's preferred language for translation
        activate(invited_user_language)

        # Define email subject with translation
        subject = _("Invitation to join {board_title}").format(board_title=board.title)
        
        # Define email message with translation
        message = _(
            "Hello {user_name},\n\n"
            "You have been invited to join the board '{board_title}' on Modern Trello.\n"
            "Please log in to accept or reject this invitation.\n\n"
            "Best regards,\nModern Trello Team"
        ).format(user_name=invited_user.name, board_title=board.title)
        
        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [invited_user.email],
            fail_silently=False,
        )
    except Invitation.DoesNotExist:
        # Silently pass if the invitation is not found
        pass