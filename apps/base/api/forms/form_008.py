from apps.base.api.forms.form_user_idx import FormUserIdxAPIView
from apps.static.models import FormField
from constants import form_constants, process_constants, status_constants, type_constants
from apps.base.models import UserRole


class Form008APIView(FormUserIdxAPIView):
    process_id = process_constants.FORM_008
    form_id = form_constants.USER_ROLE

    def __init__(self):
        super().__init__()

    def load_models(self, request):
        super().load_models(request)

    def get_data_options_selected(self, field: FormField):
        if field.data_source_key == 'ROLES':
            data_options_selected = list(
                self.user_roles.filter(
                    status_id=status_constants.ACTIVE,
                    role__type_id=self.type_id,
                    # hotel__type_id=type_constants.HOTEL_CRUISE_SHIP
                # ).exclude(
                #     role__type_id=type_constants.NOT_APPLICABLE
                ).values_list(
                    'role_id', flat=True
                )
            )
        else:
            data_options_selected = super().get_data_options_selected(field)

        return data_options_selected

    def _post(self, request):
        super()._post(request)

        record = self.record
        selected_roles = record.get('selected_roles', [])

        user_roles_to_inactivate = self.user_roles.exclude(
            role_id__in=selected_roles
        )
        user_roles_to_inactivate = user_roles_to_inactivate.filter(
            static_flag='N'
        )
        user_roles_to_inactivate.update(
            status_id=status_constants.INACTIVE
        )
        for role_id in selected_roles:
            user_role, created = UserRole.objects.update_or_create(
                user_id=self.user_idx,
                role_id=role_id,
                defaults={
                    'status_id': status_constants.ACTIVE
                }
            )
