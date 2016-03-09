import unittest
from aviation_weather import Remarks


class TestRemarks(unittest.TestCase):
    """Unit tests for aviation_weather.components.remarks.Remarks"""

    def test_valid(self):
        """Test valid remarks"""

        # Pretty much valid if it can repeat what it was told (for now at least)
        test = "AO2 PK WND 14027/1802 SLP183 P0018 T01170106"
        self.assertEqual(test, str(Remarks(test)))

    def test_invalid(self):
        """Test invalid remarks"""

        pass  # Nothing for now; as long as it can reproduce what it was given, it's fine.


if __name__ == "__main__":
    unittest.main()
