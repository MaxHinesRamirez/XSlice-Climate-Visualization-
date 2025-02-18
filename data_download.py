import os
from pathlib import Path

import numpy as np
import requests
import xarray as xr

ALL_VARIABLES = ["salt", "pottmp", "ucur", "vcur"]
def download_data():
    folder = Path("GODAS_data")
    folder.mkdir(exist_ok=True) 
    combined_files = [folder / f"godas_{var}.nc" for var in ALL_VARIABLES]
    if all(cf.exists() for cf in combined_files):
        print("Data appears to be already downloaded and combined. Skipping download.")
        create_climatologies(folder)
        return
    years = np.arange(1980, 2024)
    os.chdir(folder)

    for year in years:
        for var in ALL_VARIABLES:
            filename = f"{var}.{year}.nc"
            if not os.path.exists(filename):
                url = f"https://downloads.psl.noaa.gov/Datasets/godas/{var}.{year}.nc"
                print(f"Downloading {filename}...")
                r = requests.get(url, allow_redirects=True)
                with open(filename, "wb") as f:
                    f.write(r.content)
            else:
                print(f"{filename} already exists, skipping download.")

    for var in ALL_VARIABLES:
        print(f"Combining {var}.*.nc into godas_{var}.nc ...")
        ds = xr.open_mfdataset(f"{var}.*.nc", combine="nested", concat_dim="time")
        ds.to_netcdf(f"godas_{var}.nc")

    images_folder = Path("images")
    images_folder.mkdir(exist_ok=True)

    # create_climatologies(Path.cwd())

    print("Download and combination complete!")
    print(f"Data files are located in: {folder.resolve()}")

def create_climatologies(folder: Path):
    for var in ALL_VARIABLES:
        combined_file = folder / f"godas_{var}.nc"
        clim_file = folder / f"godas_{var}_clim.nc"

        if not combined_file.exists():
            print(f"Cannot create climatology for {var} - {combined_file} is missing!")
            continue

        if clim_file.exists():
            print(f"Climatology {clim_file.name} already exists, skipping.")
            continue

        print(f"Creating climatology for {var} -> {clim_file.name}")
        ds = xr.open_dataset(combined_file)

        if not isinstance(ds.time.values[0], np.datetime64):
            ds["time"] = ds.indexes["time"].to_datetimeindex()

        ds_clim = ds.groupby("time.month").mean(dim="time", keep_attrs=True)

        ds_clim.to_netcdf(clim_file)
        print(f"Climatology for {var} saved as {clim_file.name}")
    print(f"Data files are located in: {folder.resolve()}")
