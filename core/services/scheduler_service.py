from datetime import timedelta
from typing import Optional
from django.utils import timezone
from apps.base.models import Job, JobExtension
from constants import status_constants, type_constants, job_constants

from apps.base.utilities.exchange_rate_utilities import  ExchangeRateService
from apps.base.utilities.period_utilities import PeriodService


class SchedulerService:
    def __init__(self):
        self.job: Optional[Job] = None
        self.job_extension: Optional[JobExtension] = None
        self.job_results = []
        self.force_run = False

    def process(self, job_id, action=None):
        jobs = Job.objects.filter(
            status_id=status_constants.ACTIVE,
            type_id=type_constants.BASE_JOB_SCHEDULED
        ).order_by(
            'order_by'
        )
        if job_id != 'ALL':
            jobs = jobs.filter(job_id=job_id)

        self.force_run = (action == 'force')
        for job in jobs:
            self.job = job
            self.job_extension, created = JobExtension.objects.get_or_create(job_id=job.pk)
            self.run_job()

    def run_job(self):
        if self.force_run or self.is_due():
            try:
                self.execute_job()
            except Exception as exc:
                raise exc

    def is_due(self):
        job: Job = self.job
        job_extension: JobExtension = self.job_extension

        now = timezone.now()
        hour = now.hour
        last_run_time = job_extension.last_run_time
        elapsed_time = now - last_run_time
        is_due = False

        if job.frequency_type_id == type_constants.FREQUENCY_HOURLY:
            is_due = elapsed_time >= timedelta(minutes=60)
        if job.frequency_type_id == type_constants.FREQUENCY_DAILY and (6 <= hour < 24):
            is_due = elapsed_time >= timedelta(hours=23)
        if job.frequency_type_id == type_constants.FREQUENCY_WEEKLY:
            if elapsed_time >= timedelta(days=7):
                is_due = True
            else:
                is_monday = now.weekday() == 0
                is_due = is_monday and elapsed_time >= timedelta(days=1)

        return is_due

    def execute_job(self):
        job: Job = self.job

        process_map = {
            job_constants.PERIOD_SERVICE: PeriodService,
            job_constants.EXCHANGE_RATE_SERVICE: ExchangeRateService,
        }

        service_class = process_map.get(job.job_id)
        if not service_class:
            raise ValueError(f'No process defined for job {job.job_id} code={job.code}')

        service = service_class(job)
        service.process()
        self.job_results = service.job_results

        if service.success:
            self.job_extension.last_run_time = timezone.now()
            self.job_extension.save(update_fields=['last_run_time'])


