from django.urls import include
from django.urls import path

urlpatterns = [
    path("api/", include("goalplano.api.urls")),  # All API routes
]
