import os.path
import urllib.request
import urllib.error
from stactools.core.utils.convert import cogify


def retrieve_nc(url):
    fileName = url.split('/')[-1]
    try:
        urllib.request.urlretrieve(url, fileName)
    except (urllib.error.URLError, urllib.error.HTTPError,
            urllib.error.ContentTooShortError):
        print("File could not be downloaded")
        return (-1)
    return (fileName)


def create_cog(nc_href: str, cog_href: str) -> None:
    sst_str = "analysed_sst"
    sif_str = "sea_ice_fraction"
    sst_output = os.path.join(
        os.path.split(cog_href)[0], ('sst_' + os.path.split(cog_href)[-1]))
    sif_output = os.path.join(
        os.path.split(cog_href)[0], ('sif_' + os.path.split(cog_href)[-1]))
    cogify(f'NETCDF:"{nc_href}":{sst_str}', sst_output,
           ["-co", "compress=LZW"])
    cogify(f'NETCDF:"{nc_href}":{sif_str}', sif_output,
           ["-co", "compress=LZW"])

    print('Done')
