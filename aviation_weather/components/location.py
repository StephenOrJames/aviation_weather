import re

from aviation_weather.components import Component
from aviation_weather.exceptions import LocationDecodeError


class Location(Component):
    """The Location class represents the location associated with weather (such as a weather station or airport).

    Attributes:
        identifier (str): A sequence of four characters, the first being a letter and the other three alphanumeric.
    """

    def __init__(self, raw: str):
        """Parse `raw` to create a new Location object.

        Args:
            raw (str): The location identifier to be parsed.

        Raises:
            StationDecodeError: If the station identifier is invalid.
        """
        m = re.search(r"\b(?P<id>[A-Z][A-Z0-9]{3})\b", raw.upper())
        if not m:
            raise LocationDecodeError("Location(%r) could not be parsed" % raw)
        self.identifier = m.group("id")

    @property
    def raw(self):
        return self.identifier
