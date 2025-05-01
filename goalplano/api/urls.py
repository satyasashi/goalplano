from django.urls import include
from django.urls import path

urlpatterns = [
    path("v1/", include("goalplano.api.v1.urls")),  # Versioned API
]
