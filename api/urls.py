from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet, ChangingStatusViewSet, ReminderViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tasks', TaskViewSet, basename='tasks')
router.register('changing_status', ChangingStatusViewSet, basename='changing_status')
router.register('reminders', ReminderViewSet, basename='reminders')

urlpatterns = router.urls
