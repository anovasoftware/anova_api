from django.utils import timezone

from apps.res.models import Guest
from constants import status_constants


def get_guest_adjusted(guest: Guest, guest_arrival_date, guest_departure_date):
    today = timezone.localdate()
    status = guest.status

    status_id_old = status.status_id
    status_id_new = status.status_id
    if status.status_id == status_constants.GUEST_ARRIVING and today > guest_arrival_date.date():
        status_id_new = status_constants.GUEST_NEVER_ARRIVED

    if today > guest_departure_date.date() and status.group1 == 1:
        status_id_new = status_constants.GUEST_DISEMBARKED

    if status_id_old != status_id_new:
        guest.status_id = status_id_new
        guest.save()

    return guest


def save_guest_activity(guest: Guest, status_id_old, status_id_new):
    pass


def get_guest_state(arrival_datetime, departure_datetime):
    today = timezone.localdate()
    arrival = arrival_datetime.date()
    departure = departure_datetime.date()

    if today < arrival:
        state = 'pre-arrival'
    elif today == arrival:
        state = 'arrival-day'
    elif today == departure:
        state = 'departure-day'
    elif today > departure:
        state = 'post-departure'
    else:
        state = 'active'

    return state


def get_next_status_id(status_id, state):
    new_status_id = status_id
    mapping = {
        status_constants.GUEST_ARRIVING: {
            'pre-arrival-day': status_constants.GUEST_ARRIVING,
            'arrival-day': status_constants.GUEST_ONBOARD,
            'active': status_constants.GUEST_ONBOARD,
            'departure-day': status_constants.GUEST_DISEMBARKED,
            'post-departure': status_constants.GUEST_DISEMBARKED,
        },
        status_constants.GUEST_ONBOARD: {
            'pre-arrival-day': status_constants.GUEST_ARRIVING,
            'arrival-day': status_constants.GUEST_ASHORE,
            'active': status_constants.GUEST_ASHORE,
            'departure-day': status_constants.GUEST_DISEMBARKED,
            'post-departure': status_constants.GUEST_DISEMBARKED,
        },
        status_constants.GUEST_ASHORE: {
            'pre-arrival-day': status_constants.GUEST_ARRIVING,
            'arrival-day': status_constants.GUEST_ONBOARD,
            'active': status_constants.GUEST_ONBOARD,
            'departure-day': status_constants.GUEST_ONBOARD,
            'post-departure': status_constants.GUEST_DISEMBARKED,
        },

    }

    if status_id in mapping:
        state_mapping = mapping[status_id]
        if state in state_mapping:
            new_status_id = state_mapping[state]

    return new_status_id
