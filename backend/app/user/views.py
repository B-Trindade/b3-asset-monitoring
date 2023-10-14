"""
Views for the user API.
"""

from rest_framework import generics

from user.serializers import UserSerializer


# CreateAPIView is designed to handle POST requests for
# creating objects in the database.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
