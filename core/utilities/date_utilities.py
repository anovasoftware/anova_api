from datetime import datetime

from django.utils import timezone
from django.utils.timezone import make_aware


def string_to_datetime(date_str, date_format):
    # sample '%Y.%m.%d'
    if date_str in ('nan', ''):
        date_str = '2099.12.31'

    x = date_str.strip().replace('-', '.')

    try:
        if date_format in ('%Y.%m.%d', 'YYYY.MM.DD'):
            # dt = datetime.strptime(date_str.strip(),'%Y.%m.%d').strftime('%Y-%m-%d')
            dt = make_aware(datetime.strptime(x, '%Y.%m.%d'))
        elif date_format == '%Y%m%d':
            dt = make_aware(datetime.strptime(x, '%Y%m%d'))
        else:
            dt = make_aware(datetime.datetime(1900, 1, 1))
    except Exception as e:
        dt = timezone.now()

    return dt


#  return the beginning of the day
def beginning_of_day(date_to_convert: datetime = datetime.now()):
    dt = datetime(date_to_convert.year, date_to_convert.month, date_to_convert.day, tzinfo=timezone.utc)
    # dt.replace(microsecond=1)
    # dt = make_aware(dt)
    # dt.replace(tzinfo=timezone.utc)
    return dt


def beginning_of_time():
    return string_to_datetime('1900.01.01', '%Y.%m.%d')


def end_of_time():
    return string_to_datetime('2099.12.31', '%Y.%m.%d')


def today():
    dt = beginning_of_day()
    return dt


def today2():
    dt = datetime.now()
    # dt = timezone.now()
    return dt
