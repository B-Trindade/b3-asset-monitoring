"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # Auth system
    BaseUserManager,
    PermissionsMixin,  # Functionality for the permissions & fields
)


class UserManager(BaseUserManager):
    """Manager for users."""

    # extra_fields is responsible for creating fields such as "name",
    #   automatically parsing new values to the model.
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # Encrypting
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Asset(models.Model):
    """Asset model."""
    symbol = models.CharField(max_length=20, unique=True,
                              blank=False, null=False)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return self.symbol


class Tunnel(models.Model):
    """Tunnel model."""
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    assetId = models.ForeignKey(Asset, on_delete=models.CASCADE)
    lowerVal = models.DecimalField(max_digits=10, decimal_places=2)
    upperVal = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.PositiveIntegerField()

    def __str__(self):
        return f"Tunnel for: {self.assetId.symbol} by {self.userId.email}"
