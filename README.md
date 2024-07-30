# XSLICE README

###  Feel free to clone and experiment with adding new features and widgets in a separate branch


- `pip3 install --upgrade pip`
- Install pip-tools `pip3 install pip-tools`
- Update dev requirements: `pip-compile --output-file=requirements.dev.txt requirements.dev.in`
- Update requirements: `pip-compile --output-file=requirements.txt requirements.in`
- Install dev requirements `pip3 install -r requirements.dev.txt`
- Install requirements `pip3 install -r requirements.txt`


## Update versions

`pip-compile --output-file=requirements.dev.txt requirements.dev.in --upgrade`
`pip-compile --output-file=requirements.txt requirements.in --upgrade`


## How to change data
- In the xslice functions python script, change the latitude count, longitude count, layers, and time values, and variable names as required by the dataset.
- Upload your data in the GODAS data folder and rename it to whatever directory name is prefered.
- There should be two versions of each data variable. For example, 1 file with all of the potential temperature data and then the files for each year of potential temperature. If your data does not fit this following format, manually edit the xslice functions python script to load your data in properly. 
