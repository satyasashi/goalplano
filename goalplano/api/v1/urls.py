from rest_framework.routers import DefaultRouter

from .viewsets.health import HealthViewSet

router = DefaultRouter()
router.register("health", HealthViewSet, basename="health")  # Now works!

urlpatterns = router.urls
