from rest_framework.routers import SimpleRouter

from .views import ReminderViewSet

router = SimpleRouter()
router.register('reminders', ReminderViewSet, basename='reminder')

urlpatterns = router.urls