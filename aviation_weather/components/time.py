import re
from aviation_weather.exceptions import TimeDecodeException


class Time:
    # TODO: allow timezone conversions via datetime.time?
    # TODO: validate the specific time values?

    def __init__(self, raw):
        m = re.search(r"\b(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<timezone>Z)\b", raw)
        if not m:
            raise TimeDecodeException
        self.day = int(m.group("day"))
        self.hour = int(m.group("hour"))
        self.minute = int(m.group("minute"))
        self.timezone = m.group("timezone")

    def __str__(self):
        return "%02d%02d%02d%1s" % (self.day, self.hour, self.minute, self.timezone)
