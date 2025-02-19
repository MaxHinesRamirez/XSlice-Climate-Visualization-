import os

import matplotlib as mpl
import matplotlib.font_manager
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import netCDF4 as nC
import numpy as np
import PIL
from IPython.display import Video, display
os.environ["PROJ_LIB"] = "C:\\Utilities\\Python\\Anaconda\\Library\\share"
from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
import matplotlib.ticker as mticker
import xarray as xr
import matplotlib.animation as animation

import imageio_ffmpeg
import matplotlib as mpl


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
        return "180"  
    elif deg > 180:
        deg = 360 - deg
        return f"{int(deg)}W"
    elif deg == 0:
        return "0" 
    else:
        return f"{int(deg)}E"

def format_parallel_label(deg):
    if deg == 0:
        return "0" 
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
def hov(cs, interval, variables,pottmp_units, year, month, depth, lat, lon, clrs, font_dic, align):
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
    plt.show()


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

#Movie 
def play_movie(cs, variables, year, month,animation):
    video_path = f"movies/{animation}"
    video_widget = Video(video_path, embed=True, width=1200, height=600)
    # Display the video widget
    display(video_widget)

def create_animation(
    variables,
    pottmp_units,
    yr,
    month,
    lat,
    lon,
    depth,
    animation_title,
    clrs,
    cross_section,
    base_path="movies/created_animations",
    filename_ext=".mp4",
):

    file_path = f"godas_{variables}.nc"
    ds = xr.open_dataset(file_path)

    latitudes_full = ds["lat"].values
    longitudes_full = ds["lon"].values
    depths_full = ds["level"].values
    units = ds[variables].units if 'units' in ds[variables].attrs else 'Unknown units'

    latitudes = latitudes_full[lat[0] : lat[-1] + 1]
    longitudes = longitudes_full[lon[0] : lon[-1] + 1]
    depths_sel = depths_full[depth[0] : depth[-1] + 1]

    data_subset = ds[variables].sel(
        time=ds.time.dt.month == month,
        lat=latitudes,
        lon=longitudes,
        level=depths_sel
    ).sel(time=slice(f"{yr[0]}-01-01", f"{yr[-1]}-12-31"))

    if variables=='pottmp' and pottmp_units == "Celsius":
        data_subset = data_subset - 273.15
        units = "°C"
    sampled = data_subset.isel(time=slice(None, None, 5), level=slice(None, None, 5))
    vmin = float(sampled.min().values)
    vmax = float(sampled.max().values)

    if cross_section == "Depth":
        fig, ax = plt.subplots(
            figsize=(15,7),
            subplot_kw={"projection": ccrs.PlateCarree(central_longitude=180)}
        )
        ax.set_extent([longitudes_full[lon[0]], longitudes_full[lon[-1]],
                       latitudes_full[lat[0]], latitudes_full[lat[-1]]],
                      crs=ccrs.PlateCarree())
        ax.coastlines()
        ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor="white")
    else:
        fig, ax = plt.subplots(figsize=(15,7))

    cbar = None

    time_count = data_subset.time.size
    depth_count = data_subset.level.size
    lat_count   = data_subset.lat.size
    lon_count   = data_subset.lon.size

    month_name = months[month - 1]

    def animate(frame):
        nonlocal cbar
        ax.clear()

        def get_year(time_idx):
            dt64 = data_subset.time.isel(time=time_idx).values
            return np.datetime64(dt64, "Y").astype(int) + 1970

        if cross_section == "Depth":
            depth_ind = frame // time_count
            time_ind  = frame % time_count

            data_slice = data_subset.isel(time=time_ind, level=depth_ind)
            depth_val  = float(data_subset.level.isel(level=depth_ind))

            xx, yy = np.meshgrid(longitudes, latitudes)

            ax.coastlines()
            ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor="white")

            cs = ax.pcolormesh(
                xx, yy, data_slice.values,
                shading="auto", cmap=clrs,
                transform=ccrs.PlateCarree(),
                vmin=vmin, vmax=vmax
            )
            year_val = get_year(time_ind)

            ax.set_title(f"{variables} for {month_name} {year_val} at depth of {depth_val} m",
                         fontsize=16)

            gl = ax.gridlines(crs=ccrs.PlateCarree())
            gl.xlocator = mticker.FixedLocator([-180, -120, -60, 0, 60, 120, 180])
            gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])

            ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
            ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
            lon_fmt = LongitudeFormatter(number_format=".0f", degree_symbol="",
                                         dateline_direction_label=True)
            lat_fmt = LatitudeFormatter(number_format=".0f", degree_symbol="")
            ax.xaxis.set_major_formatter(lon_fmt)
            ax.yaxis.set_major_formatter(lat_fmt)

            if cbar is None:
                cbar = plt.colorbar(cs, ax=ax, shrink=0.88)
                cbar.ax.tick_params(labelsize=15)
                fig.text(0.79, 0.85, f'{units}', fontsize=20, ha='center', va='bottom')
                
            ax.set_extent([longitudes_full[lon[0]], longitudes_full[lon[-1]],
                           latitudes_full[lat[0]], latitudes_full[lat[-1]]],
                          crs=ccrs.PlateCarree())

        elif cross_section == "Longitudinal":
            lon_ind = frame // time_count
            time_ind = frame % time_count

            data_slice = data_subset.isel(time=time_ind, lon=lon_ind)
            lon_val = float(data_subset.lon.isel(lon=lon_ind))

            lat_vals   = data_subset.lat.values
            depth_vals = data_subset.level.values
            xx, yy = np.meshgrid(lat_vals, -depth_vals)  

            cs = ax.pcolormesh(xx, yy, data_slice.values,
                               shading="auto", cmap=clrs,
                               vmin=vmin, vmax=vmax)
            year_val = get_year(time_ind)
            ax.set_title(f"{variables} for {month_name} {year_val} at longitude {lon_val:.2f}°",
                         fontsize=16)
            ax.set_xlabel("Latitude", fontsize=14)
            ax.set_ylabel("Depth [m]", fontsize=14)

            if cbar is None:
                cbar = plt.colorbar(cs, ax=ax, shrink=0.88)
                cbar.ax.tick_params(labelsize=15)
                fig.text(0.79, 0.85, f'{units}', fontsize=20, ha='center', va='bottom')

        elif cross_section == "Latitudinal":
            lat_index_pos = frame // time_count
            time_ind      = frame % time_count

            lat_ind = lat_indices[lat_index_pos]

            data_slice = data_subset.isel(time=time_ind, lat=lat_ind)
            lat_val = float(data_subset.lat.isel(lat=lat_ind))

            lon_vals   = data_subset.lon.values
            depth_vals = data_subset.level.values
            xx, yy = np.meshgrid(lon_vals, -depth_vals)  

            cs = ax.pcolormesh(xx, yy, data_slice.values,
                               shading="auto", cmap=clrs,
                               vmin=vmin, vmax=vmax)
            year_val = get_year(time_ind)
            ax.set_title(f"{variables} for {month_name} {year_val} at latitude {lat_val:.2f}°",
                         fontsize=16)
            ax.set_xlabel("Longitude", fontsize=14)
            ax.set_ylabel("Depth [m]", fontsize=14)

            if cbar is None:
                cbar = plt.colorbar(cs, ax=ax, shrink=0.88)
                cbar.ax.tick_params(labelsize=15)
                fig.text(0.79, 0.85, f'{units}', fontsize=20, ha='center', va='bottom')

    if cross_section == "Depth":
        frames = depth_count * time_count

    elif cross_section == "Longitudinal":
        frames = lon_count * time_count

    elif cross_section == "Latitudinal":
        lat_indices = np.arange(lat_count)[::3]  
        frames = len(lat_indices) * time_count

    ani = animation.FuncAnimation(fig, animate, frames=frames, repeat=False)

    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    out_file = os.path.join(base_path, f"{animation_title}{filename_ext}")

    Writer = animation.writers["ffmpeg"]
    writer = Writer(fps=1.5, metadata=dict(artist="Me"), bitrate=1800)
    ani.save(out_file, writer=writer)
    plt.close(fig)

    print(f"Saved animation to {out_file}")

