from django.utils import timezone
from django.db.models import Min, Max
from apps.res.api_views.res_api_views import AuthorizedResAPIView
from rest_framework.response import Response
from apps.res.models import Guest, GuestRoom
from constants import process_constants, status_constants, constants

record_dict = {
    'guest_id': {'description': 'Guest Identifier', 'example': '311302'},
    'status__description': {'description': 'Guest Status', 'example': 'onboard'},
}

class AuthorizedGuestDetailAPIView(AuthorizedResAPIView):
    process_id = process_constants.RES_GUEST_DETAIL
    PARAM_SPECS = AuthorizedResAPIView.PARAM_SPECS + ('recordId', )
    PARAM_OVERRIDES = {
        'recordId': dict(
            required_get=True,
            required_post=True,
        )
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guest_id = None
        self.guest = None
        self.guest_rooms = None
        self.guest_room = None
        self.app_name = 'res'
        self.model_name = 'Guest'
        self.arrival_date = None
        self.departure_date = None

    def load_request(self, request, *args, **kwargs):
        super().load_request(request)

        if self.success:
            self.guest_id = self.record_id

    def load_models(self, request):
        super().load_models(request)

        try:
            self.guest = Guest.objects.get(pk=self.guest_id)
            person = self.guest.person
            self.context['guest_id'] = self.guest.guest_id
            self.context['guest_name'] = f'{person.last_name}/{person.first_name}'
            self.load_hotel(self.guest.reservation.hotel_id)
            self.guest_rooms = GuestRoom.objects.filter(guest_id=self.guest_id).order_by('arrival_date')

            self.guest_rooms = list(
                self.guest_rooms.select_related('room', 'type', 'status')
            )


            self.guest_room = self.get_current_guest_room()

        except Guest.DoesNotExist:
            message = f'Guest not found: {self.guest_id}'
            self.add_message(message, http_status_id=status_constants.HTTP_NOT_FOUND)

    def get_value_list(self):
        value_list = list(record_dict.keys())

        value_list += super().get_value_list()
        return value_list

    def get_query_filter(self):
        filters = {'guest_id': self.guest_id,}
        return filters

    def post_get(self, request):
        super().post_get(request)

        if self.success:
            self.record['guest_room__arrival_date'] =  self.guest_room.arrival_date.strftime(constants.DATE_FORMAT)
            self.record['guest_room__departure_date'] =  self.guest_room.departure_date.strftime(constants.DATE_FORMAT)

    def get_current_guest_room(self):
        rooms = self.guest_rooms
        current_guest_room = None
        today = timezone.localdate()

        if len(self.guest_rooms) == 1:
            current_guest_room = rooms[0]
            self.arrival_date = current_guest_room.arrival_date
            self.departure_date = current_guest_room.departure_date

        if len(self.guest_rooms) > 1:
            self.arrival_date = rooms[0].arrival_date
            self.departure_date = rooms[-1].departure_date

            if today < rooms[0].arrival_date:
                current_guest_room = rooms[0]
            elif today > rooms[-1].departure_date:
                current_guest_room = rooms[-1]
            else:
                current_guest_room = next(
                    (
                        r for r in reversed(rooms) if r.arrival_date <= today < r.departure_date),
                        None
                    )

        status_id = self.guest.status_id
        if status_id == status_constants.GUEST_ARRIVING and today > self.event_start_date.date():
            print('fixit')
            # self.guest.status = status_constants.GUEST_ONBOARD

        return current_guest_room


def get_guest_dates(guest_rooms):
    dates = guest_rooms.aggregate(
        min_arrival=Min('arrival_date'),
        max_departure=Max('departure_date')
    )
    return dates

    min_arrival = dates['min_arrival']
    max_departure = dates['max_departure']
