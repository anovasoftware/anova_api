import logging
from decimal import Decimal
from datetime import date, datetime
from apps.base.models import Log
from apps.static.models import Hotel
from constants import hotel_constants, user_constants, process_constants
from django.db.models import Q

logger = logging.getLogger(__name__)


class LogService:
    @staticmethod
    def _json_safe(value):
        if value is None:
            return None

        if isinstance(value, dict):
            return {k: LogService._json_safe(v) for k, v in value.items()}

        if isinstance(value, list):
            return [LogService._json_safe(v) for v in value]

        if isinstance(value, tuple):
            return [LogService._json_safe(v) for v in value]

        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if isinstance(value, Decimal):
            return str(value)

        return value

    @staticmethod
    def _get_request_data(request):
        try:
            if hasattr(request, 'data'):
                return LogService._json_safe(dict(request.data))
        except Exception:
            pass

        try:
            return LogService._json_safe(request.GET.dict())
        except Exception:
            return None

    @staticmethod
    def _get_response_data(response):
        try:
            return LogService._json_safe(response.data)
        except Exception:
            return None

    @staticmethod
    def log(
            message,
            level='INFO',
            request=None,
            response=None,
            error='',
            process_id='000',
            extra=None,
    ):
        extra = extra or {}
        hotel_id = get_hotel_id(request)

        # 1. Standard Python logging
        if level == 'ERROR':
            logger.error(message, exc_info=error)
        elif level == 'WARNING':
            logger.warning(message)
        elif level == 'DEBUG':
            logger.debug(message)
        else:
            logger.info(message)

        # 2. Database logging
        try:
            user_id = user_constants.NOT_APPLICABLE

            if request and hasattr(request, 'user') and request.user and request.user.is_authenticated:
                user_id = getattr(request.user, 'user_id', user_constants.NOT_APPLICABLE)

            Log.objects.create(
                level=level,
                message=message,
                endpoint=request.path if request else None,
                method=request.method if request else None,
                status_code=getattr(response, "status_code", None),

                process_id=process_id or process_constants.NOT_APPLICABLE,
                user_id=user_id,
                hotel_id=hotel_id,

                request_data=LogService._get_request_data(request) if request else None,
                response_data=LogService._get_response_data(response) if response else None,

                error=str(error) if error else '',
            )
        except Exception as db_error:
            logger.exception(f'Failed to save Log record: {db_error}')

def get_hotel_id(request):
    hotel_id = hotel_constants.NOT_APPLICABLE

    if request:
        hotel_id = request.GET.get('hotelId') or request.GET.get('hotel_id')
    elif hasattr(request, 'data') and isinstance(request.data, dict):
        hotel_id = request.data.get('hotelId') or request.data.get('hotel_id')

    hotel_id = hotel_id or hotel_constants.NOT_APPLICABLE

    # TODO: this is a temporary fix to get the hotel_id from the request
    hotel = Hotel.objects.filter(
        Q(hotel_id=hotel_id) | Q(public_key=hotel_id)).first()

    hotel_id = hotel.hotel_id if hotel else hotel_constants.NOT_APPLICABLE

    return hotel_id