def snake_to_camel(value: str, join_with: str = '_') -> str:
    def camel(part: str) -> str:
        pieces = part.split('_')
        return pieces[0] + ''.join(piece.capitalize() for piece in pieces[1:])

    parts = value.split('__')
    camel_parts = [camel(part) for part in parts]

    if join_with == '_':
        result = camel_parts[0] + ''.join(
            part[0].upper() + part[1:] for part in camel_parts[1:]
        )
    else:
        result = join_with.join(camel_parts)

    return result

def snake_to_camel_list(values: list[str], join_with: str = '_') -> list[str]:
    result = [snake_to_camel(value, join_with=join_with) for value in values]
    return result


# def nest_record(record: dict) -> dict:
#     nested = {}
#
#     for key, value in record.items():
#         parts = key.split('__')
#         current = nested
#
#         for part in parts[:-1]:
#             current = current.setdefault(part, {})
#
#         current[parts[-1]] = value
#
#     result = nested
#     return result

def nest_record(record: dict) -> dict:
    nested = {}

    for key, value in record.items():
        parts = key.split('__')
        current = nested

        for part in parts[:-1]:
            current = current.setdefault(part, {})

        if isinstance(value, dict):
            value = nest_record(value)

        current[parts[-1]] = value

    result = nested
    return result

def flat_record(record: dict, join_with: str = '_') -> dict:
    flat = {}

    def _flatten(prefix: str, value):
        if isinstance(value, dict):
            for key, val in value.items():
                new_prefix = f'{prefix}__{key}' if prefix else key
                _flatten(new_prefix, val)
        else:
            flat[snake_to_camel(prefix, join_with=join_with)] = value

    _flatten('' , record)

    result = flat
    return result


def transform_keys(obj, key_transform_func):
    if isinstance(obj, dict):
        transformed = {
            key_transform_func(key): transform_keys(value, key_transform_func)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        transformed = [transform_keys(item, key_transform_func) for item in obj]
    else:
        transformed = obj

    result = transformed
    return result


# def format_response(obj):
#     if isinstance(obj, dict):
#         formatted = {}
#         for key, value in obj.items():
#             new_key = snake_to_camel(key)
#             formatted[new_key] = format_response(value)
#
#     elif isinstance(obj, list):
#         formatted = []
#         for item in obj:
#             if isinstance(item, dict):
#                 item = nest_record(item)
#             formatted.append(format_response(item))
#
#     else:
#         formatted = obj
#
#     result = formatted
#     return result

# def format_response(obj):
#     if isinstance(obj, dict):
#         obj = nest_record(obj)
#
#         formatted = {}
#         for key, value in obj.items():
#             new_key = snake_to_camel(key)
#             formatted[new_key] = format_response(value)
#
#     elif isinstance(obj, list):
#         formatted = [format_response(item) for item in obj]
#
#     else:
#         formatted = obj
#
#     result = formatted
#     return result
def format_response(obj, shape: str = 'nested', join_with: str = '_'):
    if isinstance(obj, dict):
        if shape == 'nested':
            obj = nest_record(obj)

        formatted = {}

        for key, value in obj.items():
            new_key = snake_to_camel(key)

            if isinstance(value, dict):
                if shape == 'flat':
                    formatted[new_key] = flat_record(value, join_with=join_with)
                else:
                    formatted[new_key] = format_response(value, shape=shape, join_with=join_with)
            else:
                formatted[new_key] = format_response(value, shape=shape, join_with=join_with)

    elif isinstance(obj, list):
        formatted = [
            format_response(item, shape=shape, join_with=join_with)
            for item in obj
        ]

    else:
        formatted = obj

    result = formatted
    return result

# def transform_records(records: list[dict], shape: str = 'nested', join_with: str = '_') -> list[dict]:
# def transform_records(records, shape: str = 'nested', join_with: str = '_'):
#     is_single = isinstance(records, dict)
#     records = [records] if is_single else records
#
#     if shape == 'flat':
#         transformed = [flat_record(record, join_with=join_with) for record in records]
#     elif shape == 'nested':
#         transformed = [nest_record(record) for record in records]
#     else:
#         raise ValueError(f'Unsupported shape: {shape}')
#
#     result = transformed
#     return result
def transform_records(records, shape: str = 'nested', join_with: str = '_'):
    is_single = isinstance(records, dict)
    records_list = [records] if is_single else records

    if shape == 'flat':
        transformed = [flat_record(record, join_with=join_with) for record in records_list]
    else:
    # elif shape == 'nested':
        transformed = [nest_record(record) for record in records_list]
    # else:
    #     raise ValueError(f'Unsupported shape: {shape}')

    result = transformed[0] if is_single else transformed
    return result

# def snake_to_camel(s: str, join_with: str = '__') -> str:
#     def camel(part: str) -> str:
#         pieces = part.split('_')
#         return pieces[0] + ''.join(p.capitalize() for p in pieces[1:])
#
#     parts = s.split('__')
#     camel_parts = [camel(part) for part in parts]
#
#     if join_with == '_':
#         # flatten completely: personFirstName
#         return camel_parts[0] + ''.join(p.capitalize() for p in camel_parts[1:])
#
#     return join_with.join(camel_parts)
#
#
# def snake_to_camel_list(values: list[str], join_with: str = '__') -> list[str]:
#     return [snake_to_camel(value, join_with=join_with) for value in values]
#
#
# def flat_record(record: dict, join_with: str = '__') -> dict:
#     flat = {}
#
#     def _flatten(prefix: str, value):
#         if isinstance(value, dict):
#             for key, val in value.items():
#                 new_prefix = f'{prefix}__{key}' if prefix else key
#                 _flatten(new_prefix, val)
#         else:
#             flat[snake_to_camel(prefix, join_with=join_with)] = value
#
#     _flatten('', record)
#     return flat
#
# def transform_keys(obj, key_transform_func):
#     if isinstance(obj, dict):
#         return {
#             key_transform_func(k): transform_keys(v, key_transform_func)
#             for k, v in obj.items()
#         }
#
#     if isinstance(obj, list):
#         return [transform_keys(item, key_transform_func) for item in obj]
#
#     return obj
#
#
# def format_response(obj, level=0):
#     new_obj = obj
#     if isinstance(obj, dict):
#         new_obj = {}
#         for k, v in obj.items():
#             indent = ' -' * level
#             # print(f'{indent} {k}')
#             new_key = snake_to_camel(k)
#             new_obj[new_key] = format_response(v, level + 1)
#     elif isinstance(obj, list):
#         new_obj = []
#         for item in obj:
#             if isinstance(item, dict):
#                 item = nest_record(item)
#             # print(f'{" -" * level} PROCESSING LIST ELEMENT: {item}')
#             result = format_response(item, level + 1)
#             new_obj.append(result)
#
#     return new_obj
#
#
# def nest_record(record):
#     nested = {}
#     try:
#         for key, value in record.items():
#             # print(f'{key}:{value}')
#             parts = key.split("__")
#             current = nested
#             for part in parts[:-1]:
#                 if part not in current:
#                     current[part] = {}
#                 current = current[part]
#             current[parts[-1]] = value
#     except Exception as e:
#         print(f'{str(e)}')
#     return nested
#
#
# def transform_records(records, shape='nested'):
#     # return [nest_record(record) for record in records]
#     if shape == 'flat':
#         records_adjusted = [flat_record(record) for record in records]
#     else:
#         records_adjusted = [nest_record(record) for record in records]
#
#     return records_adjusted
