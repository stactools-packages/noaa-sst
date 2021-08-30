import os
from tempfile import TemporaryDirectory
import unittest

from tests import test_data

from stactools.noaa_sst import stac, cog


class StacTest(unittest.TestCase):
    def test_create_collection(self):
        # Create a STAC Collection using constants
        collection = stac.create_collection()
        collection.set_self_href("")

        # Check that it has the expected ID
        self.assertEqual(collection.id, "noaa-sst")

        # Validate
        collection.validate()

    def test_create_item(self):
        # Create a COG and STAC Item using test data
        test_path = test_data.get_path("data-files")
        paths = [
            os.path.join(test_path, d) for d in os.listdir(test_path)
            if d.lower().endswith(".nc")
        ]

        with TemporaryDirectory() as tmp_dir:
            for path in paths:
                cog_path = os.path.join(
                    tmp_dir,
                    os.path.basename(path)[:-3] + "_cog.tif")
                cog.create_cog(path, cog_path)

                cogs = [
                    p for p in os.listdir(tmp_dir) if p.endswith("_cog.tif")
                ]
                self.assertEqual(len(cogs), 2)

                item = stac.create_item(path, 'sst_' + cog_path,
                                        'sif_' + cog_path)

                # Validate
                item.validate()
