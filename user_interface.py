import ipywidgets as widgets
import numpy as np
import os
#Layout
widget_layout = widgets.Layout(width='auto', height='auto', font_size='50px')
#LOGO
file = open("XSLICELOGOFINAL.png", "rb")
image = file.read()
# logo = widgets.Image(
#     value=image,
#     format='png',
#     width=100,
#     height=1000,
# )

logo = widgets.Image(
    value=image,
    format='png',
    layout=widgets.Layout(width='300px', height='150px')
)
# WIDGETS
# Tab 1
# Variable Selection Widget
variable_butt = widgets.Select(
    font_weight = "bold",
    options=["pottmp", "salt", "ucur", "vcur"], description="Variables:", disabled=False,
)
# Mean maker widget
mean_butt = widgets.Select(
    options=["None", "Mean Subtracted", "Standardized Anomalies", "Detrended Anomalies"],
    description="Alter: ",
    disabled=False,
)

diff_toggle = widgets.ToggleButton(
    value=False,
    description="Difference Plot",
    disabled=False,
    button_style="", 
    tooltip="Toggle difference plot (plots difference between selected years)",
    icon="minus"  
)

time_avg_toggle = widgets.ToggleButton(
    value=False,
    description="Time Average",
    disabled=False,
    button_style="",  
    tooltip="Toggle to average the data for the given month across the selected years",
    icon="clock" 
)

anomaly_toggle = widgets.ToggleButton(
    value=False,
    description="Plot Anomalies",
    disabled=False,
    button_style="",
    tooltip="Toggle to plot anomalies instead of raw data",
    icon="exchange"
)

time_series_toggle = widgets.ToggleButton(
    value=False,
    description="Time Series",
    disabled=False,
    button_style="",     
    tooltip="Plot a time series at or averaged across the selected region",
    icon="line-chart" 
)


# Tab 2
# Cross Section Widget
cs_toggle = widgets.ToggleButtons(
    options=["Depth", "Longitudinal", "Latitudinal"],
    description="Cut: ",
    disabled=False,
    button_style="",
    icon=["bed"],
)
cs_toggle.style.button_width = u'300px'

# Selection Slider range
# levels = widgets.SelectionRangeSlider(
#     options=np.arange(0, 40),
#     index=(0, 39),
#     description="Depth",
#     disabled=False,
#     continuous_update=False,
# )
depth_levels = np.array([   5.,   15.,   25.,   35.,   45.,   55.,   65.,   75.,   85.,   95.,
        105.,  115.,  125.,  135.,  145.,  155.,  165.,  175.,  185.,  195.,
        205.,  215.,  225.,  238.,  262.,  303.,  366.,  459.,  584.,  747.,
        949., 1193., 1479., 1807., 2174., 2579., 3016., 3483., 3972., 4478.])


# Create a selection range slider for depth
levels = widgets.SelectionRangeSlider(
    options=[(f'{round(depth, 2)}', idx) for idx, depth in enumerate(depth_levels)],  # Show depth but pass index
    index=(0, len(depth_levels) - 1),  # Start with full range of depths
    description="Depth",
    continuous_update=False,
    readout=False,
    layout=widgets.Layout(width='250px'),
)
# Text inputs for manually adjusting depth range
min_depth_input = widgets.FloatText(value=round(depth_levels[0], 2), step=0.01,layout=widgets.Layout(width='55px'))
max_depth_input = widgets.FloatText(value=round(depth_levels[-1], 2), step=0.01,layout=widgets.Layout(width='55px'))

# Function to snap input to the nearest valid depth
def snap_to_closest_depth(value):
    closest_idx = np.abs(depth_levels - value).argmin()
    return depth_levels[closest_idx], closest_idx

# Update the slider when text inputs change
def update_slider_from_text(change):
    min_depth, min_idx = snap_to_closest_depth(min_depth_input.value)
    max_depth, max_idx = snap_to_closest_depth(max_depth_input.value)
    
    # Update the slider values to the corresponding indices
    levels.value = (min_idx, max_idx)

# Update text inputs when the slider changes
def update_text_from_slider(change):
    # Update the text inputs with the corresponding depth values, rounded to 2 decimals
    min_idx, max_idx = levels.value
    min_depth_input.value = round(depth_levels[min_idx], 2)
    max_depth_input.value = round(depth_levels[max_idx], 2)

# Observe changes in text inputs
min_depth_input.observe(update_slider_from_text, names='value')
max_depth_input.observe(update_slider_from_text, names='value')

# Observe changes in the slider
levels.observe(update_text_from_slider, names='value')


