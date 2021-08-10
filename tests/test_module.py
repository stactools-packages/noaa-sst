import unittest

import stactools.noaa_sst


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.noaa_sst.__version__)
