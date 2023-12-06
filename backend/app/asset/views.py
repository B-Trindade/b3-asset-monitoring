"""
Views for the asset APIs.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
# from rest_framework.authentication import TokenAuthentication

from core.models import Asset
from asset import serializers
from core.tasks import get_historical_data


# class AssetViewSet(viewsets.ModelViewSet):
#     """View for manage asset APIs."""
#     serializer_class = serializers.AssetSerializer
#     # query set thats manageable via this viewset
#     queryset = Asset.objects.all()
#     # Auth is needed to use endpoints provided by viewset
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'symbol'

#     def get_queryset(self):
#         """Retrieve assets for authenticated user."""
#         return self.queryset.filter(user=self.request.user).order_by('-id')
    
#     def retrieve(self, request, *args, **kwargs):
#         """Retrieve historical data for a single asset."""
#         instance = self.get_object()
#         print(instance)
#         serializer = self.get_serializer(instance)
#         print(serializer.data)
#         # asset_data = call_command('get_historical_ticker_data', instance)
#         return Response(serializer.data)


class DetailedAssetView(GenericAPIView):
    """View for detailed asset API."""
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    lookup_field = 'symbol'

    def get(self, request, symbol):
        """Return a json response of historical data up to 1 day."""
        try:
            async_result = get_historical_data.delay(symbol)
            json_data = async_result.get()
            # print(json_data)
            return Response(json_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListAssets(ListAPIView):
    """View for list assets API."""
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
