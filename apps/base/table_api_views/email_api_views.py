from core.api_views.core_api import AuthorizedAPIView
from django.core.mail import send_mail
from constants import process_constants


class AuthorizedEmailAPIView(AuthorizedAPIView):
    process_id = process_constants.BASE_EMAIL

    def __init__(self):
        super().__init__()

        self.subject = None
        self.body = None
        self.from_address = None
        self.to_address = None

    def load_request(self, request):
        super().load_request(request)

        default_from_address = 'support@anovasoftware.com'

        self.subject = self.get_param('subject', None, required=True)
        self.body = self.get_param('body', 'NO BODY', required=False)
        self.to_address = self.get_param('toAddress', None, required=True)
        self.from_address = self.get_param('fromAddress', default_from_address, required=False)

    def pre_post(self, request):
        super().pre_post(request)

    def _post(self, request):
        try:
            send_mail(
                subject=self.subject,
                message=self.body,
                from_email='support@anovasoftware.com',
                recipient_list=[
                    self.to_address
                ],
                fail_silently=False,
            )
            self.set_message('email sent')
        except Exception as e:
            self.set_message(f'email NOT sent {str(e)}')