# lat_w = widgets.SelectionRangeSlider(
#     options=np.arange(0, 418),
#     # options=np.arange(-74.5, 64.5 + (1/3), (1/3)),
#     # index=(0, len(np.arange(-74.5, 64.5 + (1/3), (1/3))) - 1),
#     index=(0, 417),
#     description=" Latitude ",
#     disabled=False,
#     continuous_update=False,
# )
latitude_values = np.round(np.arange(-74.5, 64.5 + (1/3), (1/3)), 2)

# Create a selection range slider
lat_w = widgets.SelectionRangeSlider(
    options=[(f'{round(lat, 2)}', idx) for idx, lat in enumerate(latitude_values)],  # Show latitudes but return index
    index=(0, 417),  # Start with the full range (-74.5 to 64.5)
    description="Latitude",
    readout=False,
    continuous_update=False,
    layout=widgets.Layout(width='250px'),
)

# Text inputs for manually adjusting latitude range, rounded to 2 decimal places
min_lat_input = widgets.FloatText(value=round(latitude_values[0], 2),step=0.1,layout=widgets.Layout(width='55px'))
max_lat_input = widgets.FloatText(value=round(latitude_values[-1], 2), step=0.1,layout=widgets.Layout(width='55px'))

# Function to snap input to the nearest valid latitude
def snap_to_closest_latitude(value):
    # Find the index of the closest latitude
    closest_idx = np.abs(latitude_values - value).argmin()
    return latitude_values[closest_idx], closest_idx

# Update the slider when text inputs change
def update_slider_from_text(change):
    # Snap inputs to closest valid latitude values
    min_lat, min_idx = snap_to_closest_latitude(round(min_lat_input.value, 2))
    max_lat, max_idx = snap_to_closest_latitude(round(max_lat_input.value, 2))
    
    # Update the slider values to the corresponding indices
    lat_w.value = (min_idx, max_idx)

# Update text inputs when the slider changes
def update_text_from_slider(change):
    # Update the text inputs with the corresponding latitude values, rounded to 2 decimals
    min_idx, max_idx = lat_w.value
    min_lat_input.value = round(latitude_values[min_idx], 2)
    max_lat_input.value = round(latitude_values[max_idx], 2)

# Observe changes in text inputs
min_lat_input.observe(update_slider_from_text, names='value')
max_lat_input.observe(update_slider_from_text, names='value')

# Observe changes in the slider
lat_w.observe(update_text_from_slider, names='value')

longitude_values = np.round(np.arange(0, 359 + 1, 1), 1)
lon_w = widgets.SelectionRangeSlider(
    options=[(f'{round(lon, 2)}', idx) for idx, lon in enumerate(longitude_values)],
    index=(0, 359),
    description=" Longitude ",
    disabled=False,
    continuous_update=False,
    readout=False,
    layout=widgets.Layout(width='250px'),
)


lon_w.style.description_width = '90px'
min_lon_input = widgets.BoundedIntText(value=0,min=0,max=359,step=1,layout=widgets.Layout(width='50px'),)
max_lon_input = widgets.BoundedIntText(value=359,min=0,max=359,step=1,layout=widgets.Layout(width='50px'),)
def update_lon_inputs(change):
    min_lon_input.value, max_lon_input.value = change['new']

def update_lonslider_from_lower(change):
    lon_w.value = (change['new'], lon_w.value[1])

def update_lonslider_from_upper(change):
    lon_w.value = (lon_w.value[0], change['new'])
    
lon_w.observe(update_lon_inputs, names='value')
min_lon_input.observe(update_lonslider_from_lower, names='value')
max_lon_input.observe(update_lonslider_from_upper, names='value')

# Time Widgets
year_w = widgets.SelectionRangeSlider(
    options=np.arange(1980, 2022),
    index=(0, 41),
    description=" Year ",
    disabled=False,
    continuous_update=False,
    readout=False,
)
min_year_input = widgets.BoundedIntText(value=1980,min=1980,max=2022,step=1,layout=widgets.Layout(width='55px'),)
max_year_input = widgets.BoundedIntText(value=2022,min=1980,max=2022,step=1,layout=widgets.Layout(width='55px'),)
def update_year_inputs(change):
    min_year_input.value, max_year_input.value = change['new']

def update_yearslider_from_lower(change):
    year_w.value = (change['new'], year_w.value[1])

def update_yearslider_from_upper(change):
    year_w.value = (year_w.value[0], change['new'])
    
year_w.observe(update_year_inputs, names='value')
min_year_input.observe(update_yearslider_from_lower, names='value')
max_year_input.observe(update_yearslider_from_upper, names='value')

