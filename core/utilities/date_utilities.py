from datetime import date, datetime, time
from django.utils import timezone


def today():
    return timezone.localdate()


def beginning_of_time():
    return date(1900, 1, 1)


def end_of_time():
    return date(2099, 12, 31)


def string_to_date(date_str, date_format='%Y.%m.%d'):
    if date_str in (None, '', 'nan'):
        return end_of_time()

    x = str(date_str).strip().replace('-', '.')

    try:
        if date_format in ('%Y.%m.%d', 'YYYY.MM.DD'):
            return date.fromisoformat(x.replace('.', '-'))

        elif date_format == '%Y%m%d':
            return datetime.strptime(x, '%Y%m%d').date()

    except (ValueError, TypeError):
        return today()

    return today()


def beginning_of_day(date_to_convert=None):
    if date_to_convert is None:
        date_to_convert = today()

    if isinstance(date_to_convert, datetime):
        date_to_convert = timezone.localtime(date_to_convert).date()

    return timezone.make_aware(
        datetime.combine(date_to_convert, time.min)
    )


def get_date_from_flag(flag):
    if flag == 'today':
        return today()
    elif flag == 'beginning_of_time':
        return beginning_of_time()
    elif flag == 'end_of_time':
        return end_of_time()

    raise ValueError(f'Unknown date flag: {flag}')
# from datetime import datetime, timezone
#
# # from django.utils import timezone
# from django.utils.timezone import make_aware
#
#
# def string_to_datetime(date_str, date_format):
#     # sample '%Y.%m.%d'
#     if date_str in ('nan', ''):
#         date_str = '2099.12.31'
#
#     x = date_str.strip().replace('-', '.')
#
#     try:
#         if date_format in ('%Y.%m.%d', 'YYYY.MM.DD'):
#             # dt = datetime.strptime(date_str.strip(),'%Y.%m.%d').strftime('%Y-%m-%d')
#             dt = make_aware(datetime.strptime(x, '%Y.%m.%d'))
#         elif date_format == '%Y%m%d':
#             dt = make_aware(datetime.strptime(x, '%Y%m%d'))
#         else:
#             dt = make_aware(datetime.datetime(1900, 1, 1))
#     except Exception as e:
#         dt = timezone.now()
#
#     return dt
#
#
# #  return the beginning of the day
# # def beginning_of_day(date_to_convert: datetime = datetime.now()):
# #     dt = datetime(date_to_convert.year, date_to_convert.month, date_to_convert.day, tzinfo=timezone.utc)
# #     # dt.replace(microsecond=1)
# #     # dt = make_aware(dt)
# #     # dt.replace(tzinfo=timezone.utc)
# #     return dt
# def beginning_of_day(date_to_convert: datetime = None):
#     if date_to_convert is None:
#         date_to_convert = datetime.now(timezone.utc)  # Ensures default is UTC-aware
#
#     dt = datetime(date_to_convert.year, date_to_convert.month, date_to_convert.day)
#
#     return make_aware(dt)  # Converts to timezone-aware datetime
#
#
# def beginning_of_time():
#     return string_to_datetime('1900.01.01', '%Y.%m.%d')
#
#
# def end_of_time():
#     return string_to_datetime('2099.12.31', '%Y.%m.%d')
#
#
# def today():
#     dt = beginning_of_day()
#     return dt
#
#
# def today2():
#     dt = datetime.now()
#     # dt = timezone.now()
#     return dt
