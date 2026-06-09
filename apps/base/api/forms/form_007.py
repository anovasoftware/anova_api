from apps.base.api.forms.form_user_idx import FormUserIdxAPIView
from apps.static.models import FormField
from constants import form_constants, process_constants, status_constants, type_constants
from apps.base.models import UserHotel


# user/hotel profile
class Form007APIView(FormUserIdxAPIView):
    process_id = process_constants.FORM_007
    form_id = form_constants.USER_HOTEL

    def __init__(self):
        super().__init__()

    def get_data_options_selected(self, field: FormField):
        if field.data_source_key == 'SHIPS':
            data_options_selected = list(
                self.user_hotels.filter(
                    hotel__type_id=type_constants.HOTEL_CRUISE_SHIP,
                    status_id=status_constants.ACTIVE
                ).values_list(
                    'hotel_id', flat=True
                )
            )
        elif field.data_source_key == 'HOTELS':
            data_options_selected = list(
                self.user_hotels.filter(
                    hotel__type_id=type_constants.HOTEL_HOTEL,
                    status_id=status_constants.ACTIVE
                ).values_list(
                    'hotel_id', flat=True
                )
            )
        else:
            data_options_selected = super().get_data_options_selected(field)

        return data_options_selected

    def _post(self, request):
        super()._post(request)

        if self.success:
            record = self.record
            selected_hotels = record.get('selected_hotels', []) + record.get('selected_ships', [])

            user_hotels_to_inactivate = self.user_hotels.exclude(
                hotel_id__in=selected_hotels,
            )
            # user_hotels_to_inactivate = user_hotels_to_inactivate.filter(
            #     static_flag='Y'
            # )
            user_hotels_to_inactivate.update(
                status_id=status_constants.INACTIVE
            )
            for hotel_id in selected_hotels:
                user_hotel, created = UserHotel.objects.update_or_create(
                    user_id=self.user_idx,
                    hotel_id=hotel_id,
                    defaults={
                        'status_id': status_constants.ACTIVE
                    }
                )
