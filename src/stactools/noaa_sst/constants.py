from datetime import datetime
from pyproj import CRS
from pystac import Provider, ProviderRole

NOAA_SST_ID = "noaa-sst"
SST_EPSG = 4326
SST_CRS = CRS.from_epsg(SST_EPSG)
LICENSE = """OSTIA Usage Statement (1985-2002): IMPORTANT usage statement. Unless otherwise agreed
in writing, these data may be used for pure academic research only, with no commercial or other
application and all usage must meet the Met Office Standard Terms and Conditions, which may be found
here: http://www.metoffice.gov.uk/corporate/legal/tandc.html. The data may be used for a maximum
period of 5 years. Reproduction of the data is permitted provided the following copyright statement
is included: (C) Crown Copyright 2010, published by the Met Office. You must submit a completed
reproduction license application form
(here http://www.metoffice.gov.uk/corporate/legal/repro_licence.html) before using the data. This
only needs to be completed once for each user. WARNING Some applications are unable to properly
handle signed byte values. If values are encountered > 127, please subtract 256 from this reported
value. GHRSST statement (2002-present): GHRSST protocol describes data use as free and open. Coral
Reef Watch program statement: The data produced by Coral Reef Watch are available for use without
restriction, but Coral Reef Watch relies on the ethics and integrity of the user to ensure that the
source of the data and products is appropriately cited and credited. When using these data and
products, credit and courtesy should be given to NOAA Coral Reef Watch. Please include the
appropriate DOI associated with this dataset in the citation. For more information, visit the NOAA
Coral Reef Watch website: https://coralreefwatch.noaa.gov. Recommendations for citing and providing
credit are provided at
https://coralreefwatch.noaa.gov/satellite/docs/recommendations_crw_citation.php. Users are referred
to the footersection of Coral Reef Watch's website(https://coralreefwatch.noaa.gov/index.php) for
disclaimers, policies, notices pertaining to the use of the data."""
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