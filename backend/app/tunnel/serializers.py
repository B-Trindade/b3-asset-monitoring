"""
Serializers for Tunnel API.
"""

from rest_framework import serializers

from core.models import Tunnel


class TunnelSerializer(serializers.ModelSerializer):
    """Serializer for the tunnel model."""

    class Meta:
        model = Tunnel
        fields = '__all__'
