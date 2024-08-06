import ipywidgets as widgets
import numpy as np
#Layout
widget_layout = widgets.Layout(width='auto', height='auto', font_size='50px')
#LOGO
file = open("XSLICELOGOFINAL.PNG", "rb")
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
levels = widgets.SelectionRangeSlider(
    options=np.arange(0, 40),
    index=(0, 39),
    description="Depth",
    disabled=False,
    continuous_update=False,
)
lat_w = widgets.SelectionRangeSlider(
    options=np.arange(0, 418),
    index=(0, 417),
    description=" Latitude ",
    disabled=False,
    continuous_update=False,
)
lon_w = widgets.SelectionRangeSlider(
    options=np.arange(0, 360),
    index=(0, 359),
    description=" Longitude ",
    disabled=False,
    continuous_update=False,
)
lon_w.style.description_width = '90px'

# Time Widgets
year_w = widgets.SelectionRangeSlider(
    options=np.arange(1980, 2022),
    index=(0, 41),
    description=" Year ",
    disabled=False,
    continuous_update=False,
)
month_w = widgets.IntSlider(
    value=1,
    min=1,
    max=12,
    description="Month: ",
    disabled=False,
    continuous_update=False,
    orientation="horizontal",
    readout=True,
)
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
#MOVIE WIDGETS
movie = widgets.ToggleButton(
    value=False,
    description="Movie",
    disabled=False,
    button_style="",
    tooltip="Movie mode",
    icon="play-circle",  # (FontAwesome names without the `fa-` prefix)
)

movie_order = widgets.Dropdown(
    options=["Time First", "Depth First"],
    value="Depth First",
    description="Slider Sequence",
    disabled=False,
)

movie_order.style.description_width = '100px'

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
                        variable_butt,
                         mean_butt
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
    t2a2r3 = widgets.HBox([month_w, year_w])  # Tab 2 accordion 2, row 3
    t2a2r4 = widgets.HTML(  # Some HTML to make it prettier
        value="<h2><b><center>Axes</center></b></h2>",
        placeholder="",
        description="",
    )
    t2a2r5 = widgets.HBox([levels, lat_w, lon_w])  # Tab 2, accordion 2, row 5
    tab2_accord2 = widgets.VBox(
        [t2a2r1, t2a2r2, t2a2r3, t2a2r4, t2a2r5]
    )  # Combining into 1 accordion
    # tab2_accord3 = widgets.HBox([movie,movie_order])
    # Combining accordions to make the tab
    # tab2 = widgets.Accordion(children=[tab2_accord1, tab2_accord3,tab2_accord2], selected_index=2)
    tab2 = widgets.Accordion(children=[tab2_accord1, tab2_accord2], selected_index=1)
    # adding names
    # accordion_titles = ["Hovmoller","Movie", "Cross Section"]
    accordion_titles = ["Hovmoller", "Cross Section"]
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
