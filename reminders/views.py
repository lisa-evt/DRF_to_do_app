from django.db import transaction
from rest_framework import mixins, viewsets

from config.schema import is_schema_generation

from .models import Reminder
from .serializers import ReminderSerializer
from .services import schedule_reminder


class ReminderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """List, create and delete reminders of the current user."""

    serializer_class = ReminderSerializer
    ordering_fields = ('created',)

    def get_queryset(self):
        if is_schema_generation(self):
            return Reminder.objects.none()
        return Reminder.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            reminder = serializer.save(owner=self.request.user)
            schedule_reminder(reminder)
