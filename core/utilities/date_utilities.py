from datetime import datetime, timezone
from django.utils import timezone as dj_timezone  # Alias to avoid confusion

def string_to_datetime(date_str, date_format):
    """
    Convert a date string to a timezone-aware datetime object.
    If the string is 'nan' or empty, it defaults to '2099.12.31' (UTC).
    """
    if date_str in ('nan', ''):
        date_str = '2099.12.31'

    x = date_str.strip().replace('-', '.')

    try:
        if date_format in ('%Y.%m.%d', 'YYYY.MM.DD'):
            dt = datetime.strptime(x, '%Y.%m.%d')
        elif date_format == '%Y%m%d':
            dt = datetime.strptime(x, '%Y%m%d')
        else:
            dt = datetime(1900, 1, 1)

        # Ensure the datetime is timezone-aware
        return dj_timezone.make_aware(dt, timezone.utc) if dj_timezone.is_naive(dt) else dt
    except Exception:
        return dj_timezone.now()  # Default to current time if parsing fails


def beginning_of_day(date_to_convert: datetime = None):
    """
    Return the beginning of the day (00:00:00) in UTC.
    If no date is provided, defaults to today.
    """
    if date_to_convert is None:
        date_to_convert = dj_timezone.now()  # Always timezone-aware

    # Convert to UTC and reset time components
    dt = date_to_convert.astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return dt


def beginning_of_time():
    """
    Returns the beginning of application time as '1900-01-01 00:00:00 UTC'.
    """
    return string_to_datetime('1900.01.01', '%Y.%m.%d')


def end_of_time():
    """
    Returns the end of application time as '2099-12-31 23:59:59 UTC'.
    """
    return string_to_datetime('2099.12.31', '%Y.%m.%d')


def today():
    """
    Returns today's date at 00:00:00 UTC.
    """
    return beginning_of_day()

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
