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

