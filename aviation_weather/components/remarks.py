import re

from aviation_weather import Pressure
from aviation_weather.components import Component
from aviation_weather.exceptions import PressureDecodeError, RemarksDecodeError


class Remarks(Component):

    # TODO: create property setters that properly update text.

    """The Remarks class represents the remarks ("RMK") section of a report or forecast.
    """

    def __init__(self, raw):
        """Parse `raw` to create a new Remarks object.

        Args:
            raw (str): The remarks to be stored (not actually parsed at the moment).

        Raises:
            RemarksDecodeError: If `raw` could not be parsed.
        """
        if not raw.startswith("RMK "):
            raise RemarksDecodeError("Remarks(%r) could not be parsed" % raw)

        self._text = raw

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
        return self._text

    @property
    def ao(self):
        """The type of automated station. If AO1, then 1, or if AO2, then 2. Otherwise, the value is None (int/None).
        """
        return self._ao

    @property
    def slp(self):
        """The sea-level pressure (Pressure/None).
        """
        return self._slp
