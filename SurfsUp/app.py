# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Create a homepage that show the available routes
@app.route("/")
def homepage():
    """List all the available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start_date&gt;<br/>"
        f"/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;"
    )


# Create a precipitation page that show the precipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation analysis for the last 12 months in JSON form."""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Design a query to retrieve the last 12 months of precipitation data. 
    # Starting from the most recent data point in the database. 
    most_recent_date = dt.date(2017,8,23)
    
    # Calculate the date one year from the last date in data set.
    one_year_before_recent_date = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    query_last_12_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=one_year_before_recent_date).all()
    
    # Change the precitation data to dictionary 
    last_12_months_precipitation_dict = dict(query_last_12_months)

    # Close the session
    session.close()

    # Return the precitation data as JSON
    return jsonify(last_12_months_precipitation_dict)
    

# Create a stations page to show list of station in JSON
@app.route("/api/v1.0/stations")
def stations():
    """List the stations in JSON."""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the stations data.
    station_query = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Create a dictionary from the row data and append to a list of stations
    stations = []
    for station, name, latitude, longitude, elevation in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations.append(station_dict)

    # Close the session
    session.close()

    # Return the stations data as JSON
    return jsonify(stations)


# Create a tobs page to show list of temperature observations for the previous year in JSON
@app.route("/api/v1.0/tobs")
def tobs():
    """List temperature observations of the most-active station for the previous year in JSON."""
    
    # Design a query to retrieve the temperature data.
    # Create our session (link) from Python to the DB
    session = Session(engine)   

    # Starting from the most recent data point in the database. 
    most_recent_date = dt.date(2017,8,23)
    
    # Calculate the date one year from the last date in data set.
    one_year_before_recent_date = most_recent_date - dt.timedelta(days=365)

    # Design a query to retrieve the temperature observations of the most-active station for the previous year
    query_last_12_months_temperature_most_active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date>=one_year_before_recent_date).order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of stations
    most_active_station_temperature = []
    for date, temperature in query_last_12_months_temperature_most_active_station:
        most_active_station_tobs_dict = {}
        most_active_station_tobs_dict["date"] = date
        most_active_station_tobs_dict["temperature"] = temperature
        most_active_station_temperature.append(most_active_station_tobs_dict)

    # Close the session
    session.close()

    # Return the stations data as JSON
    return jsonify(most_active_station_temperature)


# Create a start route that show the min, max, and average temepratures calculated from the given start date to the end of the data
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Accept the start date and reurn the min, max, average temperatures calculated from the start date to the end of the dataset."""

    # Check the formate of 
    # Design a query to retrieve the temperature data.
    # Create our session (link) from Python to the DB
    session = Session(engine)   

    # Store the start date in form of date
    try:
        start_date = dt.date.fromisoformat(f'{start}')
    except ValueError:
        return(f"error: The format of the start date is wrong. Please try to type the start date in format yyyy-mm-dd"), 404
    
    # Design a query to check the date in our dataset or not.
    start_date_check_query = session.query(Measurement.date).filter(Measurement.date == start_date).all()

    if start_date_check_query:
        # Design a query to retrieve the temperature data
        start_date_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >=start_date).all()

        # Create a dictionary for the temperature calculated data
        temperature_dict = {}
        temperature_dict["minimum temperature"] = start_date_query[0][0]
        temperature_dict["maximum temperature"] = start_date_query[0][1]
        temperature_dict["average temperature"] = start_date_query[0][2]
        return jsonify(temperature_dict)
    else:
        return(f"error: The date you type in is not in the dateset. Please try to type in a date from 2010-01-01 to 2017-08-23"), 404
    

# Create a start route that show the min, max, and average temepratures calculated from the given start date to the end of the data
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Accept the start date and reurn the min, max, average temperatures calculated from the start date to the end of the dataset."""

    # Check the formate of 
    # Design a query to retrieve the temperature data.
    # Create our session (link) from Python to the DB
    session = Session(engine)   

    # Store the start date in form of date
    try:
        start_date = dt.date.fromisoformat(f'{start}')
    except ValueError:
        return(f"error: The format of the start date is wrong. Please try to type the start date in format yyyy-mm-dd"), 404
    
    # Store the end date in form of date
    try:
        end_date = dt.date.fromisoformat(f'{end}')
    except ValueError:
        return(f"error: The format of the end date is wrong. Please try to type the end date in format yyyy-mm-dd"), 404
     
    # Check that the end date is later than the start date or not
    if (end_date< start_date):
        return (f"error: The end date cannot be earlier than the start date. Please try again."), 404
    
    # Design a query to check the start date in our dataset or not.
    start_date_check_query = session.query(Measurement.date).filter(Measurement.date == start_date).all()

    if start_date_check_query:
        # Design a query to check the end date in our dataset or not.
        end_date_check_query = session.query(Measurement.date).filter(Measurement.date == end_date).all()

        if end_date_check_query:
            # Design a query to retrieve the temperature data
            date_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(and_(Measurement.date >=start_date,Measurement.date <=end_date)).all()

            # Create a dictionary for the temperature calculated data
            temperature_dict2 = {}
            temperature_dict2["minimum temperature"] = date_query[0][0]
            temperature_dict2["maximum temperature"] = date_query[0][1]
            temperature_dict2["average temperature"] = date_query[0][2]
            return jsonify(temperature_dict2)

        else:
            return(f"error: The end date you type in is not in the dateset. Please try to type in a date from 2010-01-01 to 2017-08-23"), 404
        
    else:
        return(f"error: The start date you type in is not in the dateset. Please try to type in a date from 2010-01-01 to 2017-08-23"), 404

if __name__ == '__main__':
    app.run(debug=True)