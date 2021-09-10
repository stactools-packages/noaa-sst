import click
import logging

from stactools.noaa_sst import stac
from stactools.noaa_sst import cog

logger = logging.getLogger(__name__)


def create_noaasst_command(cli):
    """Creates the stactools-noaa-sst command line utility."""
    @cli.group(
        "noaasst",
        short_help=("Commands for working with stactools-noaa-sst"),
    )
    def noaasst():
        pass

    @noaasst.command(
        "retrieve-nc",
        short_help="Downloads a NOAA CoralTemp netcdf file",
    )
    @click.argument("source")
    def retrieve_nc_command(source: str) -> None:
        """Downloads a NOAA CoralTemp netcdf file given its FTP address
        Args:
            source (str): The ftp address of the netcdf
        """
        cog.retrieve_nc(source)

    @noaasst.command(
        "create-cog",
        short_help="Creates 2 COGs from a NOAA CoralTemp netcdf file",
    )
    @click.argument("source")
    @click.argument("destination")
    def create_cog_command(source: str, destination: str) -> None:
        """Creates 2 Cogs
        Args:
            source (str): An HREF for the NOAA CoralTemp netcdf file
            destination (str): An HREF for the Collection JSON
        """
        cog.create_cog(source, destination)

    @noaasst.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    def create_collection_command(destination: str):
        """Creates a STAC Collection
        Args:
            destination (str): An HREF for the Collection JSON
        """
        collection = stac.create_collection()

        collection.set_self_href(destination)
        collection.validate()

        collection.save_object()

        return None

    @noaasst.command("create-item", short_help="Create a STAC item")
    @click.argument("nc_href")
    @click.argument("sst_cog_href")
    @click.argument("sif_cog_href")
    @click.argument("destination")
    def create_item_command(nc_href: str, sst_cog_href: str, sif_cog_href: str,
                            destination: str) -> None:
        """Creates a STAC Item
        Args:
            nc_href (str): HREF of the netcdf associated with the Item
            sst_cog_href (str): An HREF for the associated sea surface temp COG asset
            sif_cog_href (str): An HREF for the associated sea ice fraction COG asset
            destination (str): An HREF for the STAC Collection
        """
        item = stac.create_item(nc_href, sst_cog_href, sif_cog_href)
        item.validate()
        item.save_object(dest_href=destination)

    return noaasst
