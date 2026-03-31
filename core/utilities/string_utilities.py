# def integer_to_char31_OLD(int_value, length):
#     i = length
#     char31 = ''
#     mask = '0123456789BCDFGHJKLMNPQRSTVWXYZ'
#
#     while i >= 1:
#         factor = pow(31, i - 1)
#         position = int(int_value / factor)
#         char31 = char31 + mask[position]
#         int_value = int_value % factor
#         i = i - 1
#
#     char31.zfill(length)
#     return char31

def mask_string(s):
    if not s:
        return ""
    return s[0] + "#" * (len(s) - 1)


def snake_to_camel(s):
    parts = s.split('_')
    snaked = parts[0] + ''.join(word.capitalize() for word in parts[1:])
    return snaked
    # return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def field_to_data_path(field_name: str) -> str:
    parts = field_name.split('__')
    camel_parts = [parts[0]] + [snake_to_camel(p) for p in parts[1:]]
    return '.'.join(camel_parts)