month_w = widgets.IntSlider(
    value=1,
    min=1,
    max=12,
    description="Month: ",
    disabled=False,
    continuous_update=False,
    orientation="horizontal",
    readout=False,
    layout=widgets.Layout(width='250px'),

)
month_input = widgets.BoundedIntText(value=1,min=1,max=12,step=1,layout=widgets.Layout(width='50px'),)
def update_month_inputs(change):
    month_input.value = change['new']

def update_month_slider(change):
    month_w.value = (change['new'], month_w.value[1])

month_w.observe(update_month_inputs, names='value')
month_input.observe(update_month_slider, names='value')

# HOVMOLLER WIDGETS
hovmoller = widgets.ToggleButton(
    value=False,
    description="Hovmoller",
    disabled=False,
    button_style="",  # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Description",
    icon="hourglass",  # (FontAwesome names without the `fa-` prefix)
)
hov_interval = widgets.Dropdown(
    options=["Monthly", "Seasonal", "Annual"],
    value="Monthly",
    description="Cycle:",
    disabled=False,
)
############### ANIMATION WIDGETS ##############################

def get_animation_files_for_month(month, base_folder="movies", extension=".mp4"):
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_folder = os.path.join(base_folder, month_names[month-1])

    files_month = []
    if os.path.exists(month_folder):
         files_month = [f for f in os.listdir(month_folder) if f.endswith(extension)]

    created_folder = os.path.join(base_folder, "created_animations")
    files_created = []
    if os.path.exists(created_folder):
         files_created = [f for f in os.listdir(created_folder) if f.endswith(extension)]
    
    # Combine the lists, adding a folder prefix for clarity.
    options = []
    for f in files_month:
         options.append(f"{month_names[month-1]}/{f}")
    for f in files_created:
         options.append(f"created_animations/{f}")
    return options

animation_dropdown = widgets.Dropdown(
    options=get_animation_files_for_month(month_w.value),
    description="Animations:",
    disabled=False,
    style={"description_width": "100px"},
)
def update_animation_dropdown(change):
    new_month = change['new']
    new_options = get_animation_files_for_month(new_month)
    animation_dropdown.options = get_animation_files_for_month(month_w.value)

month_w.observe(update_animation_dropdown, names='value')
refresh_button = widgets.Button(description="Refresh Animations")
def refresh_button_clicked(b):
    animation_dropdown.options = get_animation_files_for_month(month_w.value)
    
refresh_button.on_click(refresh_button_clicked)

movie = widgets.ToggleButton(
    value=False,
    description="Animation",
    disabled=False,
    button_style="",
    tooltip="Play selected animation",
    icon="play-circle",  
)

animation_title_w = widgets.Text(
    value="animation",
    description="File Name:",
    layout=widgets.Layout(width='300px'),
    style={"description_width": "100px"},
)

create_animation_button = widgets.Button(
    description="Create Animation",
    tooltip="Create a new animation with the click of a button",
    button_style="",
    icon="video-camera" 
)

animation_printbox = widgets.Output()
def on_create_video_clicked(b):
    with animation_printbox:
        from xslice_functions_Current import create_animation
        print("Creating Animation! Please wait...")
        create_animation(
            variables=variable_butt.value,
            yr=year_w.value,
            month=month_w.value,
            lat=lat_w.value,
            lon=lon_w.value,
            depth=levels.value,
            animation_title=animation_title_w.value,
            clrs=color_drop.value,
            cross_section=cs_toggle.value
        )
        print(f'{animation_title_w.value} created! Click refresh animations to find your animation!')

create_animation_button.on_click(on_create_video_clicked)


