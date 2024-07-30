import os

os.environ["PROJ_LIB"] = "C:\\Utilities\\Python\\Anaconda\\Library\\share"
# fixr
from user_interface import *
from xslice_functions_Current import f


def output():
    out = widgets.interactive_output(
        f,
        {
            "hovmoller": hovmoller,
            "interval": hov_interval,
            "cross_section": cs_toggle,
            "variables": variable_butt,
            "yr": year_w,
            "month": month_w,
            "depth": levels,
            "lat": lat_w,
            "lon": lon_w,
            "clrs": color_drop,
            "file_format": file_format,
            "dark": dark_mode,
            "features": features,
            "hatches": hatch_w,
            "text_size": text_size,
            "font": fonts,
            "align": align,
        },
    )
    return out
