import re
from aviation_weather.exceptions import TimeDecodeException


class Time:

    def __init__(self, raw):
        m = re.search(r"\b(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<timezone>Z)\b", raw)
        if not m:
            raise TimeDecodeException("Time(%s) could not be parsed" % raw)

        self.day = int(m.group("day"))
        self.hour = int(m.group("hour"))
        self.minute = int(m.group("minute"))
        self.timezone = m.group("timezone")

        # Validations
        if self.day > 31:
            raise TimeDecodeException("Time(%s) contains an invalid day" % raw)
        if self.hour > 23:
            raise TimeDecodeException("Time(%s) contains an invalid hour" % raw)
        if self.minute > 59:
            raise TimeDecodeException("Time(%s) contains an invalid minute" % raw)

    def __str__(self):
        return "%02d%02d%02d%1s" % (self.day, self.hour, self.minute, self.timezone)
