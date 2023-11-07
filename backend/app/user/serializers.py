"""
Serializers for the user API View.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


MIN_PASSWORD_LENGTH = 8


# ModelSerializers automaitcally validate and save things
# to specific models defined.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        # Specifies model for users
        model = get_user_model()
        # Fields users can change using the API
        fields = ['email', 'password', 'name']
        # Extra metadata for precise control over certain fields
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': MIN_PASSWORD_LENGTH
            }
        }

    # Overwrites the default 'create' ModelSerializer method,
    # which stores the recieved value as is.
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        # Instance = Model instance to be updated
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for logging in the user."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def check_user(self, validated_data):
        """Validates and authenticates the user."""
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        return user


# WARNING: AUTHENTICATION TOKENS DISABLED !!!
# class AuthTokenSerializer(serializers.Serializer):
#     """Serializer for the user auth token."""
#     email = serializers.EmailField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#     )

#     def validate(self, attrs):
#         """Validate and authenticate the user."""
#         email = attrs.get('email')
#         password = attrs.get('password')
#         user = authenticate(
#             request=self.context.get('request'),
#             username=email,
#             password=password,
#         )

#         if not user:
#             msg = _('Unable to authenticate with provided credentials.')
#             raise serializers.ValidationError(msg, code='authorization')

#         attrs['user'] = user
#         return attrs
