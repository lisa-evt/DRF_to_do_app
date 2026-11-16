from datetime import timedelta

from django.conf import settings

MIN_DELAY_MINUTES = 1
MAX_DELAY_MINUTES = settings.REMINDER_MAX_DELAY // timedelta(minutes=1)
TEXT_MAX_LENGTH = 1000
SEND_MAX_RETRIES = 3
EMAIL_SUBJECT = 'Reminder'
