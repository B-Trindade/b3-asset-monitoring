"""
Tests for asset APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Asset

# from asset.serializers import AssetSerializer


ASSETS_URL = reverse('asset:asset-list')


def create_asset(symbol: str, users, **params):
    """Create and return a sample asset."""
    defaults = {
        'symbol': symbol,
        'value': 32.05,
        'date': timezone.now()
    }
    defaults.update(params)

    asset = Asset.objects.create(**defaults)
    for user in users:
        asset.user.add(user)
    return asset


class PublicAssetAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    # TODO UPDATE TEST
    def test_auth_required(self):
        """Tests auth is required to call API."""
        res = self.client.get(ASSETS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAssetAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            'user1@example.com',
            'samplepass123',
        )
        self.user2 = get_user_model().objects.create_user(
            'user2@example.com',
            'samplepass123',
        )
        self.client.force_authenticate(self.user1)

    # FIXME TODO UPDATE ACCORDING TO NEW ASSET MODEL FIELDS
    # def test_retrieve_assets(self):
    #     """Test retrieving the list of assets."""
    #     create_asset(symbol='sampl3.sa', users=[self.user1])
    #     create_asset(symbol='gogl34.sa', users=[self.user1, self.user2])

    #     res = self.client.get(ASSETS_URL)

    #     assets = Asset.objects.all().order_by('-id')
    #     serializer = AssetSerializer(assets, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    # FIXME TODO UPDATE ACCORDING TO NEW ASSET MODEL FIELDS
    # def test_asset_list_limited_to_user(self):
    #     """Test list of assets associated to authenticated user."""
    #     create_asset(symbol='gogl34.sa', users=[self.user1])
    #     create_asset(symbol='sampl3.sa', users=[self.user1, self.user2])
    #     create_asset(symbol='sampl4.sa', users=[self.user2])

    #     res = self.client.get(ASSETS_URL)

    #     assets = Asset.objects.filter(user=self.user1).order_by('-id')
    #     serializer = AssetSerializer(assets, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
