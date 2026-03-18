class JobService:
    def __init__(self, job):
        self.job = job
        self.success = True
        self.message = ''
        self.records_created = 0
        self.records_updated = 0
        self.job_results = {}

    def process(self):
        try:
            self._pre_process()
            if self.success:
                self._process()
                if self.success:
                    self._post_process()
        except Exception as e:
            self.success = False
            self.message = str(e)

        self.job_results['records_created'] = self.records_created
        self.job_results['records_updated'] = self.records_updated
        self.job_results['success'] = self.success
        self.job_results['message'] = self.message


    def _pre_process(self):
        self.job_results = {
            'job_id': self.job.job_id,
            'code': self.job.code,
            'records_created': self.records_created,
            'records_updated': self.records_updated,
            'success': self.success
        }

    def _process(self):
        self.success = False
        self.message = 'Subclasses must implement _process()'

    def _post_process(self):
        pass



