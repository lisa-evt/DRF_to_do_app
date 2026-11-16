from functools import partial

from django.db import transaction

from .tasks import send_reminder_email


def schedule_reminder(reminder):
    """Queue the email once the reminder row is committed."""
    transaction.on_commit(
        partial(
            send_reminder_email.apply_async,
            args=(reminder.pk,),
            eta=reminder.send_at,
        )
    )
    