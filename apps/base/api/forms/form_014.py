from apps.static.table_api_views.form_api_views import AuthorizedFormAPIView
from constants import form_constants, process_constants
from apps.static.models import Process
from typing import Optional, Type as TypingType, cast


class Form014APIView(AuthorizedFormAPIView):
    process_id = process_constants.FORM_014
    form_id = form_constants.ROLE_PROCESS

    def __init__(self):
        super().__init__()
        self._role_id = None
        self._process_id = None
        self.process: Optional[Process] = None

    # def load_models(self, request):
    #     super().load_models(request)
    #     print(self.record)
    #     if self.success:
    #         self.process = Process.objects.get(pk=self._process_id)

    def load_record(self):
        super().load_record()

        if self.success:
            self._role_id = self.record.get('role_id')
            self._process_id = self.record.get('process_id')

            self.process = Process.objects.get(pk=self._process_id)

    def is_readonly(self, field, value):
        readonly = super().is_readonly(field, value)

        if readonly:
            pass
        elif field.name == 'can_create' and not self.process.supports_create:
            readonly = True
        elif field.name == 'can_read' and not self.process.supports_read:
            readonly = True
        elif field.name == 'can_update' and not self.process.supports_update:
            readonly = True
        elif field.name == 'can_delete' and not self.process.supports_delete:
            readonly = True

        return readonly
