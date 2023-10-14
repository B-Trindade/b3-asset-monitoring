"""
Views for the user API.
"""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


# CreateAPIView is designed to handle POST requests for
# creating objects in the database.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


# ObtainAuthToken uses name and password as auth fields by default
# using our AuthTokenSerializer we make it email and password instead.
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # Makes the view available in browsable API
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