#Time Series plot
def plot_timeseries(variables,pottmp_units, yr, month, lat, lon, depth, cross_section):
    ds = xr.open_dataset(f"godas_{variables}.nc")
    units = ds[variables].units if 'units' in ds[variables].attrs else 'Unknown units'
    lats = ds["lat"].values
    lons = ds["lon"].values
    depths = ds["level"].values
    all_years = np.arange(yr[0], yr[1] + 1)
    data_points = []

    for y in all_years:
        date_str = f"{y}-{month:02d}-01"
        single_time_ds = ds[variables].sel(time=date_str, method="nearest")

        if cross_section == "Depth":
            val = single_time_ds.isel(
                lat=lat[0],
                lon=lon[0],
                level=slice(depth[0], depth[-1] + 1)
            ).mean(dim="level").values
            title = (
                f"Time Series of {months[month - 1]} {variables} at "
                f"latitude {round(lats[lat[0]],1)}$^\circ$, longitude {lons[lon[0]]}$^\circ$, "
                f"averaged across depth {depths[depth[0]]} m to {depths[depth[-1]]} m")

        elif cross_section == "Longitudinal":
            val = single_time_ds.isel(
                lat=lat[0],
                level=depth[0],
                lon=slice(lon[0], lon[-1] + 1)
            ).mean(dim="lon").values
            title = (f"Time Series of {months[month-1]} {variables} at "
                     f"latitude {str(round(lats[lat[0]],1))}$^\circ$, depth {depths[depth[0]]} m, "
                     f"averaged across longitude {lons[lon[0]]}$^\circ$ to {lons[lon[-1]]}$^\circ$")

        elif cross_section == "Latitudinal":
            val = single_time_ds.isel(
                lon=lon[0],
                level=depth[0],
                lat=slice(lat[0], lat[-1] + 1)
            ).mean(dim="lat").values
            title = (f"Time Series of {months[month-1]} {variables} at "
                     f"longitude {lons[lon[0]]}$^\circ$, depth {depths[depth[0]]} m, "
                     f"averaged across latitude {str(round(lats[lat[0]],1))}$^\circ$ to {str(round(lats[lat[-1]],1))}$^\circ$")

        data_points.append(val)
    if variables=='pottmp' and pottmp_units == "Celsius":
        data_points = data_points - 273.15
        units = "°C"    
    plt.figure(figsize=(10, 5))
    plt.plot(all_years, data_points, marker="o", linestyle="-")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(f"{variables} ({units})")
    plt.grid(True)
    plt.show()



