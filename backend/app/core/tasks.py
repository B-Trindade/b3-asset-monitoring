from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command


logger = get_task_logger(__name__)


@shared_task
def sample_task():
    """Test logging to console."""
    logger.info("The sample task has ran.")


@shared_task
def update_db_task():
    """Task for updating Assets on db."""

    # Evokes
    call_command('initialize_db')
