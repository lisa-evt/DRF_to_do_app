from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import MAX_DELAY_MINUTES, MIN_DELAY_MINUTES, TEXT_MAX_LENGTH


class Reminder(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reminders',
    )
    email = models.EmailField()
    text = models.CharField(max_length=TEXT_MAX_LENGTH)
    delay_minutes = models.PositiveIntegerField(
        validators=(
            MinValueValidator(MIN_DELAY_MINUTES),
            MaxValueValidator(MAX_DELAY_MINUTES),
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ('-created', '-id')

    def __str__(self):
        return f'Reminder to {self.email} in {self.delay_minutes} min'

    @property
    def send_at(self):
        return self.created + timedelta(minutes=self.delay_minutes)
