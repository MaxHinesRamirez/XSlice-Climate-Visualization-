import os

import matplotlib as mpl
import matplotlib.font_manager
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import netCDF4 as nC
import numpy as np
import PIL

os.environ["PROJ_LIB"] = "C:\\Utilities\\Python\\Anaconda\\Library\\share"
from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
import matplotlib.ticker as mticker
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
norm = colors.TwoSlopeNorm(vcenter=0.00)


# Create a dictionary for drawing lines on Basemap
def draw_countries(ax):
    ax.add_feature(cfeature.BORDERS)


def draw_rivers(ax):
    ax.add_feature(cfeature.RIVERS)


def draw_states(ax):
    ax.add_feature(cfeature.STATES)

def draw_lakes(ax):
    ax.add_feature(cfeature.LAKES)

def format_meridian_label(deg):
    if deg == 180:
        return "180"  # No 'E' or 'W' for 180 degrees
    elif deg > 180:
        deg = 360 - deg
        return f"{int(deg)}W"
    elif deg == 0:
        return "0"  # No 'E' for 0 degrees
    else:
        return f"{int(deg)}E"

def format_parallel_label(deg):
    if deg == 0:
        return "0"  # No 'N' or 'S' for 0 degrees (Equator)
    elif deg < 0:
        return f"{-int(deg)}S"
    else:
        return f"{int(deg)}N"
        
aesthetics = {"Countries": draw_countries, "Rivers": draw_rivers, "States": draw_states,"Lakes":draw_lakes}


# Separating Hovmoller into Seasons
def seasonal_cols(Year, Month):
    all_col = np.zeros((3 * (Year[1] - Year[0]) - 2))
    season = int(Month % 12 / 3)
    if season == 0:  # winter
        col = [0, 1, 11]
    elif season == 1:  # spring
        col = [2, 3, 4]
    elif season == 2:  # summer
        col = [5, 6, 7]
    else:  # fall
        col = [8, 9, 10]
    for i in range(0, all_col.size):
        if i % 3 == 0:
            all_col[i] = col[0] + int(i / 3) * 12
        elif i % 3 == 1:
            all_col[i] = col[1] + int(i / 3) * 12
        else:
            all_col[i] = col[2] + int(i / 3) * 12
    if Month % 3 == 1:
        all_col = all_col[1:]
    if Month % 3 == 2:
        all_col = all_col[2:]
    return all_col.astype(int)


# homvoller graph
def hov(cs, interval, variables, year, month, depth, lat, lon, clrs, font_dic, align):
    plt.clf()
    file = nC.Dataset("godas_" + variables + ".nc")
    time = np.linspace(year[0], year[1], (year[1] - year[0]) * 12 + 1)
    if variables == "salt":
            units='psu'
    else:
        units = file.variables[variables].units if 'units' in file.variables[variables].ncattrs() else 'Unknown units'
    if interval == "Annual":
        time = time[::12]

    if cs == "Latitudinal":
        zz = file.variables[variables][
             (year[0] - 1980) * 12: (year[1] - 1980) * 12 + month,
             depth[0],
             lat[0]: lat[-1] + 1,
             lon[0],
             ]
        x = file.variables["lat"][lat[0]: lat[-1] + 1]
        fig, ax = plt.subplots(figsize=(20,8))
        plt.xlabel("Latitude", size=20)
    elif cs == "Longitudinal":
        zz = file.variables[variables][
             (year[0] - 1980) * 12: (year[1] - 1980) * 12 + month,
             depth[0],
             lat[0],
             lon[0]: lon[-1] + 1,
             ]
        x = file.variables["lon"][lon[0]: lon[-1] + 1]
        fig, ax = plt.subplots(figsize=(20,8))
        plt.xlabel("Longitude", size=20)
    else:
        x = file.variables["level"][depth[0]: depth[-1] + 1]
        zz = file.variables[variables][
             (year[0] - 1980) * 12: (year[1] - 1980) * 12 + month,
             depth[0]: depth[-1] + 1,
             lat[0],
             lon[0],
             ]
        fig, ax = plt.subplots(figsize=(20,8))
        plt.xlabel("Depth [m]",size=20)

    if interval == "Seasonal":
        cols = seasonal_cols(year, month)
        time = time[cols]
        zz = zz[cols, :]
    else:
        zz = zz[month - 1:, :]
        if interval == "Annual":
            zz = zz[::12, :]
    xx, tt = np.meshgrid(x, time)
    if variables in ["ucur", "vcur"]:
        plt.contourf(xx, tt, zz, norm=norm, levels=100, cmap=clrs)
    else:
        plt.contourf(xx, tt, zz, levels=100, cmap=clrs)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=20)
    ax.tick_params(axis="x", labelsize=20)
    ax.tick_params(axis="y", labelsize=20)
    plt.text(0.5, 1.01, f'{units}', font=font_dic, ha='center', va='bottom', transform=cb.ax.transAxes)
    plt.ylabel("Year", size=20)
    title = hov_title(cs, variables, interval, month, depth, lat, lon)
    plt.title(title, font=font_dic, loc=align)


