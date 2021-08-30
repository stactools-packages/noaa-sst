import os.path
from tempfile import TemporaryDirectory

from tests import test_data

import pystac
from stactools.noaa_sst.commands import create_noaasst_command
from stactools.testing import CliTestCase


def get_test_path():
    test_path = test_data.get_path("data-files")
    path = [
        os.path.join(test_path, d) for d in os.listdir(test_path)
        if d.lower().endswith(".nc")
    ][0]
    return path


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_noaasst_command]

    def test_create_cog(self):
        path = get_test_path()

        with TemporaryDirectory() as tmp_dir:
            cog_path = os.path.join(tmp_dir,
                                    os.path.basename(path)[:-3] + "_cog.tif")
            result = self.run_command(
                ["noaasst", "create-cog", path, cog_path])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))
            print(os.listdir(tmp_dir))
            print("****************")
            print(path)
            cogs = [p for p in os.listdir(tmp_dir) if p.endswith("_cog.tif")]
            self.assertEqual(len(cogs), 2)

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            destination = os.path.join(tmp_dir, "collection.json")

            result = self.run_command(
                ["noaasst", "create-collection", destination])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(destination)
            self.assertEqual(collection.id, "noaa-sst")

            collection.validate()

    def test_create_item(self):
        path = get_test_path()

        with TemporaryDirectory() as tmp_dir:
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command([
                "noaasst",
                "create-item",
                path,
                "mock__sst_cog.tif",
                "mock__sif_cog.tif",
                destination,
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item = pystac.read_file(destination)
            item.validate()
