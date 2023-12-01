"""
Shared tasks for celery beat.
"""

from celery import shared_task
from celery.utils.log import get_task_logger

from django.utils import timezone
from django.core.management import call_command


logger = get_task_logger(__name__)


@shared_task
def sample_task():
    """Test logging to console."""
    logger.info("The sample task has ran.")


@shared_task
def update_db_task():
    """Task for updating Assets on db."""

    # Evokes django admin command for updating db
    call_command('initialize_db')


@shared_task
def check_tunnel_thresholds_task():
    """Task for checking if current ticker value crosses thresholds"""
    from .models import Tunnel
    now = timezone.now()

    for tunnel in Tunnel.objects.all():
        if (now - tunnel.lastChecked) >= tunnel.interval:
            if tunnel.assetId.value > tunnel.upperVal:
                pass  # TODO send email
            if tunnel.assetId.value < tunnel.lowerVal:
                pass  # TODO send email
            tunnel.save()  # Will automatically update lastChecked
