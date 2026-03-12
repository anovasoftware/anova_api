from django.utils import timezone
from django.db.models import Min, Max
from apps.res.api_views.res_api_views import AuthorizedResAPIView
from rest_framework.response import Response
from apps.static.models import Status
from apps.res.models import Guest, GuestRoom
from constants import process_constants, status_constants, constants
from apps.res.utilities.guest_utilities import get_guest_adjusted, get_guest_state, get_next_status_id

record_dict = {
    'guest_id': {'description': 'Guest Identifier', 'example': '311302'},
    'person__first_name': {'description': 'First name', 'example': 'John'},
    'person__last_name': {'description': 'Last name', 'example': 'Doe'},
    'person__salutation': {'description': 'Salutation', 'example': 'Mr'},
    'person__birth_date': {'description': 'Birth date', 'example': '1990-01-01'},
    'person__email': {'description': 'Email', 'example': ''},
    'reservation__reservation_id': {'description': 'Reservation ID', 'example': '0000F8'},
    'reservation__hotel_id': {'description': 'Hotel ID', 'example': '000001'},
    'status_id': {'description': 'Guest Status ID', 'example': '1'},
    'status__description': {'description': 'Guest Status', 'example': 'onboard'},

}

class AuthorizedGuestDetailAPIView(AuthorizedResAPIView):
    process_id = process_constants.RES_GUEST_DETAIL
    PARAM_SPECS = AuthorizedResAPIView.PARAM_SPECS + ('recordId', )
    PARAM_OVERRIDES = {
        **getattr(AuthorizedResAPIView, 'PARAM_OVERRIDES', {}),
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
            # self.context['guest_id'] = self.guest.guest_id
            # self.context['guest_name'] = f'{person.last_name}/{person.first_name}'
            self.load_hotel(self.guest.reservation.hotel_id)
            self.guest_rooms = GuestRoom.objects.filter(guest_id=self.guest_id).order_by('arrival_date')

            self.guest_rooms = list(
                self.guest_rooms.select_related('room', 'type', 'status')
            )
            self.guest_room = self.get_current_guest_room()
            self.guest = get_guest_adjusted(self.guest, self.arrival_date, self.departure_date)

            # self.context['guest'] = {
            #     'guest_id': self.guest.guest_id,
            #     'name': f'{person.last_name}/{person.first_name}',
            #     'status_id': self.guest.status_id,
            #     'status__code': self.guest.status.code,
            # }


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

        return current_guest_room


class AuthorizedGuestDetailToggleStatusAPIView(AuthorizedGuestDetailAPIView):
    process_id = process_constants.RES_GUEST_TOGGLE_STATUS
    PARAM_OVERRIDES = {
        **getattr(AuthorizedGuestDetailAPIView, 'PARAM_OVERRIDES', {}),
        # 'postingType': dict(
        #     required_get=False,
        #     required_post=False,
        #     default='simple',
        # )
    }


    def _post(self, request):
        super()._post(request)

        if self.success:
            status_id_old = self.guest.status_id
            status_old:Status = self.guest.status
            state = get_guest_state(self.arrival_date, self.departure_date)
            status_id_new = get_next_status_id(self.guest.status_id, state)
            status_new = Status.objects.get(pk=status_id_new)

            self.data = {
                'changed': status_old.status_id != status_new.status_id,
                'status_id_old': status_old.status_id,
                'status_code_old': status_old.code,
                'status_id_new': status_new.status_id,
                'status_code_new': status_new.code,
            }
            if status_old.status_id == status_new.status_id:
                self.set_message(f'guest status unchanged: {status_old.code}')
            else:
                self.guest.status_id = status_id_new
                self.guest.save()
                self.add_message(f'Guest status changed from {status_old.code} to {status_new.code}')


