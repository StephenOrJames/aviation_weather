import re

from aviation_weather import Pressure
from aviation_weather.components import Component
from aviation_weather.exceptions import PressureDecodeError, RemarksDecodeError


class Remarks(Component):

    # TODO: create property setters that properly update text.

    def __init__(self, raw):
        """Parse `raw` to create a new Remarks object.

        Args:
            raw (str): The remarks to be stored (not actually parsed at the moment).
            ao (int): The type of automated station. If AO1, then 1, or if AO2, then 2. Otherwise, the value is None.
            slp (Pressure/None): The sea-level pressure.

        Raises:
            RemarksDecodeError: If `raw` could not be parsed.
        """
        if not raw.startswith("RMK "):
            raise RemarksDecodeError("Remarks(%r) could not be parsed" % raw)

        self.text = raw

        ao = re.search(r"\bAO(?P<ao>[12])\b", raw)
        if ao:
            self._ao = int(ao.group("ao"))
        else:
            self._ao = None

        slp = re.search(r"\b(?P<slp>SLP(\d{3}|NO))\b", raw)
        if slp:
            self._slp = Pressure(slp.group("slp"))
        else:
            self._slp = None

    @property
    def decoded(self):
        return ""  # We don't fully parse remarks.

    @property
    def raw(self):
        return self.text

    @property
    def ao(self):
        return self._ao

    @property
    def slp(self):
        return self._slp