def f(
        hovmoller,
        interval,
        movie,
        cross_section,
        variables,
        mean,
        pottmp_units,
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
        diff,
    time_avg,
    animation,
    animation_title,
    time_series
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
            pottmp_units,
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
    elif movie:
        play_movie(cross_section, variables, yr, month,animation)
    else:
        if variables in ["EOF_1", "EOF_2"]:
            file = nC.Dataset(variables+'_corrected.nc')
            data = file.variables['EOF']
            units = 'na'

        else:
            ds = xr.open_dataset(f"godas_{variables}.nc")
            data = ds[variables].sel(time=f"{yr[0]}-{month:02d}-01")
            units = ds[variables].attrs.get("units", "Unknown units")
            if variables == "salt":
                units='psu'
                data = data*1000
            if variables=='pottmp' and pottmp_units == "Celsius":
                data = data - 273.15
                units = "°C"
        lats = ds["lat"].values
        lons = ds["lon"].values
        depths = ds["level"].values
        new_hatch = []
        if diff:
            ds = xr.open_dataset(f"godas_{variables}.nc")
            date1 = f"{yr[0]}-{month:02d}-01"
            date2 = f"{yr[1]}-{month:02d}-01"
            data_date1 = ds[variables].sel(time=date1)
            data_date2 = ds[variables].sel(time=date2)
            data = data_date2 - data_date1

        if time_avg:
            ds = xr.open_dataset(f"godas_{variables}.nc")
            data_sel = ds[variables].sel(
                time=(ds.time.dt.year >= yr[0]) & 
                (ds.time.dt.year <= yr[1]) & 
                (ds.time.dt.month == month)
                )
            data = data_sel.mean(dim="time")

        if mean=="Mean Subtracted":
            ds_clim = xr.open_dataset(f"godas_{variables}_clim.nc")
            month_clim = ds_clim[variables].sel(month=month)
            data = data - month_clim
    
        for c in hatches:
            for i in range(0, 20):
                new_hatch.append(c)

        if time_series:
            plot_timeseries(variables, pottmp_units,yr, month, lat, lon, depth, cross_section)
    
        else:
            if cross_section == "Latitudinal":
                fig, ax = plt.subplots(figsize=(20,8))
                xx, yy = np.meshgrid(
                    lons[lon[0]: lon[-1]+1], 0 - depths[depth[0]: depth[-1]+1]
                )
                zz = data[depth[0]: depth[-1]+1, lat[0], lon[0]: lon[-1]+1]
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
                        + str(round(lats[lat[0]],1))
                )
                if diff:
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + "-"
                        + str(int(yr[1]))
                        + " difference in "
                        + variables
                        + " at Latitude "
                        + str(round(lats[lat[0]],1))
                    )
                if time_avg:
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + "-"
                        + str(int(yr[1]))
                        + " average "
                        + variables
                        + " at Latitude "
                        + str(round(lats[lat[0]],1))
                    )
                if mean=="Mean Subtracted":
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + " "
                        + variables 
                        + " anomaly"
                        + " at Latitude "
                        + str(round(lats[lat[0]],1))
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
                    lats[lat[0]: lat[-1]+1], 0 - depths[depth[0]: depth[-1]+1]
                )
                zz = data[depth[0]: depth[-1]+1, lat[0]: lat[-1]+1, lon[0]]
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
                if diff:
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + "-"
                        + str(int(yr[1]))
                        + " difference in "
                        + variables
                        + " at Longitude "
                        + str(lons[lon[0]])
                    )
                if time_avg:
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + "-"
                        + str(int(yr[1]))
                        + " average "
                        + variables
                        + " at Longitude "
                        + str(lons[lon[0]])
                    )
                if mean=="Mean Subtracted":
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + " "
                        + variables 
                        + " anomaly"
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
                xx, yy = np.meshgrid(lons[lon[0]: lon[-1]+1], lats[lat[0]: lat[-1]+1])
                ig = plt.figure(figsize=(20,8))
                ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
                zz = data[depth[0], lat[0]: lat[-1]+1, lon[0]: lon[-1]+1]
                if variables in ["ucur", "vcur"]:
                    plt.pcolormesh(xx, yy, zz, shading="auto", norm=norm, cmap=clrs,transform=ccrs.PlateCarree())
                else:
                    plt.pcolormesh(xx, yy, zz, shading="auto", cmap=clrs,transform=ccrs.PlateCarree())
                cax = ig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
                cb = plt.colorbar(location="right",cax=cax,shrink=1)
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
                if diff:
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + "-"
                        + str(int(yr[1]))
                        + " difference in "
                        + variables
                        + " at "
                        + str(int(depths[depth[0]]))
                        + " m"
                    )
                if time_avg:
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + "-"
                        + str(int(yr[1]))
                        + " average "
                        + variables
                        + " at "
                        + str(int(depths[depth[0]]))
                        + " m"
                    )
                if mean=="Mean Subtracted":
                    title = (
                        months[month - 1]
                        + " "
                        + str(int(yr[0]))
                        + " "
                        + variables 
                        + " anomaly"
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
