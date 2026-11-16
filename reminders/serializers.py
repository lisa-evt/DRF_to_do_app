from rest_framework import serializers

from .models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    send_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Reminder
        fields = (
            'id', 'email', 'text', 'delay_minutes',
            'created', 'send_at', 'sent_at',
        )
        read_only_fields = ('id', 'created', 'sent_at')
