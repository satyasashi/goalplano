from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class HealthViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]  # Override default

    def list(self, request):
        return Response({"status": "healthy"})