# Aesthetics Widgets
# Color Widgets
# Dark Mode
dark_mode = widgets.ToggleButton(
    value=False,
    description="Dark Mode",
    disabled=False,
    button_style="",  # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Description",
    icon="bed",  # (FontAwesome names without the `fa-` prefix)
)
# CMAP
color_drop = widgets.Dropdown(
    options=[
        "jet",
        "Greys",
        "seismic",
        "rainbow",
        "twilight_shifted",
        "viridis",
        "hot_r",
    ],
    value="jet",
    description="Colorscale:",
    disabled=False,
)
# Hatch marks
hatch_w = widgets.Dropdown(
    options=[" ", "./-\\*"],
    value=" ",
    description="Hatches:",
    disabled=False,
)
file_format = widgets.Dropdown(
    options=["NONE", ".png", ".pdf", ".jpg", ".eps", ".tiff"],
    value="NONE",
    description="Save As:",
    disabled=False,
)
# Text Widgets
# Changing Font Sizes
text_size = widgets.BoundedFloatText(
    value=25, min=0, max=50, step=0.5, description="Font Size:", disabled=False
)
# Changing Fonts
fonts = widgets.Dropdown(
    options=[
        "Arial",
        "Bookman Old Style",
        "Broadway",
        "Brush Script M7",
        "Century",
        "Century Gothic",
        "Comic Sans",
        "Courier New",
        "Elephant",
        "Franklin Gothic Heavy",
        "Garamond",
        "Georgia",
        "Impact",
        "Ink Free",
        "Magneto",
        "Old English Text MT",
        "Papyrus",
        "Sans Serif",
        "Stencil",
        "Times New Roman",
        "Vivaldi",
    ],
    value="Arial",
    description="Fonts:",
    disabled=False,
)
# Alignment
align = widgets.Dropdown(
    options=[
        "left",
        "center",
        "right",
    ],
    value="center",
    description="Align:",
    disabled=False,
)
# Put display features here
features = widgets.SelectMultiple(
    options=["Countries", "Rivers", "States","Lakes"], description="Features", disabled=False
)


def ui():
    from IPython.display import display, HTML
    style = """
    <style>
    .widget-label, 
    .widget-select select, 
    .widget-slider input, 
    .widget-toggle-button button, 
    .widget-dropdown select,
    .widget-SelectionRangeSlider
    .widget-text input, 
    .widget-boundedfloattext input {
        font-size: 18px !important;
    }
    .widget-button button {
        font-size: 18px !important;
    }
    .tabs .widget-tab .tab {
        font-size: 18px !important;  
    }
    .widget-readout {
    font-size: 18px !important;
    width: 140px !important;
    text-align: left !important;
    }
    .widget-label {
        font-size: 18px !important; 
    }
    </style>
    """

    # Display the CSS
    display(HTML(style))
    tabs = widgets.Tab()
    tab1 = widgets.HBox([ logo,
                        variable_butt,mean_butt
                        ])

    # Second tab is the main interface for operations

    # Separate Accordion for Hovmoller which will be used less
    tab2_accord1 = widgets.HBox([hovmoller, hov_interval])
    t2a2r1 = cs_toggle  # tab 2, accordion 2, row 1
    t2a2r2 = widgets.HTML(  # Some HTML to make it prettier
        value="<h2><b><center>Time</center></b></h2>",
        placeholder="",
        description="",
    )
    t2a2r3 = widgets.HBox([month_w,month_input, year_w,min_year_input,max_year_input])  # Tab 2 accordion 2, row 3
    t2a2r4 = widgets.HTML(  # Some HTML to make it prettier
        value="<h2><b><center>Axes</center></b></h2>",
        placeholder="",
        description="",
    )
    t2a2r5 = widgets.HBox([levels,min_depth_input,max_depth_input, lat_w,min_lat_input,max_lat_input, lon_w,min_lon_input,max_lon_input])  # Tab 2, accordion 2, row 5
    t2a2r6 = widgets.HBox([diff_toggle,time_avg_toggle, anomaly_toggle, time_series_toggle])
    tab2_accord2 = widgets.VBox(
        [t2a2r1, t2a2r2, t2a2r3, t2a2r4, t2a2r5,t2a2r6]
    )  # Combining into 1 accordion
    tab2_accord3_row1 = widgets.HBox([animation_title_w,create_animation_button])
    tab2_accord3_row2 = widgets.HBox([movie,animation_dropdown,refresh_button])
    tab2_accord3 = widgets.VBox([tab2_accord3_row1,tab2_accord3_row2,animation_printbox])
    # Combining accordions to make the tab
    tab2 = widgets.Accordion(children=[tab2_accord1, tab2_accord3,tab2_accord2], selected_index=2)
    # adding names
    accordion_titles = ["Hovmoller","Animation", "Cross Section"]
    [tab2.set_title(i, title) for i, title in enumerate(accordion_titles)]
    # Final Tab
    color_accord = widgets.HBox([dark_mode, color_drop, hatch_w])
    text_accord = widgets.HBox([fonts, text_size, align])
    t3_accord = widgets.Accordion(children=[color_accord, text_accord])
    accordion_titles = ["Color", "Text"]
    [t3_accord.set_title(i, title) for i, title in enumerate(accordion_titles)]
    t3r3 = widgets.HBox([features, file_format])
    tab3 = widgets.VBox([t3_accord, t3r3])
    # Putting it all together
    tabs.children = [tab1, tab2, tab3]
    tab_titles = ["Data", "Main", "Display and Export"]
    [tabs.set_title(i, title) for i, title in enumerate(tab_titles)]
    ui = tabs
    return ui
