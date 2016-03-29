import re

from aviation_weather.components import Component
from aviation_weather.exceptions import TimeDecodeError


class Time(Component):

    def __init__(self, raw):
        m = re.search(r"\b(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<timezone>Z)\b", raw)
        if not m:
            raise TimeDecodeError("Time(%s) could not be parsed" % raw)

        self.day = int(m.group("day"))
        self.hour = int(m.group("hour"))
        self.minute = int(m.group("minute"))
        self.timezone = m.group("timezone")

        # Validations
        if self.day > 31:
            raise TimeDecodeError("Time(%s) contains an invalid day" % raw)
        if self.hour > 23:
            raise TimeDecodeError("Time(%s) contains an invalid hour" % raw)
        if self.minute > 59:
            raise TimeDecodeError("Time(%s) contains an invalid minute" % raw)

    @property
    def raw(self):
        return "%02d%02d%02d%1s" % (self.day, self.hour, self.minute, self.timezone)
