from typing import Optional

from core.api_views.table_api_views import PublicTableAPIView
from django.core.cache import cache

from constants import type_constants, process_constants, job_constants
from apps.base.models import JobExtension


class ExchangeRateAPIView(PublicTableAPIView):
    process_id = process_constants.BASE_EXCHANGE_RATE
    PARAM_SPECS = PublicTableAPIView.PARAM_SPECS + ('typeId',)
    PARAM_OVERRIDES = {
        'typeId': dict(
            required_get=True,
            required_post=False,
            allowed=(
                type_constants.EXCHANGE_RATE_LATEST,
            )
        )
    }

    def __init__(self):
        super().__init__()
        self.app_name = 'base'
        self.model_name = 'ExchangeRate'
        # self.job_extension: Optional[JobExtension] = None

    # def load_models(self, request):
    #     super().load_models(request)
    #
    #     self.job_extension = JobExtension.objects.get(job_id=job_constants.EXCHANGE_RATE_SERVICE)

    def get_value_list(self):
        value_list = [
            'currency__currency_id',
            'currency__code',
            'rate'
        ] + super().get_value_list()
        return value_list

    def _get(self, request):
        cache_key = f'exchange_rate_api:type_id:{self.type_id}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            self.data['cached'] = False
            self.data = cached_data
            return
        super()._get(request)

        self.data['cached'] = False
        self.data['home_currency'] = self.home_currency

        job_extension = JobExtension.objects.get(job_id=job_constants.EXCHANGE_RATE_SERVICE)
        job_extension = {
            'job_extension_id': job_extension.job_extension_id,
            'last_run_time': job_extension.last_run_time,
        }

        self.data['job_extension'] = job_extension
        self.data['exchange_rates'] = self.records,

        cache.set(cache_key, self.data, timeout=3600)
