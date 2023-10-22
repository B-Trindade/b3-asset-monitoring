"""
Serializers for asset APIs.
"""
from rest_framework import serializers

from core.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for assets."""

    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'value']
        read_only_fields = ['id', 'symbol', 'value']
