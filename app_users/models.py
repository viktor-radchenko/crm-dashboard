from email.policy import default
import secrets

from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_registered", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    is_deleted = models.BooleanField("deleted", default=False)
    is_client = models.BooleanField("user_type", default=False)
    is_registered = models.BooleanField("is_registered", default=False)
    confirmation_sent = models.BooleanField("confirmation_sent", null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_img/', default="profile_default.jpeg")
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, related_name="client"
    )

    def generate_uuid():
        return secrets.token_hex(32)

    uuid = models.CharField(max_length=255, default=generate_uuid)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def getAgencyInfo(self):
        if self.is_client:
            agency = self.created_by.agency.first()
        else:
            agency = self.agency.first()
        if agency.logo:
            return f'<img class="agency-logo" src="{agency.logo.url}" alt="agency_logo">'
        if agency.name:
            return f'<div class="sidebar-brand-text mx-3 agency-name">{agency.name.upper()}</div>'
        return '<div class="sidebar-brand-text mx-3">DASHBOARD</div>'

    def __str__(self):
        return self.email


class UserReplication(models.Model):
    new_email = models.EmailField(max_length=255)
    old_email = models.EmailField(max_length=255)
    deleted_on = models.DateTimeField(auto_now_add=True)
    user_uuid = models.CharField(max_length=255)
    original_user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=None, related_name="replicated_user")

    def __str__(self):
        return f"Replication for {self.old_email}"
