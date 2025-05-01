import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a development superuser from environment variables"

    def handle(self, *args, **kwargs):
        user_model = get_user_model()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not user_model.objects.filter().exists():
            user_model.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"✅ Superuser `{email}` created"))
        else:
            self.stdout.write(f"⚠️ Superuser `{email}` already exists.")
