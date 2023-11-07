"""
Views for the user API.
"""

from rest_framework import (
    generics,
    permissions,
    status,
    # authentication,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from django.contrib.auth import login, logout

from user.validations import validate_email, validade_password
from user.serializers import (
    UserSerializer,
    UserLoginSerializer,
    AuthTokenSerializer,
)


# CreateAPIView is designed to handle POST requests for
# creating objects in the database.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


# !!!-----> CURRENTLY NOT IN USE <-----!!!
# ObtainAuthToken uses name and password as auth fields by default
# using our AuthTokenSerializer we make it email and password instead.
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # Makes the view available in browsable API
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Token Authentication disabled.
    # authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserLoginView(APIView):
    """Log the user in."""
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        data = request.data
        # Custom validation for empty field checks
        assert validate_email(data)
        assert validade_password(data)

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """Log the user out."""

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
