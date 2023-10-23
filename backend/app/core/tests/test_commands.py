"""
Test custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from core.models import Asset


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""

        # Psycopg2Error -> When Postgres application hasnt started yet
        # OperationalError -> Postgres is ready to accept connections
        #   but dev database has not been created yet.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


@patch('core.management.commands.initialize_db.Command.check')
class DatabaseCommandTests(TestCase):
    """Test commands interacting with db."""

    @classmethod
    def setUpTestData(cls):
        cls.mock_asset = Asset.objects.create(
            symbol='ABCB4.SA',
            value=19.45,
            date=timezone.now(),
        )

    def test_initialize_db_is_successful(self, patched_check):
        """Test assets are created in the database successfuly."""
        patched_check.return_value = True

        call_command('initialize_db')

        self.assertTrue(
            Asset.objects.filter(symbol=self.mock_asset.symbol).exists()
        )
