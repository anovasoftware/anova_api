from apps.res.api_views.guest_api_views import AuthorizedGuestDetailAPIView
from apps.static.models import Status
from constants import process_constants
from apps.res.utilities.guest_utilities import get_guest_state, get_next_status_id


class GuestStatusToggleAPIView(AuthorizedGuestDetailAPIView):
    process_id = process_constants.RES_GUEST_TOGGLE_STATUS
    PARAM_OVERRIDES = {
        **getattr(AuthorizedGuestDetailAPIView, 'PARAM_OVERRIDES', {}),
        # 'hotelId': dict(
        #     required_get=True,
        # ),
    }

    def _post_simple(self, request):
        status_id_old = self.guest.status_id
        status_old: Status = self.guest.status
        state = get_guest_state(self.arrival_date, self.departure_date)
        status_id_new = get_next_status_id(self.guest.status_id, state)
        status_new = Status.objects.get(pk=status_id_new)

        self.data = {
            'guest_id': self.guest.guest_id,
            # 'name': f'{self.guest.person.last_name}/{self.guest.person.first_name}',
            'name': 'Doe/John',
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


