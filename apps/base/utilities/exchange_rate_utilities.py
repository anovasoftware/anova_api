import requests
from django.utils import timezone
from django.core.cache import cache
from datetime import datetime, time, timedelta

from core.services.job_service import JobService
from apps.static.models import Currency
from apps.base.models import ExchangeRate
from constants import type_constants, status_constants, process_constants
from apps.base.table_api_views.table_exchange_rate_api_views import ExchangeRateAPIView


class ExchangeRateService(JobService):
    def _process(self):
        self.update_last_exchange_rate()

    def update_last_exchange_rate(self):
        url = 'https://open.er-api.com/v6/latest/USD'
        data = {}
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            self.success = False
            self.message = str(e)

        if self.success:
            rates = data.get('rates', {})
            currencies = Currency.objects.filter(
                type_id=type_constants.CURRENCY_REAL,
                status_id=status_constants.ACTIVE
            )
            for currency in currencies:
                code = currency.code
                rate = rates.get(code)
                if rate is None:
                    self.success = False
                    self.message = f'No exchange rate found for {code}'
                    break
                else:
                    exchange_rate, created = ExchangeRate.objects.update_or_create(
                        currency_id=currency.currency_id,
                        type_id=type_constants.EXCHANGE_RATE_LATEST,
                        defaults={
                            'rate': rate,
                            'start_date': timezone.now(),
                        }
                    )
                    if created:
                        self.records_created += 1
                    else:
                        self.records_updated += 1


            cache_key = f'{ExchangeRateAPIView.get_cache_key_pattern()}.{type_constants.EXCHANGE_RATE_LATEST}'
            print(cache_key)
            cache.delete(cache_key)
