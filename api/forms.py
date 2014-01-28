from rest_framework.fields import DateTimeField


def get_timezone_format():
    import time

    if time.daylight:
        offsetHour = -time.altzone / 3600
    else:
        offsetHour = -time.timezone / 3600
    return '%Y-%m-%dT%H:%M:%S.%f' + ("%+02d" % offsetHour).zfill(3) + ':00'


def formatTimeZoneAwareDateTime(value):
    if value is None:
        return value
    return value.strftime(get_timezone_format())


class TimeZoneAwareDateTimeField(DateTimeField):
    def __init__(self, *args, **kwargs):
        super(TimeZoneAwareDateTimeField, self).__init__(
            format=get_timezone_format(), *args, **kwargs)
