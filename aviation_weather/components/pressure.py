import re

from aviation_weather.components import Component
from aviation_weather.exceptions import PressureDecodeError


class Pressure(Component):
    """The Pressure class represents atmospheric pressure in either inches of mercury or hectopascals/millibars.

    Attributes:
        is_slp (boolean): Whether the pressure is being treated as sea-level pressure.
        indicator (str): The indicator for the unit the pressure is expressed in.
        value (int/float/None): The measure of the pressure in the unit indicated by `indicator`, or None if SLPNO.
    """

    def __init__(self, raw: str):
        """Parse `raw` to create a new Pressure object.

        Args:
            raw (str): The pressure to be parsed.

        Raises:
            PressureDecodeError: If `raw` could not be parsed.
        """
        m = re.search(r"\b((?P<indicator>[AQ])(?P<value>\d{4})|SLP(?P<slp>(\d{3}|NO)))\b", raw)
        if not m:
            raise PressureDecodeError("Pressure(%r) could not be parsed" % raw)

        if m.group("slp"):
            self.is_slp = True
            self.indicator = "Q"
            slp = m.group("slp")
            if slp == "NO":
                self.value = None
            else:
                value = float(slp)
                self.value = value / 10
                if value < 600:
                    self.value += 1000
                else:
                    self.value += 900
        else:
            self.is_slp = False
            self.indicator = m.group("indicator")
            value = m.group("value")
            if self.indicator == "A":
                self.value = int(value) / 100
            elif self.indicator == "Q":
                self.value = int(value)
            else:
                raise PressureDecodeError("Pressure(%r) contains an invalid indicator" % raw)

    @property
    def raw(self):
        if self.is_slp:
            if self.value:
                return "SLP%s" % str(int(self.value * 10))[-3:]
            else:
                return "SLPNO"
        else:
            if self.indicator == "A":
                return "A%d" % int(self.value * 100)
            elif self.indicator == "Q":
                return "Q%d" % self.value
