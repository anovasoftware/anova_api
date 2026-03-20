from core.api_views.core_api import AuthorizedRecordAPIView
from constants import process_constants
from core.services.scheduler_service import SchedulerService

class AuthorizedJobSchedulerAPIView(AuthorizedRecordAPIView):
    process_id = process_constants.BASE_JOB_SCHEDULER

    PARAM_SPECS = AuthorizedRecordAPIView.PARAM_SPECS + ('recordId', 'action')
    PARAM_OVERRIDES = {
        **getattr(AuthorizedRecordAPIView, 'PARAM_OVERRIDES', {}),
        'recordId': dict(
            required_get=True,
            required_post=True,
        )
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.job_id = None
        self.action = '#'
        self.job_results = []

    def load_request(self, request, *args, **kwargs):
        super().load_request(request)

        if self.success:
            self.job_id = self.record_id

    def _post(self, request):
        scheduler_service = SchedulerService()
        scheduler_service.process(self.job_id, self.action)
        self.job_results = scheduler_service.job_results
        self.data['job_results'] = self.job_results

    # def build_response(self):
    #     response = super().build_response()
    #     response['job_results'] = self.job_results
    #     return response