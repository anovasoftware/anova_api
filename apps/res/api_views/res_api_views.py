from core.api_views.core_api import CoreAPIView, AuthorizedAPIView
from core.api_views.table_api_views import AuthorizedTableAPIView
from apps.static.models import Hotel
from apps.res.models import HotelExtension, Event
from constants import status_constants
from typing import Optional, Type as TypingType, cast


class ResCoreAPIView(CoreAPIView):
    PARAM_NAMES = AuthorizedTableAPIView.PARAM_NAMES  + ('eventId',)
    PARAM_OVERRIDES = {
        **getattr(AuthorizedTableAPIView, 'PARAM_OVERRIDES', {}),
        'hotelId': dict(
            required_get=True,
        ),

    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hotel_id = None
        self.hotel: Optional[Hotel] = None
        self.hotel_extension: Optional[HotelExtension] = None
        self.event_start_date = None
        self.event_end_date = None

        self.event_id = None
        self.event: Optional[Event] = None

        self.currency_id = None
        self.rate_type_id = None

    def load_models(self, request):
        super().load_models(request)

        if self.success:
            self.load_hotel(self.hotel_id)

            if self.event_id:
                self.load_event()

    def load_hotel(self, hotel_id=None):
        self.hotel_id = hotel_id

        user_hotels = self.user.userhotels.filter(
            hotel_id=self.hotel_id,
            effective_status_id=status_constants.EFFECTIVE_STATUS_CURRENT
        )
        if not user_hotels.exists():
            message = f'access denied to hotel_id: {self.hotel_id}'
            self.set_message(message, http_status_id=status_constants.HTTP_ACCESS_DENIED)
        else:
            self.hotel = Hotel.objects.get(pk=self.hotel_id)
            self.hotel_extension = HotelExtension.objects.filter(hotel_id=self.hotel_id).first()
            self.context['hotel'] = self.hotel.description

            if self.hotel_extension:
                event = self.hotel_extension.current_event

                if event is not None:
                    self.event_start_date = event.event_start_date
                    self.event_end_date = event.event_end_date

                # event = getattr(self.hotel_extension, 'current_event', None)
                    self.context['current_event'] = {
                        'code': event.code,
                        'start_date': self.event_start_date.strftime('%Y-%m-%d'),
                        'end_date': self.event_end_date.strftime('%Y-%m-%d')
                    }

    def load_event(self):
        event = Event.objects.filter(pk=self.event_id).first()

        if not event:
            self.add_message(f'Invalid event id: {self.event_id}', status_constants.HTTP_BAD_REQUEST)
        else:
            self.event = event


class AuthorizedResAPIView(AuthorizedAPIView, ResCoreAPIView):
    pass


class AuthorizedResTableAPIView(AuthorizedTableAPIView, ResCoreAPIView):
    PARAM_NAMES = ResCoreAPIView.PARAM_NAMES  # + ('',)

    PARAM_OVERRIDES = {
        **getattr(AuthorizedTableAPIView, 'PARAM_OVERRIDES', {}),
        'hotelId': dict(
            required_get=True,
            required_post=True,
            required_patch=True,
        ),

    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

