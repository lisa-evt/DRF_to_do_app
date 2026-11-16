from django.contrib import admin

from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """
    Read-only view; 
    reminders are created through the API, which schedules the Celery task.
    """

    list_display = ('email', 'owner', 'delay_minutes', 'created', 'sent_at')
    list_select_related = ('owner',)
    search_fields = ('email', 'owner__username')
    readonly_fields = ('send_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False