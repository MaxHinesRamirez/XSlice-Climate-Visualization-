import os
from pathlib import Path

import numpy as np
import requests
import xarray as xr


def download_data():
    years = np.arange(1980, 2024)
    # MAKING FOLDER
    folder = Path("GODAS data")
    folder.mkdir(exist_ok=True)
    os.chdir(folder)
    # DOWNLOADING NOAA DATA
    for year in years:
        # SALT
        url = "https://downloads.psl.noaa.gov/Datasets/godas/salt." + str(year) + ".nc"
        r = requests.get(url, allow_redirects=True)
        open("salt." + str(year) + ".nc", "wb").write(r.content)
        # POTTMP
        url = (
            "https://downloads.psl.noaa.gov/Datasets/godas/pottmp." + str(year) + ".nc"
        )
        r = requests.get(url, allow_redirects=True)
        open("pottmp." + str(year) + ".nc", "wb").write(r.content)
        # UCUR
        url = "https://downloads.psl.noaa.gov/Datasets/godas/ucur." + str(year) + ".nc"
        r = requests.get(url, allow_redirects=True)
        open("ucur." + str(year) + ".nc", "wb").write(r.content)
        # VCUR
        url = "https://downloads.psl.noaa.gov/Datasets/godas/vcur." + str(year) + ".nc"
        r = requests.get(url, allow_redirects=True)
        open("vcur." + str(year) + ".nc", "wb").write(r.content)
    # CONCATENATING NETCDF FILES FOR HOVMOLLER

    # FOR SALT
    ds_salt = xr.open_mfdataset("salt.*.nc", combine="nested", concat_dim="time")
    ds_salt.to_netcdf("godas_salt.nc")
    # For POTTMP
    ds_pottmp = xr.open_mfdataset("pottmp.*.nc", combine="nested", concat_dim="time")
    ds_pottmp.to_netcdf("godas_pottmp.nc")
    # For U Current
    ds_ucur = xr.open_mfdataset("ucur.*.nc", combine="nested", concat_dim="time")
    ds_ucur.to_netcdf("godas_ucur.nc")
    # For V Current
    ds_vcur = xr.open_mfdataset("vcur.*.nc", combine="nested", concat_dim="time")
    ds_vcur.to_netcdf("godas_vcur.nc")
    # Subfolder to store images
    subfolder = Path("images")
    subfolder.mkdir(exist_ok=True)
