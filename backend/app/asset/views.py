"""
Views for the asset APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Asset
from asset import serializers


class AssetViewSet(viewsets.ModelViewSet):
    """View for manage asset APIs."""
    serializer_class = serializers.AssetSerializer
    # query set thats manageable via this viewset
    queryset = Asset.objects.all()
    # Token auth is needed to use endpoints provided by viewset
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve assets for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
