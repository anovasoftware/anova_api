from apps.base.api.forms.form_user_idx import FormUserIdxAPIView
from apps.static.models import FormField
from constants import form_constants, process_constants, status_constants, type_constants, client_constants, \
    hotel_constants
from apps.base.models import UserRole
from core.utilities.date_utilities import end_of_time, today


class Form008APIView(FormUserIdxAPIView):
    PARAM_OVERRIDES = {
        **FormUserIdxAPIView.PARAM_OVERRIDES,
        'typeId': dict(
            required_get=True,
            required_post=True,
        ),
    }

    process_id = process_constants.FORM_008
    form_id = form_constants.USER_ROLE

    def __init__(self):
        super().__init__()

    def load_request(self, request, *args, **kwargs):
        super().load_request(request, *args, **kwargs )

    def load_models(self, request):
        super().load_models(request)

    def get_data_options_selected(self, field: FormField):
        client_id = self.client_id if self.type_id == type_constants.ROLE_CLIENT else client_constants.NOT_APPLICABLE
        hotel_id = self.hotel_id if self.type_id == type_constants.ROLE_HOTEL else hotel_constants.NOT_APPLICABLE

        if field.data_source_key == 'ROLES':
            user_roles = self.user_roles.filter(
                status_id=status_constants.ACTIVE,
                role__type_id=self.type_id,
                effective_status_id=status_constants.EFFECTIVE_STATUS_CURRENT,
                client_id=client_id,
                hotel_id=hotel_id,
            )

            data_options_selected = list(
                user_roles.values_list('role_id', flat=True)
            )
        else:
            data_options_selected = super().get_data_options_selected(field)

        return data_options_selected

    def _patch(self, request, *args, **kwargs):
        super()._patch(request, *args, **kwargs)
        self.process_selected_roles()

    def _post(self, request):
        super()._post(request)
        self.process_selected_roles()

    def process_selected_roles(self):
        client_id = self.client_id if self.type_id == type_constants.ROLE_CLIENT else client_constants.NOT_APPLICABLE
        hotel_id = self.hotel_id if self.type_id == type_constants.ROLE_HOTEL else hotel_constants.NOT_APPLICABLE
        record = self.record

        selected_roles = record.get('selected_roles', [])

        user_roles_to_inactivate = self.user_roles.exclude(
            role_id__in=selected_roles,
        )
        user_roles_to_inactivate = user_roles_to_inactivate.filter(
            static_flag='N',
            role__type_id=self.type_id,
            client_id=client_id,
            hotel_id=hotel_id,
        )

        user_roles_to_inactivate.update(
            status_id=status_constants.INACTIVE,
            end_date=today(),
            effective_status_id=status_constants.EFFECTIVE_STATUS_EXPIRED
        )
        for role_id in selected_roles:
            user_role, created = UserRole.objects.update_or_create(
                user_id=self.user_idx,
                role_id=role_id,
                client_id=client_id,
                hotel_id=hotel_id,
                defaults={
                    'status_id': status_constants.ACTIVE,
                    'end_date': end_of_time(),
                    'effective_status_id': status_constants.EFFECTIVE_STATUS_CURRENT,
                }
            )
