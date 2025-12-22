from rest_framework import serializers as s
from drf_spectacular.utils import inline_serializer

MetaSerializer = inline_serializer(
    name='Meta',
    fields={
        'version': s.CharField(help_text='API version (e.g., 03.01.08)'),
        'databaseKey': s.CharField(help_text='Database key (e.g., production)'),
        'parameters': s.DictField(
            help_text='Original request parameters.'
        ),
        'recordCount': s.IntegerField(help_text='Number of records returned'),
    },
)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For may be a comma-separated list of IPs
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# def make_envelope(record_serializer: serializers.Serializer) -> serializers.Serializer:
#     """Reusable response envelope: success/code/message/meta/context/data.records[*]."""
#     return inline_serializer(
#         name='StandardEnvelope',
#         fields={
#             'success': serializers.BooleanField(help_text='Request succeeded'),
#             'code': serializers.CharField(help_text='Status code (e.g., OK, VALIDATION_ERROR)'),
#             'message': serializers.CharField(help_text='Human-readable status'),
#             'meta': serializers.JSONField(help_text='Metadata (version, parameters, recordCount)'),
#             'context': serializers.JSONField(help_text='Context (user, hotel, etc.)'),
#             'data': inline_serializer('Data', {
#                 'records': serializers.ListSerializer(child=record_serializer)
#             }),
#         }
#     )


