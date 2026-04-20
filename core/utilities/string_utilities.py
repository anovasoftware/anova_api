from core.utilities.data_transformation_utilities import snake_to_camel


def mask_string(s):
    if not s:
        return ""
    return s[0] + "#" * (len(s) - 1)


# def snake_to_camel(s):
#     parts = s.split('_')
#     snaked = parts[0] + ''.join(word.capitalize() for word in parts[1:])
#     return snaked


# def field_to_data_path(field_name: str) -> str:
#     parts = field_name.split('__')
#     part0 = snake_to_camel(parts[0])
#     camel_parts = [part0] + [snake_to_camel(p) for p in parts[1:]]
#     data_path = '.'.join(camel_parts)
#     return data_path
