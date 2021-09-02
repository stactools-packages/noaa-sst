from datetime import datetime
from pyproj import CRS
from pystac import Provider, ProviderRole, Link

NOAA_SST_ID = "noaa-sst"
SST_EPSG = 4326
SST_CRS = CRS.from_epsg(SST_EPSG)
LICENSE = "proprietary"
lic_link = "https://github.com/stactools-packages/noaa-sst/tree/main/src/stactools/noaa_sst/license"
"/data-license.txt"
LICENSE_LINK = Link(rel="license",
                    target=lic_link,
                    title="Public Domain License - NOAA")
SPATIAL_EXTENT = [-180.0, 90.0, 180.0, -90.0]
TEMPORAL_EXTENT = [
    datetime(1985, 1, 1),
    None,
]
DESCRIPTION = """The NOAA Coral Reef Watch (CRW) daily global 5km Sea Surface Temperature (SST)
product, also known as CoralTemp, shows the nighttime ocean temperature measured at the surface.
The SST scale ranges from -2 to 35 °C. The product is updated each afternoon at about
12:00pm U.S. Eastern Time."""
TITLE = 'NOAA 5km Sea Surface Temperature (SST)'
SST_PROVIDER = Provider(
    name="NOAA Coral Reef Watch Program",
    roles=[ProviderRole.PRODUCER, ProviderRole.PROCESSOR, ProviderRole.HOST],
    url="https://coralreefwatch.noaa.gov/")
