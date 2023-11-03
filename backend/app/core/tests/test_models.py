"""
Tests for models.
"""
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""

        email = 'test@example.com'  # @example.com is reserved for testing
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        # user.check_password checks password through hashing sys
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""

        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises an error."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """Test creating a superuser."""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'sample123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_creating_asset_successful(self):
        """Tests creating an asset is successful."""
        asset = models.Asset.objects.create(
            symbol='gogl34.sa',
            value=58.23,
            date=timezone.now(),
        )

        self.assertEqual(str(asset), asset.symbol)

    # FIXME
    def test_creating_asset_missing_fields_raises_error(self):
        """Tests creating asset without a symbol raises error."""
        # with self.assertRaises(ValueError):
        #     models.Asset.objects.create(
        #         value=58.23,
        #         date=timezone.now(),
        #     )
        pass

    def test_creating_tunnel_successful(self):
        asset = models.Asset.objects.create(
            symbol='gogl34.sa',
            value=58.23,
            date=timezone.now(),
        )
        user = get_user_model().objects.create_user(
            email='user@example.com',
            password='samplepass123',
        )

        tunnel = models.Tunnel.objects.create(
            userId=user,
            assetId=asset,
            lowerVal=10,
            upperVal=50,
            interval=5,
        )
        expected_str = f"Tunnel for: {asset.symbol} by {user.email}"

        self.assertEqual(str(tunnel), expected_str)
        self.assertEqual(tunnel.userId, user)
        self.assertEqual(tunnel.assetId, asset)
        self.assertEqual(tunnel.lowerVal, 10)
        self.assertEqual(tunnel.upperVal, 50)
        self.assertEqual(tunnel.interval, 5)

    def test_creating_tunnel_invalid_params_raises_error(self):
        pass

    # FIXME DEPRECATED
    # def test_assigning_users_to_asset(self):
    #     """Tests assigning users to an asset is successful."""
    #     user1 = get_user_model().objects.create_user(
    #         'testuser1@example.com',
    #         'samplepass123',
    #     )
    #     user2 = get_user_model().objects.create_user(
    #         'testuser2@example.com',
    #         'samplepass123',
    #     )
    #     asset = models.Asset.objects.create(
    #         symbol='gogl34.sa',
    #         value=58.23,
    #         date=timezone.now(),
    #     )
    #     asset.user.add(user1, user2)

    #     self.assertEqual(user1.email,
    #      asset.user.get(email=user1.email).email)
    #     self.assertEqual(user2.email,
    #      asset.user.get(email=user2.email).email)
