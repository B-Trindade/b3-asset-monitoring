"""
Views for the asset APIs.
"""

from rest_framework import viewsets  # , views
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
# from rest_framework.authentication import TokenAuthentication

from core.models import Asset
from asset import serializers


# class AssetView(views.ListAPIView):
#     """View for listing assets."""


class AssetViewSet(viewsets.ModelViewSet):
    """View for manage asset APIs."""
    serializer_class = serializers.AssetSerializer
    # query set thats manageable via this viewset
    queryset = Asset.objects.all()
    # Auth is needed to use endpoints provided by viewset
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve assets for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')


class ListAssets(ListAPIView):
    """View for list assets API."""
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
