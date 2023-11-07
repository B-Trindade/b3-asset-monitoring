"""
ViewSets for the tunnel API.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from core.models import Tunnel
from tunnel import serializers


class TunnelViewSet(viewsets.ModelViewSet):
    """View set for the tunnel model handlers."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    queryset = Tunnel.objects.all()
    serializer_class = serializers.TunnelSerializer

    def get_queryset(self):
        """Only shows the user the query of tunnels pertaining to them."""
        return self.queryset.filter(userId=self.request.user).order_by('-id')
