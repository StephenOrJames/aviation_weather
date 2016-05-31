import re

from aviation_weather.components import Component
from aviation_weather.exceptions import RemarksDecodeError


class Remarks(Component):

    def __init__(self, raw):
        """Parse `raw` to create a new Remarks object.

        Args:
            raw (str): The remarks to be stored (not actually parsed at the moment).
            ao (int): The type of automated station. If AO1, then 1, or if AO2, then 2. Otherwise, the value is None.

        Raises:
            RemarksDecodeError: If `raw` could not be parsed.
        """
        if not raw.startswith("RMK "):
            raise RemarksDecodeError("Remarks(%r) could not be parsed" % raw)

        self.text = raw

        ao = re.search(r"\bAO(?P<ao>[12])\b", raw)
        if ao:
            self.ao = int(ao.group("ao"))
        else:
            self.ao = None

    @property
    def decoded(self):
        return ""  # We don't fully parse remarks.

    @property
    def raw(self):
        return self.text
