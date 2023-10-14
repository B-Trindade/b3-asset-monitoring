"""
Serializers for the user API View.
"""

from django.contrib.auth import get_user_model

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
