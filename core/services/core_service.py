# core/services.py
from apps.static.models import Status

class CoreService:
    _http_statuses = None  # class-level cache for the queryset

    @classmethod
    @property
    def http_statuses(cls):
        http_classes = cls.get_http_classes()
        if cls._http_statuses is None:
            cls._http_statuses = cls.load_http_statuses()
            for status in cls._http_statuses:
                http_classes[status.status_id] = {
                    'status_id': status.status_id,
                    'code': status.description,
                    'http_status': status.status_code,
                    'success': 200 <= status.status_code < 300
                }
        return http_classes

    @classmethod
    def load_http_statuses(cls):
        if cls._http_statuses is None:
            cls._http_statuses = Status.objects.filter(grouping='HTTP Status')
        return cls._http_statuses

    @classmethod
    def get_http_statuses(cls):
        return cls.load_http_statuses()

    @classmethod
    def get_success(cls, status_id) :
        statuses = cls.get_http_statuses()
        success = False
        try:
            status_code= statuses.get(pk=status_id).status_code
            success = 200 <= status_code < 300
        except Status.DoesNotExist:
            success = False

        return success

    @classmethod
    def refresh_http_statuses(cls):
        cls._http_statuses = Status.objects.filter(grouping='HTTP Status')
