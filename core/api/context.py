from rest_framework.permissions import IsAuthenticated
from core.api_views.core_api import CoreAPIView
from apps.base.utilities.user_utilities import get_user_profile
from constants import process_constants, status_constants
from apps.res.models import HotelExtension
from typing import Optional, Type as TypingType, cast


class ContextAPIView(CoreAPIView):
    permission_classes = [IsAuthenticated]
    process_id = process_constants.CORE_CONTEXT
    PARAM_OVERRIDES = {
        'hotelId': dict(
            required_get=True,
        )
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hotel_extension: Optional[HotelExtension] = None

    def load_models(self, request):
        super().load_models(request)

        self.hotel_extension = HotelExtension.objects.filter(hotel_id=self.hotel_id).first()
        if not self.hotel_extension:
            self.add_message('hotel extension not found', http_status_id=status_constants.HTTP_NOT_FOUND)

    def _get(self, request):
        self.data['hotel_context'] = {
            'hotel_id': self.hotel.hotel_id,
            'current_event__event_id': self.hotel_extension.current_event.event_id,
            'current_event__code': self.hotel_extension.current_event.code,
            # 'current_event' = {
            #     'code': self.hotel_extension.current_event.code,
            # }

        }
