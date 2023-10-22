"""
Django command to initialize the db with most recent B3 values.
"""
import yahooquery as yq
from b3symbols import symbols

import pandas as pd

from core.models import Asset
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to initialize the database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Fetching latest data...')
        df = self.__get_all_tickers()

        entries = []
        for e in df.T.to_dict().values():
            entries.append(Asset(**e))
        Asset.objects.bulk_create(
            entries,
            update_conflicts=True,
            unique_fields=['symbol'],
            update_fields=['date', 'value'],
        )

    def __get_all_tickers(self):
        """Uses Yahoo Query to fetch ticker information."""

        # YahooQuery utilizes the '.SA' termination for B3 assets
        tickers = []
        for symbol in symbols:
            tickers.append(symbol + '.SA')

        # Ticker objects are used for fetching Yahoo Finance data
        tickers = yq.Ticker(tickers)

        # Gets most recent data for each ticker
        df = tickers.history(period='1d', interval='1m')
        df = df.reset_index(level=['symbol', 'date'])
        df = df[['symbol', 'date', 'close']].groupby('symbol').tail(1)
        df['date'] = df['date'].map(lambda x: pd.to_datetime(x))
        return df
