import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .constants import EMAIL_SUBJECT, SEND_MAX_RETRIES
from .models import Reminder

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(OSError,),  # SMTPException and socket errors are OSError subclasses
    retry_backoff=True,
    retry_kwargs={'max_retries': SEND_MAX_RETRIES},
)
def send_reminder_email(reminder_id):
    with transaction.atomic():
        reminder = (
            Reminder.objects.select_for_update()
            .filter(pk=reminder_id, sent_at__isnull=True)
            .first()
        )
        if reminder is None:
            logger.info('Reminder %s was deleted or already sent', reminder_id)
            return
        send_mail(
            subject=EMAIL_SUBJECT,
            message=reminder.text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(reminder.email,),
        )
        reminder.sent_at = timezone.now()
        reminder.save(update_fields=('sent_at',))