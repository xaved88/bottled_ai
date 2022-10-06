import unittest

from rs.helper.seed import get_seed_string, make_seed_string_number


class SeedTestCase(unittest.TestCase):
    def test_seed_conversion(self):
        self.assertEqual(get_seed_string(2283446537348531365), "NMRZXQFDKKHK")
        self.assertEqual(get_seed_string(4309242589861862459), "19M4YWURMXE59")
        self.assertEqual(get_seed_string(1394488993359253936), "EFI1QKN4EWKB")
        self.assertEqual(get_seed_string(7230305506610474027), "24W1XWCFJR2ZC")

    def test_seed_conversion_other_way(self):
        self.assertEqual(make_seed_string_number("NMRZXQFDKKHK"), 2283446537348531365)
        self.assertEqual(make_seed_string_number("19M4YWURMXE59"), 4309242589861862459)
        self.assertEqual(make_seed_string_number("EFI1QKN4EWKB"), 1394488993359253936)
        self.assertEqual(make_seed_string_number("24W1XWCFJR2ZC"), 7230305506610474027)
