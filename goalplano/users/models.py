# Native imports
from pathlib import Path

from django.conf import settings

# Framework imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# third party imports
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# my imports
from .managers import CustomUserManager
from .services import get_user_directory_thumbnail_path


class User(AbstractUser):
    """
    Default custom user model for goalplano.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    email = models.EmailField(_("Email Address"), unique=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_absolute_url(self):
        """
        Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.email

    class Meta:
        db_table = "User"


class UserDetail:
    """
    Contains the details about the user
    of this application
    """

    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Other"))
    REPUTATION_CHOICES = (("BR", "Bronze"), ("GO", "Gold"), ("DI", "Diamond"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(blank=True, null=True)
    about = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
    )
    occupation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    admires = models.ManyToManyField("public_figures.PublicFigure", blank=True)
    country = CountryField(blank_label="(select country)", blank=True, null=True)
    address = models.CharField(max_length=500, blank=True)
    phone_number = PhoneNumberField(blank=True)

    # privacy and settings
    profile_visibility = models.BooleanField(default=True)
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        blank=True,
        null=True,
    )
    reputation_earned = models.CharField(
        choices=REPUTATION_CHOICES,
        default=REPUTATION_CHOICES[0][0],
        max_length=2,
    )
    profile_score = models.CharField(max_length=10, default=0)

    # Social media links
    twitter_profile_url = models.URLField(blank=True)
    github_profile_url = models.URLField(blank=True)
    instagram_profile_url = models.URLField(blank=True)
    linkedin_profile_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        """Resize and save profile picture thumbnail."""

        if self.profile_picture:
            img = Image.open(self.profile_picture)
            img.thumbnail(settings.IMG_PROF)

            img_thumbnail_path = get_user_directory_thumbnail_path(
                self.user.username,
                self.profile_picture,
            )

            try:
                img.save(img_thumbnail_path)
            except FileNotFoundError:
                user_name = self.user.email.split("@")[0]
                target_dir = Path(settings.MEDIA_ROOT) / user_name / "profile_pics"
                target_dir.mkdir(parents=True, exist_ok=True)
                img.save(img_thumbnail_path)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.email

    class Meta:
        db_table = "UserDetail"
        verbose_name = "UserDetail"
        verbose_name_plural = "UserDetails"
