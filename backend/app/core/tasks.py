"""
Shared tasks for celery beat.
"""

from celery import shared_task
from celery.utils.log import get_task_logger

from django.utils import timezone
from django.core.management import call_command
from django.core.mail import send_mail
from app import settings

from datetime import timedelta


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
        if (now - tunnel.lastChecked) >= timedelta(minutes=tunnel.interval):
            logger.info(f"Checking {tunnel.assetId} for {tunnel.userId}.")
            if tunnel.assetId.value > tunnel.upperVal:
                send_mail_task.delay(
                    user=tunnel.userId.email,
                    username=tunnel.userId.name,
                    ticker=tunnel.assetId.symbol,
                    action='Selling',
                    curr_value=tunnel.assetId.value,
                    set_value=tunnel.upperVal
                )
            if tunnel.assetId.value < tunnel.lowerVal:
                send_mail_task.delay(
                    user=tunnel.userId.email,
                    username=tunnel.userId.name,
                    ticker=tunnel.assetId.symbol,
                    action='Buying',
                    curr_value=tunnel.assetId.value,
                    set_value=tunnel.lowerVal
                )
            tunnel.save()  # Will automatically update lastChecked


@shared_task
def send_mail_task(user, username, ticker, action, curr_value, set_value):
    """Task for sending notification emails."""

    receiver = user
    mail_sbj = f"B3 Notifier: {action} {ticker} is recommended!"
    msg = f"""
        Hello, {username}!

        Your conditions for {action} {ticker} have been met.
        {ticker}'s set threshold of R$ {set_value} has been crossed.
        Lastest market value is: R$ {curr_value}!

        {action} is advised!
    """

    logger.info(f"Sending email to {user}.")
    send_mail(
        subject=mail_sbj,
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[receiver],
        fail_silently=True,
    )


@shared_task
def get_historical_data(ticker):
    """Task for fetching historical data given a ticker symbol."""
    import yahooquery as yq
    import pandas as pd

    logger.info(f'Fetching data for {ticker}...')

    # Ticker objects used for fetching Yahoo Finance data
    ticker_data = yq.Ticker(ticker)

    df_ticker_data = ticker_data.history(period='1d', interval='5m')
    df_ticker_data = df_ticker_data.reset_index(level=['symbol', 'date'])
    df_ticker_data['date'] = df_ticker_data['date'].map(lambda x: pd.to_datetime(x))

    logger.info(f'{ticker} data retrieved.')
    return df_ticker_data.to_json(orient='records')
