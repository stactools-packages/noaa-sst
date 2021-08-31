from datetime import datetime
import logging

from pystac import (
    Collection,
    Item,
    Asset,
    Extent,
    SpatialExtent,
    TemporalExtent,
    CatalogType,
    MediaType,
)
from pystac.extensions.projection import ProjectionExtension

from stactools.noaa_sst.constants import (
    NOAA_SST_ID,
    SPATIAL_EXTENT,
    TEMPORAL_EXTENT,
    SST_PROVIDER,
    TITLE,
    DESCRIPTION,
    LICENSE,
    LICENSE_LINK,
    SST_EPSG,
)
from netCDF4 import Dataset

logger = logging.getLogger(__name__)


def create_collection() -> Collection:
    """Create a STAC Collection

    This function includes logic to extract all relevant metadata from
    an asset describing the STAC collection and/or metadata coded into an
    accompanying constants.py file.

    See `Collection<https://pystac.readthedocs.io/en/latest/api.html#collection>`_.

    Returns:
        Collection: STAC Collection object
    """
    extent = Extent(
        SpatialExtent([SPATIAL_EXTENT]),
        TemporalExtent(TEMPORAL_EXTENT),
    )

    collection = Collection(
        id=NOAA_SST_ID,
        title=TITLE,
        description=DESCRIPTION,
        license=LICENSE,
        providers=[SST_PROVIDER],
        extent=extent,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
    )

    collection.add_link(LICENSE_LINK)

    return collection


def create_item(nc_href: str, sst_cog_href: str, sif_cog_href: str) -> Item:
    """Create a STAC Item
    Collect metadata from a NOAA-SST netcdf file to create the Item
    Args:
        nc_href (str): The HREF pointing to the NOAA netcdf file
        cog_href (str): The HREF pointing to the associated asset COG. The COG should
        be created in advance using `cog.create_cog`
    Returns:
        Item: STAC Item object
    """
    with Dataset(nc_href) as ds:
        properties = {
            "title": ds.title,
            "noaa-sst:institution": ds.institution,
            "noaa-sst:source": ds.source,
            "noaa-sst:history": ds.history,
            "noaa-sst:comment": ds.comment,
        }
        item_datetime = datetime.strptime(ds.time_coverage_start,
                                          '%Y%m%dT%H%M%SZ')

        dims = ds.dimensions
        ds_shape = [dims["lon"].size, dims["lat"].size]
        x_cellsize = 360.0 / float(dims["lon"].size)
        y_cellsize = 180.0 / float(dims["lat"].size)

    global_geom = {
        "type":
        "Polygon",
        "coordinates": [[[-180.0, -90.0], [180.0, -90.0], [180.0, 90.0],
                         [-180.0, 90.0], [-180.0, -90.0]]],
    }

    item = Item(id=f"{NOAA_SST_ID}-noaa-{item_datetime}",
                properties=properties,
                geometry=global_geom,
                bbox=SPATIAL_EXTENT,
                datetime=item_datetime,
                stac_extensions=[])

    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = SST_EPSG
    proj_attrs.bbox = SPATIAL_EXTENT
    proj_attrs.shape = ds_shape
    proj_attrs.transform = [
        SPATIAL_EXTENT[0],
        x_cellsize,
        0.0,
        SPATIAL_EXTENT[1],
        0.0,
        -y_cellsize,
    ]
    # It is a good idea to include proj attributes to optimize for libs like stac-vrt
    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = 4326
    proj_attrs.bbox = [-180, 90, 180, -90]
    proj_attrs.shape = [1, 1]  # Raster shape
    proj_attrs.transform = [-180, 360, 0, 90, 0, 180]  # Raster GeoTransform

    # Add an asset to the item (COG for example)
    item.add_asset(
        "sst_cog",
        Asset(
            href=sst_cog_href,
            media_type=MediaType.COG,
            roles=["data"],
        ),
    )
    item.add_asset(
        "sif_cog",
        Asset(
            href=sif_cog_href,
            media_type=MediaType.COG,
            roles=["data"],
        ),
    )
    return item
