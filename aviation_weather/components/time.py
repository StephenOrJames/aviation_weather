import re
from aviation_weather.exceptions import TimeDecodeException


class Time:
    # TODO: use the datetime library to provide additional features?
    # TODO: validate the specific time values?

    def __init__(self, raw):
        m = re.search(r"\b(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<timezone>Z)\b", raw)
        if not m:
            raise TimeDecodeException
        self.day = m.group("day")
        self.hour = m.group("hour")
        self.minute = m.group("minute")
        self.timezone = m.group("timezone")

    def __str__(self):
        return self.day + self.hour + self.minute + self.timezone
