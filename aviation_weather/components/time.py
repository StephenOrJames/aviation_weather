import re

from aviation_weather.components import Component
from aviation_weather.exceptions import TimeDecodeError


class Time(Component):
    """The Time class represents the time and date associated with the weather.

    Attributes:
        day (int): The day associated with the weather.
        hour (int): The hour associated with the weather.
        minute (int): The minute associated wih the weather.
        timezone (str): The timezone that `day`, `hour`, and `minute` are referenced in.
    """

    def __init__(self, raw):
        """Parse `raw` to create a new Time object.

        Args:
            raw (str): The time to be parsed.

        Raises:
            TimeDecodeError: If `raw` could not be parsed.
        """
        m = re.search(r"\b(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<timezone>Z)\b", raw)
        if not m:
            raise TimeDecodeError("Time(%r) could not be parsed" % raw)

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
