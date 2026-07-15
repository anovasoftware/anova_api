from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants


class Form015APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_015
    form_id = form_constants.COMPANY_TRAVEL_AGENCY

    def __init__(self):
        super().__init__()

    def load_record(self):
        super().load_record()

        if self.success:
            pass

    def is_readonly(self, field, value):
        readonly = super().is_readonly(field, value)

        # if readonly:
        #     pass
        # elif field.name == 'can_create' and not self.process.supports_create:
        #     readonly = True
        # elif field.name == 'can_read' and not self.process.supports_read:
        #     readonly = True
        # elif field.name == 'can_update' and not self.process.supports_update:
        #     readonly = True
        # elif field.name == 'can_delete' and not self.process.supports_delete:
        #     readonly = True

        return readonly
