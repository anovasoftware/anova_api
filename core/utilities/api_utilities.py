from rest_framework import serializers as s
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For may be a comma-separated list of IPs
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def make_envelope(record_serializer: serializers.Serializer) -> serializers.Serializer:
    """Reusable response envelope: success/code/message/meta/context/data.records[*]."""
    return inline_serializer(
        name='StandardEnvelope',
        fields={
            'success': serializers.BooleanField(help_text='Request succeeded'),
            'code': serializers.CharField(help_text='Status code (e.g., OK, VALIDATION_ERROR)'),
            'message': serializers.CharField(help_text='Human-readable status'),
            'meta': serializers.JSONField(help_text='Metadata (version, parameters, recordCount)'),
            'context': serializers.JSONField(help_text='Context (user, hotel, etc.)'),
            'data': inline_serializer('Data', {
                'records': serializers.ListSerializer(child=record_serializer)
            }),
        }
    )

def build_record_fields(record_dict):
    fields = {}
    for key, spec in record_dict.items():
        name = spec.get('name', key.replace('__', '_'))
        field_class  = spec.get('type', s.CharField)
        description = spec.get('description', f'Field for {name}')
        fields[name] = field_class (help_text=description, required=False, allow_null=True)
    return fields


def expand_record_dict(record_dict=None):
    record_dict = record_dict or {}

    default_description = "Auto description for {name}"

    for key, val in record_dict.items():
        if 'name' not in val:
            val['name'] = key.replace('__', '_')
        if 'description' not in val:
            val['description'] = default_description.format(name=val['name'])
        if 'type' not in val:
            # # Example: add some custom type logic
            # if 'date' in key:
            #     val['type'] = s.DateTimeField
            # elif 'flag' in key:
            #     val['type'] = s.BooleanField
            # elif key.endswith('_id'):
            #     val['type'] = s.IntegerField
            # else:
                val['type'] = s.CharField

    return record_dict