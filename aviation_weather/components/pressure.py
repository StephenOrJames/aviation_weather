import re

from aviation_weather.components import Component
from aviation_weather.exceptions import PressureDecodeError


class Pressure(Component):
    """The Pressure class represents atmospheric pressure in either inches of mercury or hectopascals/millibars.

    Attributes:
        indicator (str): The indicator for the unit the pressure is expressed in.
        value (int/float): The measure of the pressure in the unit indicated by `indicator`.
    """

    def __init__(self, raw: str):
        """Parse `raw` to create a new Pressure object.

        Args:
            raw (str): The pressure to be parsed.

        Raises:
            PressureDecodeError: If `raw` could not be parsed.
        """
        m = re.search(r"\b(?P<indicator>[AQ])(?P<value>\d{4})\b", raw)
        if not m:
            raise PressureDecodeError("Pressure(%s) could not be parsed" % raw)
        self.indicator = m.group("indicator")
        value = m.group("value")
        if self.indicator == "A":
            self.value = int(value) / 100
        elif self.indicator == "Q":
            self.value = int(value)
        else:
            raise PressureDecodeError("Pressure(%s) contains an invalid indicator" % raw)

    @property
    def raw(self):
        if self.indicator == "A":
            return "A%d" % int(self.value * 100)
        elif self.indicator == "Q":
            return "Q%d" % self.value
