# 10-sqlalchemy-challenge

This is the module 10 challenge about using sqlalchemy to get analysis and use flask to create a webpage.

---
## Analyze the Climate Data
[climate analysis](https://github.com/XueXuanXu/10-sqlalchemy-challenge/blob/main/SurfsUp/climate_starter.ipynb)        
This notebook file uses python and sqlalchemy to retrieve the climate data from *hawaii.sqlite* and does analysis for precipitation and stations based on the dataset.

---
## The Climate App
[climate app](https://github.com/XueXuanXu/10-sqlalchemy-challenge/blob/main/SurfsUp/app.py)      
This file uses python and flask to create a webpage that contain:
1. homepage(/): List all the available routes.
2. precipitation(/api/v1.0/precipitation): Return the precipitation analysis for the last 12 months in JSON form.
3. stations(/api/v1.0/stations): List the stations in JSON.
4. tobs(/api/v1.0/tobs): List temperature observations of the most-active station for the previous year in JSON.
5. start_date(/api/v1.0/<start>): Accept the start date and reurn the min, max, average temperatures calculated from the start date to the end of the dataset.
6. start_end_date(/api/v1.0/<start>/<end>): Accept the start date and reurn the min, max, average temperatures calculated from the start date to the end of the dataset.

