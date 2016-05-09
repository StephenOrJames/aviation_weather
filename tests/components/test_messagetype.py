import unittest

from aviation_weather.components.messagetype import MessageType
from aviation_weather.exceptions import MessageTypeDecodeError


class TestMessageType(unittest.TestCase):

    def _test_valid(self, raw):
        self.assertEqual(raw, MessageType(raw).raw)

    def test_valid_metar(self):
        self._test_valid("METAR")

    def test_valid_speci(self):
        self._test_valid("SPECI")

    def test_valid_taf(self):
        self._test_valid("TAF")

    def test_valid_taf_amd(self):
        self._test_valid("TAF AMD")

    def _test_invalid(self, raw):
        with self.assertRaises(MessageTypeDecodeError):
            MessageType(raw)

    def test_invalid_1(self):
        self._test_invalid("")

    def test_invalid_2(self):
        self._test_invalid("BAD")

    def test_invalid_3(self):
        self._test_invalid("INVALID")
