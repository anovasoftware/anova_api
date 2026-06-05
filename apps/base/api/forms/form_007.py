from apps.static.models import FormField
from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants, status_constants, type_constants
from apps.base.models import UserHotel
from apps.base.utilities.user_utilities import get_user_profile


# user/hotel profile
class Form007APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_007
    form_id = form_constants.USER_HOTEL

    def __init__(self):
        super().__init__()

        self.user_hotels = None

    def load_models(self, request):
        super().load_models(request)

        if self.success:
            self.user_hotels = UserHotel.objects.filter(
                user_id=self.record_id
            )

    def get_data_options(self, field):
        data_options = super().get_data_options(field)

        for data_option in data_options:
            data_option['disabled_flag'] = False

        return data_options

    def get_data_options_selected(self, field: FormField):
        if field.data_source_key == 'SHIPS':
            # data_options_selected = ['A002', 'A004']
            data_options_selected = list(
                self.user_hotels.filter(
                    hotel__type_id=type_constants.HOTEL_CRUISE_SHIP
                ).values_list(
                    'hotel_id', flat=True
                )
            )
        elif field.data_source_key == 'HOTELS':
            data_options_selected = list(
                self.user_hotels.filter(
                    hotel__type_id=type_constants.HOTEL_HOTEL
                ).values_list(
                    'hotel_id', flat=True
                )
            )
        else:
            data_options_selected = super().get_data_options_selected(field)

        return data_options_selected

    def _post(self, request):
        super()._post(request)

        record = self.record
        selected_hotels = record.get('selected_hotels', []) + record.get('selected_ships', [])

        self.user_hotels.exclude(
            hotel_id__in=selected_hotels,
            static_flag='N'
        ).update(
            status_id=status_constants.INACTIVE
        )
        for hotel_id in selected_hotels:
            user_hotel, created = UserHotel.objects.update_or_create(
                user_id=self.record_id,
                hotel_id=hotel_id,
                defaults={
                    'status_id': status_constants.ACTIVE
                }
            )
            print('x')