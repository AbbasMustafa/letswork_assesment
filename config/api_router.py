from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from event_management.events.views import EventViewSet, AttendeeViewSet
from event_management.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("events", EventViewSet, basename="events")
router.register("events", AttendeeViewSet, basename="attendees")

app_name = "api"
urlpatterns = router.urls
