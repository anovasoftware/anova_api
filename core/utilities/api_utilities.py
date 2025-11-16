from core.utilities.string_utilities import snake_to_camel
from rest_framework import serializers as s
from drf_spectacular.utils import inline_serializer
from drf_spectacular.utils import OpenApiParameter
from copy import deepcopy


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

def get_docs_envelope(record_serializer: s.Serializer,  name: str = 'StandardEnvelope') -> s.Serializer:
    data_serializer = inline_serializer(
        name=f'{name}Data',
        fields={
            'records': s.ListSerializer(child=record_serializer),
        },
    )

    envelope_serializer = inline_serializer(
        name=name,
        fields={
            'success': s.BooleanField(help_text='Request succeeded'),
            'code': s.CharField(help_text='Status code (e.g., OK, VALIDATION_ERROR)'),
            'message': s.CharField(help_text='Human-readable status'),
            # 'meta': s.JSONField(help_text='Metadata (version, databaseKey, parameters, recordCount)'),
            'meta': MetaSerializer,
            'context': s.JSONField(help_text='Context (user, hotel, etc.)'),
            'data': data_serializer,
            'errors': s.ListSerializer(
                child=s.JSONField(),
                help_text='List of errors (usually empty).',
            ),
        },
    )

    return envelope_serializer


def get_record_fields(record_dict):
    fields = {}
    for key, spec in record_dict.items():
        name = spec.get('name', key.replace('__', '_'))
        description = spec.get('description', f'Field for {name}')
        field_class  = spec.get('type', s.CharField)
        example = spec.get('example', f'Field for {name}')
        fields[name] = field_class (
            help_text=description,
            required=False,
            allow_null=False,
        )
    return fields


def expand_record_dict(record_dict=None):
    record_dict = record_dict or {}

    default_description = "Auto description for {name}"

    for key, val in record_dict.items():
        if 'name' not in val:
            name = key.replace('__', '_')
            name = snake_to_camel(name)
            val['name'] = name

        if 'description' not in val:
            val['description'] = default_description.format(name=val['name'])
        if 'type' not in val:
            val['type'] = s.CharField
        if key.endswith('_date'):
            val['type'] = s.DateTimeField

    return record_dict


from drf_spectacular.types import OpenApiTypes


def get_parameters_from_open_api_parameters(open_api_params, overrides=None) -> dict:
    overrides = overrides or {}
    params = {}

    for p in open_api_params:
        # Allow explicit overrides per parameter name
        if p.name in overrides:
            params[p.name] = overrides[p.name]
            continue

        t = p.type  # this is an OpenApiTypes sentinel, e.g. OpenApiTypes.STR

        if t in (OpenApiTypes.STR, OpenApiTypes.UUID, OpenApiTypes.EMAIL):
            params[p.name] = "string"
        elif t in (OpenApiTypes.INT, OpenApiTypes.NUMBER):
            params[p.name] = 0
        elif t is OpenApiTypes.BOOL:
            params[p.name] = True
        else:
            # fallback for anything else (objects, arrays, unknowns)
            params[p.name] = None

    return params


def get_docs_record_example(record_dict: dict) -> dict:
    example = {}

    for key, meta in record_dict.items():
        example[key] = meta.get('example', None)

    return example


def get_docs_envelope_example(
        context: dict,
        records: list[dict],
        parameters: dict | None = None,
        errors: list[dict] | None = None,
) -> dict:
    parameters = parameters or {}
    errors = errors or []

    return {
        "success": True,
        "code": "OK",
        "message": "Request completed successfully",
        "meta": {
            "version": '00.00.00',
            "databaseKey": 'production',
            "parameters": deepcopy(parameters),
        },
        "context": context,
        "data": {
            "recordCount": 1,
            "records": deepcopy(records),
        },
        "errors": deepcopy(errors),
    }
