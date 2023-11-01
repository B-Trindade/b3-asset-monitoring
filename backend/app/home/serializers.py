"""
Serializers for the frontend app.
"""

from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """Register form serializer."""

    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=40,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    name = serializers.CharField(
        style={'placeholder': 'Name', 'autofocus': True}
    )


class LoginSerializer(serializers.Serializer):
    """Login form serializer."""

    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=40,
        style={'placehold': 'Password', 'input_type': 'password'}
    )