def hov_title(cs, variables, interval, month, depth, lat, lon):
    file = nC.Dataset("godas_" + variables + ".nc")
    if cs == "Latitudinal":
        u, v = file.variables["level"][:], file.variables["lon"][:]
        title = (
                variables + " at " + str(u[depth[0]]) + "m and Longitude " + str(v[lon[0]])
        )
    elif cs == "Longitudinal":
        u, v = file.variables["level"][:], file.variables["lat"][:]
        title = (
                variables + " at " + str(u[depth[0]]) + "m and Latitude " + str(v[lat[0]])
        )
    else:
        u, v = file.variables["lat"][:], file.variables["lon"][:]
        title = (
                variables
                + " at Latitude "
                + str(u[lat[0]])
                + " and Longitude "
                + str(v[lon[0]])
        )
    if interval == "Annual":
        title = months[month - 1] + " " + title
    elif interval == "Seasonal":
        season = int(month % 12 / 3)
        if season == 0:
            title = "Winter " + title
        elif season == 1:
            title = "Spring " + title
        elif season == 2:
            title = "Summer " + title
        else:
            title = "Fall " + title
    return title


def f(
        hovmoller,
        interval,
        cross_section,
        variables,
        yr,
        month,
        depth,
        lat,
        lon,
        clrs,
        file_format,
        dark,
        features,
        hatches,
        text_size,
        font,
        align,
):
    font_dic = {
        "family": font,
        "weight": "normal",
        "size": text_size,
    }
    if dark:
        plt.style.use("dark_background")
    else:
        mpl.rcParams.update(mpl.rcParamsDefault)
    if hovmoller:
        hov(
            cross_section,
            interval,
            variables,
            yr,
            month,
            depth,
            lat,
            lon,
            clrs,
            font_dic,
            align,
        )
        title = hov_title(cross_section, variables, interval, month, depth, lat, lon)
    else:
        file = nC.Dataset(variables + "." + str(yr[0]) + ".nc")
        data = file.variables[variables][month - 1]
        units = file.variables[variables].units if 'units' in file.variables[variables].ncattrs() else 'Unknown units'
        if variables == "salt":
            units='psu'
            data = data*1000
        lons = file.variables["lon"][:]
        lats = file.variables["lat"][:]
        depths = file.variables["level"][:]
        new_hatch = []
        for c in hatches:
            for i in range(0, 20):
                new_hatch.append(c)
        if cross_section == "Latitudinal":
            fig, ax = plt.subplots(figsize=(20,8))
            xx, yy = np.meshgrid(
                lons[lon[0]: lon[-1]], 0 - depths[depth[0]: depth[-1]]
            )
            zz = data[depth[0]: depth[-1], lat[0], lon[0]: lon[-1]]
            if variables in ["ucur", "vcur"]:
                plt.contourf(
                    xx, yy, zz, norm=norm, cmap=clrs, hatches=new_hatch, levels=100
                )
            else:
                plt.contourf(xx, yy, zz, levels=100, hatches=new_hatch, cmap=clrs)

            title = (
                    months[month - 1]
                    + " "
                    + str(int(yr[0]))
                    + " "
                    + variables
                    + " at Latitude "
                    + str(lats[lat[0]])
            )
            plt.title(title + r"$^\circ$", font=font_dic, loc=align)
            plt.xlabel("Longitude", size=20)
            plt.ylabel("depth [m]", size=20)
            cb = plt.colorbar()
            cb.ax.tick_params(labelsize=20)
            ax.tick_params(axis="x", labelsize=20)
            ax.tick_params(axis="y", labelsize=20)
            plt.text(0.5, 1.01, f'{units}', font=font_dic, ha='center', va='bottom', transform=cb.ax.transAxes)

        elif cross_section == "Longitudinal":
            fig, ax = plt.subplots(figsize=(20,8))
            xx, yy = np.meshgrid(
                lats[lat[0]: lat[-1]], 0 - depths[depth[0]: depth[-1]]
            )
            zz = data[depth[0]: depth[-1], lat[0]: lat[-1], lon[0]]
            if variables in ["ucur", "vcur"]:
                plt.contourf(
                    xx, yy, zz, levels=100, norm=norm, hatches=new_hatch, cmap=clrs
                )
            else:

                plt.contourf(xx, yy, zz, levels=100, hatches=new_hatch, cmap=clrs)
            title = (
                    months[month - 1]
                    + " "
                    + str(int(yr[0]))
                    + " "
                    + variables
                    + " at Longitude "
                    + str(lons[lon[0]])
            )
            plt.title(title + r"$^\circ$", font=font_dic, loc=align)
            plt.xlabel("Latitude", size=20)
            plt.ylabel("depth [m]", size=20)
            cb = plt.colorbar(
                format=mpl.ticker.ScalarFormatter(useMathText=True)
            )
            cb.ax.tick_params(labelsize=20)
            ax.tick_params(axis="x", labelsize=20)
            ax.tick_params(axis="y", labelsize=20)
            plt.text(0.5, 1.01, f'{units}', font=font_dic, ha='center', va='bottom', transform=cb.ax.transAxes)

        else:
            xx, yy = np.meshgrid(lons[lon[0]: lon[-1]], lats[lat[0]: lat[-1]])
            ig = plt.figure(figsize=(20,8))
            ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
            zz = data[depth[0], lat[0]: lat[-1], lon[0]: lon[-1]]
            if variables in ["ucur", "vcur"]:
                plt.pcolormesh(xx, yy, zz, shading="auto", norm=norm, cmap=clrs,transform=ccrs.PlateCarree())
            else:
                plt.pcolormesh(xx, yy, zz, shading="auto", cmap=clrs,transform=ccrs.PlateCarree())
            cax = ig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
            cb = plt.colorbar(location="right",cax=cax,shrink=0.8)
            cb.ax.tick_params(labelsize=20)
            cb.formatter.set_powerlimits((-7, 3))
            plt.text(0.5, 1.01, f'{units}', font=font_dic, ha='center', va='bottom', transform=cb.ax.transAxes)
            for feature in features:
                aesthetics[feature](ax)
            ax.coastlines()
            ax.add_feature(cfeature.LAND.with_scale('50m'), facecolor='white')
            gl = ax.gridlines(crs=ccrs.PlateCarree())
            gl.xlocator = mticker.FixedLocator([-180, -120, -60, 0, 60, 120, 180])
            gl.ylocator = mticker.FixedLocator([-90, -60, -30,0, 30, 60, 90])
            # gl.xlabel_style = {'size': 20}
            # gl.ylabel_style = {'size':20}
            # Set the gridlines and labels
            ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
            ax.set_yticks([-90, -60, -30,0, 30, 60, 90], crs=ccrs.PlateCarree())
            lon_formatter = LongitudeFormatter(number_format='.0f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
            lat_formatter = LatitudeFormatter(number_format='.0f',
                                      degree_symbol='')
            ax.xaxis.set_major_formatter(lon_formatter)
            ax.yaxis.set_major_formatter(lat_formatter)
            ax.tick_params(axis="x", labelsize=20)
            ax.tick_params(axis="y", labelsize=20)
            ax.set_extent([lons[lon[0]], lons[lon[-1]], lats[lat[0]], lats[lat[-1]]], crs=ccrs.PlateCarree())
            title = (
                    months[month - 1]
                    + " "
                    + str(int(yr[0]))
                    + " "
                    + variables
                    + " at "
                    + str(int(depths[depth[0]]))
                    + " m"
            )
            plt.sca(ax)
            plt.title(title, font=font_dic, loc=align, pad=20)
            
            plt.xticks(size=20)
            plt.yticks(size=20)

    if file_format != "NONE":
        plt.savefig("images/" + title + file_format)
    plt.show()
