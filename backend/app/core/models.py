"""
Database models.
"""

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

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encrypting
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
